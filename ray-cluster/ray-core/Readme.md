**Connecting to Remote Cluster from Local Machine**

To connect to a remote cluster from your local machine, follow these steps. Ensure you have VPN access before proceeding.

**Step 1: Connect to the Server**

Run the following command to establish an SSH connection to the remote server:

```bash
ssh -J fahadali@192.168.209.133:2522 fahadali@192.168.209.37
```

Replace `fahadali@192.168.209.133:2522` with your VPN username and the IP address and port of your VPN server.

**Step 2: Copy kubeconfig to local machine**

After establishing the SSH connection, copy the kubeconfig file from the remote server to your local machine's `.kube` directory:

```bash
scp fahadali@192.168.209.37:/home/fahadali/.kube/config ~/.kube/config
```

This command fetches the kubeconfig file from the remote server and places it in your local machine's `.kube` directory.

**Step 3: Create a Proxy Inside the Remote Server**

To access the Kubernetes API from your local machine, create a proxy inside the remote server using the following command:

```bash
kubectl proxy --port 9040
```

This command starts a proxy server on the remote server's port 9040.

**Step 4: Create SSH Tunnel**

Finally, create an SSH tunnel from your local machine to the remote server to forward traffic to the Kubernetes proxy:

```bash
ssh -L 9040:localhost:9040 -J fahadali@192.168.209.133:2522 fahadali@192.168.209.37 -N
```

This command forwards traffic from port 9040 on your local machine to port 9040 on the remote server via SSH.

Now you should be able to access the Kubernetes API on your local machine through the proxy running on port 9040.