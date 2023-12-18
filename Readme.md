# Setting Up WSL 2, Ubuntu 22.04 LTS, Docker, Minikube, and kubectl on Windows 10

This guide will walk you through the step-by-step process to set up WSL 2, install Ubuntu 22.04 LTS distribution, Docker, Minikube, and kubectl on Windows 10.

## Prerequisites

- Windows 10 Pro or Enterprise edition with Build 19041 or higher.
- Ensure that virtualization is enabled in BIOS settings.

## Step 1: Install WSL 2

1. Open PowerShell as Administrator and run:
   ```powershell
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
    ```
2. Restart your computer.

3. Download and install the WSL2 [Linux Kernel](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi) Update Package.

4. Set WSL 2 as the default version:
    
    ```
    wsl --set-default-version 2
    ```

## Step 2: Install Ubuntu 22.04 LTS

1. Open Microsoft Store, search for "Ubuntu 22.04 LTS," and click "Install."

2. Launch Ubuntu, set up your user account, and wait for the installation to complete.

## Step 3: Install Docker

1. Run series of commands to get right build of Docker installed
    
    ```Removes the old crap, gets the dependencies right, adds Docker key, adds Docker repo, installs the new hotness
    
    sudo apt-get remove docker docker-engine docker.io containerd runc
    sudo apt-get update
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
    sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt-get install docker-ce docker-ce-cli containerd.io -y
    ```
2. Run series of commands to ensure you can interact with Docker without root

    - Third command here is a trick to reload your profile without actually logging out
    - Closing out Ubuntu shell and starting over instead of third command is an option

    ```
    sudo groupadd docker
    sudo usermod -aG docker ${USER}
    su -s ${USER}
    ```

3. Test the Docker configuration

    ```
    sudo service docker start
    docker run hello-world
    ```

## Step 4: Install Minikube

1. Install Minikube:

    ```
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
    sudo dpkg -i minikube_latest_amd64.deb
    ```

2. Start Minikube:

    ```
    minikube start --driver=docker
    ```

## Step 5: Install kubectl
    
1.  Run the following commands:

    ```
    sudo apt update
    sudo apt install -y kubectl
    ```

2. Verify the installation:

    ```
    kubectl version --client
    ```

Congratulations! You've successfully set up WSL 2, Ubuntu 22.04 LTS, Docker, Minikube, and kubectl on Windows 10.


[Visit for installation guide for KeyCloak on Ubuntu 22.04 LTS](tree/main/keycloak/install-guide.md)

[Kubernetes Authentication and Authorization Demo](tree/main/rbac-demo/rbac-demo.md)