**KubeRay Autoscaling**

This guide explains how to configure the Ray Autoscaler on Kubernetes.

**Step 1: Create a Kubernetes cluster with Kind**
This step creates a local Kubernetes cluster using Kind. 

```
kind create cluster --image=kindest/node:v1.23.0
```
## Step 2: Deploy a KubeRay operator
Deploy the KubeRay operator with the Helm chart repository.

```
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
```

Install both CRDs and KubeRay operator v1.0.0.

```
helm install kuberay-operator kuberay/kuberay-operator --version 1.0.0 --namespace ray-cluster
```
Confirm that the operator is running in the namespace `default`.

```
kubectl get pods  -n ray-cluster

# NAME                                          READY   STATUS              RESTARTS      AGE
# kuberay-operator-7c96fc695c-8cnws             1/1     Running             1 (11d ago)   13d
# raycluster-kuberay-head-hkcwg                 1/1     Running             0             13d
# raycluster-kuberay-worker-workergroup-7kklb   1/1     Running             0             13d
```
**Step 3: Create a RayCluster custom resource with autoscaling enabled**

```
curl -LO https://raw.githubusercontent.com/ray-project/kuberay/release-1.1.0/ray-operator/config/samples/ray-cluster.autoscaler.yaml
kubectl apply -f ray-cluster.autoscaler.yaml --namespace ray-cluster
```
**Step 4: Verify the Kubernetes cluster status**

Check the Pods in the `ray-cluster` namespace.
```
kubectl get pods -l ray.io/is-ray-node=yes --namespace=ray-cluster

# NAME                                          READY   STATUS    RESTARTS   AGE
# raycluster-autoscaler-head-nq6sd              2/2     Running   0          3m27s
# raycluster-kuberay-head-hkcwg                 1/1     Running   0          13d
# raycluster-kuberay-worker-workergroup-7kklb   1/1     Running   0          13d
```
Check the ConfigMap in the `ray-cluster` namespace.
```
kubectl get configmaps --namespace=ray-cluster

#NAME                  DATA   AGE
# kube-root-ca.crt      1      48d
# ray-example           2      5m27s
# ray-operator-leader   0      48d
```
The RayCluster has one head Pod and zero worker Pods. The head Pod has two containers: a Ray head container and a Ray Autoscaler sidecar container. Additionally, the ray-cluster.autoscaler.yaml includes a ConfigMap named ``ray-example`` that houses two Python scripts: ``detached_actor.py`` and ``terminate_detached_actor.py``.

`detached_actor.py` is a Python script that creates a detached actor which requires 1 CPU.
```
import ray
import sys

@ray.remote(num_cpus=1)
class Actor:
  pass

ray.init(namespace="default_namespace")
Actor.options(name=sys.argv[1], lifetime="detached").remote()
```
`terminate_detached_actor.py` is a Python script that terminates a detached actor.

```
import ray
import sys

ray.init(namespace="default_namespace")
detached_actor = ray.get_actor(sys.argv[1])
ray.kill(detached_actor)
```
**Step 5: Trigger RayCluster scale-up by creating detached actors**

Create a detached actor ``actor1`` which requires 1 CPU.
```
kubectl exec -it raycluster-autoscaler-head-nq6sd --namespace=ray-cluster -- python3 detached_actor.py actor1

```
The Ray Autoscaler creates a new worker Pod.
```
kubectl get pods -l=ray.io/is-ray-node=yes --namespace=ray-cluster
# NAME                                             READY   STATUS    RESTARTS   AGE
# raycluster-autoscaler-head-nq6sd                 2/2     Running   0          20m
# raycluster-autoscaler-worker-small-group-tsfqb   1/1     Running   0          2m25s
```

