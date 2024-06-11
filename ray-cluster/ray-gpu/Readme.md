# Accessing GPU in Ray Cluster

This guide provides step-by-step instructions to enable GPU usage in Ray cluster by installing the NVIDIA GPU Operator and Device Plugin on your Kubernetes cluster.

## Prerequisites

- Kubernetes cluster with nodes that have NVIDIA GPUs.
- Helm installed on your system.

## Step 1: Install NVIDIA Device Plugin

The NVIDIA Device Plugin for Kubernetes is a DaemonSet that allows you to automatically expose NVIDIA GPUs on each node of your Kubernetes cluster.

### 1.1 Set Up NVIDIA Drivers

Ensure that the NVIDIA drivers are installed on your GPU nodes. You can check the driver installation by running:

```sh
nvidia-smi
```

This command should display information about your GPUs and the installed driver.

### 1.2 Install NVIDIA Container Toolkit

This is required to run GPU-accelerated containers. Follow the installation instructions from the [NVIDIA Container Toolkit documentation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

### 1.3 Deploy the NVIDIA Device Plugin

Apply the NVIDIA Device Plugin DaemonSet from the official NVIDIA repository:

```sh
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.15.0/deployments/static/nvidia-device-plugin.yml
```

## Step 2: Install NVIDIA GPU Operator

The NVIDIA GPU Operator automates the management of all NVIDIA software components needed to provision GPUs within Kubernetes.

### 2.1 Add the NVIDIA Helm Repository

Add the NVIDIA repository to Helm:

```sh
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
```

### 2.2 Install the NVIDIA GPU Operator

Install the NVIDIA GPU Operator using Helm:

```sh
helm install --wait --generate-name \
  nvidia/gpu-operator \
  --set operator.defaultRuntime=containerd \
  --set toolkit.version=1.11.0-ubi8
```

Replace `containerd` with your container runtime if different, and specify the desired version of the toolkit.

## Step 3: Verification

After installation, verify that the GPU operator and device plugin are running correctly.

### 3.1 Check the NVIDIA Device Plugin

```sh
kubectl get pods -n kube-system | grep nvidia
```

Ensure the NVIDIA device plugin DaemonSet is running on all GPU nodes.

### 3.2 Check the GPU Operator

```sh
kubectl get pods -n gpu-operator-resources
```

Verify that the GPU operator and its components are running.

## Documentation

For more detailed instructions and troubleshooting, refer to the following official documentation:

- **NVIDIA Device Plugin**
  - [Official Documentation](https://github.com/NVIDIA/k8s-device-plugin)
  - [Quick Start Guide](https://github.com/NVIDIA/k8s-device-plugin#quick-start)

- **NVIDIA GPU Operator**
  - [Official Documentation](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/index.html)
  - [Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/getting-started.html)


## Using GPU with Ray

  - [Official Documentation](https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/gpu.html)