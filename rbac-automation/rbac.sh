#!/bin/bash

# Check if namespace is provided as an argument
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <role_name> <user_name> <namespace>"
  exit 1
fi

role_name=$1
user_name=$2
namespace=$3

# Check if the Role already exists
if kubectl get role "$role_name" -n "$namespace" &> /dev/null; then
  echo "Error: Role '$role_name' already exists in namespace '$namespace'."
  exit 1
fi

# Check if the RoleBinding already exists
if kubectl get rolebinding "$role_name-binding" -n "$namespace" &> /dev/null; then
  echo "Error: RoleBinding '$role_name-binding' already exists in namespace '$namespace'."
  exit 1
fi

# Step 1: Create a Role to read pods in the specified namespace
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: "$namespace"
  name: "$role_name"
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
EOF

# Step 2: Create a RoleBinding for the specified user with the created Role
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: "$role_name-binding"
  namespace: "$namespace"
subjects:
- kind: User
  name: "$user_name"
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: "$role_name"
  apiGroup: rbac.authorization.k8s.io
EOF

echo "Role and RoleBinding created successfully for user $user_name reading pods in namespace $namespace."
