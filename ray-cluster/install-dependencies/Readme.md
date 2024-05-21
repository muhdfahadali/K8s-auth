# Installing Dependencies in Kubernetes Head and Worker Pods

This guide provides instructions for installing dependencies in Kubernetes head and worker pods using Docker images and container hooks, such as `postStart`.

## Prerequisites

- A Kubernetes cluster
- `kubectl` command-line tool installed and configured
- Docker installed

## Method 1: Container Image  

### Overview

Create Docker images Start from the official Ray image for both head and then add additional dependencies.

### Step 1: Create Docker Images

```
# Start from the official Ray image
FROM rayproject/ray:2.9.0

# Install scikit-learn and any other dependencies you need
RUN pip install scikit-learn

```

### Step 2: Build the Docker Image:

```
docker build -t muhdfahadali/my-custom-ray:2.9.0 .
```

### Step 3: Log in to Docker Hub from Your Terminal:

```
docker login
```

### Step 4: Push Custom Image to Docker Hub:

```
docker push muhdfahadali/my-custom-ray:2.9.0
```

### Step 5: Update Your RayCluster YAML:

Replace image rayproject/ray:2.9.0 with muhdfahadali/my-custom-ray:2.9.0 in RayCluster YAML configuration:

```
    spec:
        containers:
        - image: muhdfahadali/my-custom-ray:2.9.0
          lifecycle:
            preStop:
              exec:
                command:
                - /bin/sh
                - -c
                - ray stop
```

### Step 6: Delete the Existing Ray Head Pod:

Delete the head pod to force Kubernetes to recreate it with the new image:

```
kubectl delete pod raycluster-autoscaler-head-nxhdb -n ray-cluster
```

### Step 7: Verify the New Pod:

Kubernetes will automatically create a new head pod using the updated Docker image with the dependencies installed.

## Method 2: Container Hooks

### Step 1: Update Your RayCluster YAML

Create Kubernetes manifests for the head and worker pods.

#### Head Pod Manifest

```yaml  
headGroupSpec:
    rayStartParams:
      num-cpus: "0"
    template:
      spec:
        containers:
        - image: rayproject/ray:2.9.0
          lifecycle:
            postStart:
              exec:
                command: ["/bin/bash", "-c", "/usr/local/bin/setup-head.sh"]
```

#### Worker Pod Manifest

```yaml  
workerGroupSpec:
    rayStartParams:
      num-cpus: "0"
    template:
      spec:
        containers:
        - image: rayproject/ray:2.9.0
          lifecycle:
            postStart:
              exec:
                command: ["/bin/bash", "-c", "/usr/local/bin/setup-worker.sh"]
```


### Step 6: Delete the Existing Pod:

Delete the head or worker pod to force Kubernetes to recreate it with the all dependencies installed:

```
kubectl delete pod raycluster-autoscaler-head-nxhdb -n ray-cluster
```

### Step 7: Verify the New Pod:

Kubernetes will automatically create a new head or worker pod using the added configration file with the dependencies installed.

## Conclusion

You have now set up head and worker pods in a Kubernetes cluster with dependencies installed using Docker images and `postStart` hooks. Customize the `setup-head.sh` and `setup-worker.sh` scripts to fit your specific setup requirements.