# User Certificate and Context Setup Script

## Overview

This Bash script automates the process of creating a new user from certificate and user context in the kubeconfig file for Kubernetes. It uses OpenSSL to generate a private key and certificate request, creates a CertificateSigningRequest in Kubernetes, approves the request, and downloads the user's assigned certificate.

## Prerequisites

- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [OpenSSL](https://www.openssl.org/source/)

## Script Details

- **user_creation.sh**: The Bash script for creating a new user certificate and context.

## Usage

1. Make sure you have the prerequisites installed.

2. Execute the script, providing the username as an argument:

    ```bash
    ./user-creation.sh <username>
    ```

    Replace `<username>` with the desired username.

3. The script will generate the user's certificate and configure the kubeconfig file with the new user context.

4. Verify the configuration:

    ```bash
    kubectl config view
    kubectl config use-context <username>-context
    ```

## Notes

- Backup your kubeconfig file before running the script.



# Role and RoleBinding Automation Script

## Overview

This Bash script automates the process of creating a Role and RoleBinding in Kubernetes RBAC (Role-Based Access Control). It is designed to be used with a Kubernetes cluster to grant specific permissions to a user within a given namespace.

## Prerequisites

Ensure that you have the `kubectl` command-line tool installed and configured to connect to your Kubernetes cluster.

## Script Usage

1. Make sure you have the prerequisites installed.

2. Execute the script, providing the rolename username and namespace as an argument:

    ```bash
    ./rbac-automation.sh <role_name> <user_name> <namespace>

    ```

    Replace `<role_name> <user_name> <namespace>` with the desired rolename username and namespace.