Create second detached actor ``actor2`` which requires 1 CPU.
```
kubectl exec -it raycluster-autoscaler-head-nq6sd -n ray-cluster -- python3 detached_actor.py actor2

```
The Ray Autoscaler creates another new worker Pod.
```
kubectl get pods -l=ray.io/is-ray-node=yes --namespace=ray-cluster

# NAME                                             READY   STATUS    RESTARTS   AGE
# raycluster-autoscaler-head-nq6sd                 2/2     Running   0          23m
# raycluster-autoscaler-worker-small-group-bnjqw   1/1     Running   0          73s
# raycluster-autoscaler-worker-small-group-tsfqb   1/1     Running   0          5m16s
```
List all actors in the Ray cluster.

```
kubectl exec -it raycluster-autoscaler-head-nq6sd --namespace=ray-cluster -- ray list actors

Defaulted container "ray-head" out of: ray-head, autoscaler

======== List: 2024-05-06 14:50:57.856213 ========
Stats:
------------------------------
Total: 2

Table:
------------------------------
#    ACTOR_ID                          CLASS_NAME    STATE      JOB_ID  NAME    NODE_ID                                                     PID  RAY_NAMESPACE
# 0  0212a14cbf25f371c95d9dad01000000  Actor         ALIVE    01000000  actor1  1ff788090c63a10c634273a11aa1636ec40cee169e19520bec9d2e63     77  ray-cluster
# 1  659040c3d0b51e32ded49cf502000000  Actor         ALIVE    02000000  actor2  8a84c0348285d1646a36bd5ba70120fae0c0502c68dc4dcfa7dae634     76  ray-cluster
```
The Ray Autoscaler generates a new worker Pod for each new detached actor. This is because the rayStartParams field in the Ray head specifies num-cpus: "0", preventing the Ray scheduler from scheduling any Ray actors or tasks on the Ray head Pod.

**Step 6: Trigger RayCluster scale-down by terminating detached actors**

Terminate the detached actor "actor1".
```
kubectl exec -it raycluster-autoscaler-head-nq6sd --namespace=ray-cluster -- python3 terminate_detached_actor.py actor1

```
A worker Pod will be deleted after `idleTimeoutSeconds` (default 60s) seconds.

```
# NAME                                          READY   STATUS    RESTARTS   AGE
# raycluster-autoscaler-head-nq6sd              2/2     Running   0          35m
```


Terminate the detached actor "actor2".
```
kubectl exec -it raycluster-autoscaler-head-nq6sd --namespace=ray-cluster -- python3 terminate_detached_actor.py actor2
```
A worker Pod will be deleted after `idleTimeoutSeconds` (default 60s) seconds.
```
kubectl get pods -l=ray.io/is-ray-node=yes -n ray-cluster

# NAME                                             READY   STATUS    RESTARTS   AGE
# raycluster-autoscaler-head-nq6sd                 2/2     Running   0          30m
# raycluster-autoscaler-worker-small-group-tsfqb   1/1     Running   0          11m
```

**Step 7: Ray Autoscaler observability**

Method 1: "ray status"
```
kubectl exec raycluster-autoscaler-head-nq6sd --namespace=ray-cluster -it -c ray-head -- ray status
======== Autoscaler status: 2024-05-06 15:02:47.261890 ========
Node status
---------------------------------------------------------------
Active:
 1 head-group
Pending:
 (no pending nodes)
Recent failures:
 (no failures)

Resources
---------------------------------------------------------------
Usage:
 0B/1.86GiB memory
 0B/501.18MiB object_store_memory

Demands:
 (no resource demands)
```
Method 2: "kubectl logs"

```
kubectl logs raycluster-autoscaler-head-nq6sd --namespace=ray-cluster -c autoscaler | tail -n 20
2024-05-06 15:04:23,836 INFO autoscaler.py:426 --
======== Autoscaler status: 2024-05-06 15:04:23.836054 ========
Node status
---------------------------------------------------------------
Active:
 1 head-group
Pending:
 (no pending nodes)
Recent failures:
 (no failures)

Resources
---------------------------------------------------------------
Usage:
 0B/1.86GiB memory
 0B/501.18MiB object_store_memory

Demands:
 (no resource demands)
2024-05-06 15:04:23,837 INFO autoscaler.py:469 -- The autoscaler took 0.046 seconds to complete the update iteration.
```