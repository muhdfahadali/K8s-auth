#!/bin/bash

set -e

# Define variables
KIND_CLUSTER_NAME="ray-cluster"
KIND_IMAGE="kindest/node:v1.23.0"
NAMESPACE="ray-cluster"
HELM_REPO="https://ray-project.github.io/kuberay-helm/"
HELM_CHART_VERSION="1.0.0"
CUSTOM_DOCKER_IMAGE="muhdfahadali/my-custom-ray"
DOCKERFILE_PATH="./Dockerfile"
RAY_AUTOSCALER_CONFIG_URL="https://raw.githubusercontent.com/ray-project/kuberay/release-1.1.0/ray-operator/config/samples/ray-cluster.autoscaler.yaml"

# Function to create Dockerfile
create_dockerfile() {
    cat <<EOF > $DOCKERFILE_PATH
# Start from the official Ray image
FROM rayproject/ray:2.9.0

# Install scikit-learn and any other dependencies you need
RUN pip install scikit-learn
EOF
}

# Function to build and push custom Docker image
build_and_push_docker_image() {
    docker build --no-cache -t $CUSTOM_DOCKER_IMAGE -f $DOCKERFILE_PATH .
    docker login
    docker push $CUSTOM_DOCKER_IMAGE
}

# Create a Kubernetes cluster with Kind
create_kind_cluster() {
    kind create cluster --name $KIND_CLUSTER_NAME --image=$KIND_IMAGE
}

# Deploy KubeRay operator
deploy_kuberay_operator() {
    helm repo add kuberay $HELM_REPO
    helm repo update
    kubectl create namespace $NAMESPACE || true
    helm install kuberay-operator kuberay/kuberay-operator --version $HELM_CHART_VERSION --namespace $NAMESPACE
}

# Create RayCluster custom resource with autoscaling enabled
create_raycluster_autoscaler() {
    curl -LO $RAY_AUTOSCALER_CONFIG_URL
    sed -i "s|image: rayproject/ray:2.9.0|image: $CUSTOM_DOCKER_IMAGE|g" ray-cluster.autoscaler.yaml
    kubectl apply -f ray-cluster.autoscaler.yaml --namespace $NAMESPACE
}

# Verify the setup
verify_setup() {
    kubectl get pods -n $NAMESPACE --watch
}

# Main function
main() {
    create_dockerfile
    build_and_push_docker_image
    create_kind_cluster
    deploy_kuberay_operator
    create_raycluster_autoscaler
    verify_setup
}

# Execute the main function
main
