**This is a deployment for running in a vSphere with Kubernetes environment (vSphere pods)**

Create a namespace 'research-concept' in your vSphere with Kubernetes cluster if it does not exist yet:

![](https://i.imgur.com/90WBygM.png)

Give yourself 'can edit' rights on the new namespace and assign the 'pacific-gold-storage-policy' to the namespace. Then click on 'open' under 'link to CLI Tools to access the namespace':

![](https://i.imgur.com/UyYWIhk.png)

Then, you can choose to donwload kubectl with the vsphere plugin. Place these two executables in your PATH or put them in the folder you'll be working from.

To connect do:
````console
kubectl vsphere login --server=<IP-of-the-webpage-you-got-when-clicking-link-to-cli-tools> --insecure-skip-tls-verify
````

Switch to the newly created namespace using:
````console
kubectl config use-context research-concept
````
Now run the deployment:
````console
kubectl apply -f deployment.yaml
````

**Specific to this deployment:**
In this deployment we create a NetworkPolicy to allow ingress and egress.

Because of the way the vSphere Kubernetes cluster works, we can't easily use a horizontal pod autoscaler. This is because we can't edit cluster-level settings, only inside the namespace, so installing metrics-server is not an easy task. 
Thus, an HPA is not used. To use autoscaling deployments in a guest cluster, check out the TKG deployment.

For some reason, the API deployment does not work without specifying a volume for /dev/shm
So to make I had to add this volume:
````console
volumes:
  - name: dshm
    emptyDir:
      medium: Memory
````
And mount it to /dev/shm in the deployment:
````console
volumeMounts:
  - mountPath: /dev/shm
    name: dshm
````
Then, the deployment started working.

In this deployment, we can find the external IP address of our application using the vCenter webGUI:

![](https://i.imgur.com/xLzqzp2.png)
