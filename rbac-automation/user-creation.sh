#!/bin/bash

# Check if username is provided as an argument
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <username>"
  exit 1
fi

username=$1

# Step 1: Generate private key and certificate request for the specified user
openssl genrsa -out "$username.key" 2048 
openssl req -new -key "$username.key" -out "$username.csr" -subj "/CN=$username"

# Step 2: Create certificate signing request object in Kubernetes
cat <<EOF | kubectl create -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: "$username-csr"
spec:
  groups:
  - system:authenticated
  request: $(cat "$username.csr" | base64 | tr -d '\n')
  usages:
  - digital signature
  - key encipherment
  - client auth
  signerName: kubernetes.io/kube-apiserver-client
EOF

# Step 3: Approve certificate as admin
kubectl certificate approve "$username-csr"

# Step 4: Download user’s assigned certificate
kubectl get csr "$username-csr" -o jsonpath='{.status.certificate}' | base64 --decode > "$username.crt"

# Step 5: Generate kubeconfig for the user
kubectl config set-credentials "$username" --client-certificate="$username.crt" --client-key="$username.key"
kubectl config set-context "${username}-context" --cluster=minikube --namespace=test --user="$username"


echo "User $username configured successfully."
