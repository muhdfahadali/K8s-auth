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


