**This is a deployment for running in a Tanzu Kubernetes cluster (in the case of the research I conducted, a guest cluster running in vSphere with Kubernetes)**

Create a namespace 'research-concept' in your vSphere with Kubernetes cluster if it does not exist yet.

Run the tkc-runthisfirst.yaml file first. This will create a Tanzu Kubernetes Cluster in the 'research-concept' namespace (create that namespace first)

This can take a while to properly apply. Wait untill the cluster is fully created.

When the cluster is created, switch to it:

````console
kubectl vsphere login --insecure-skip-tls-verify --tanzu-kubernetes-cluster-namespace research-concept --tanzu-kubernetes-cluster-name tkg01 --server=ip-of-vsphere-cluster
````

Then we need to install the metrics server, otherwise the horizontal pod autoscaler will not work.
````console
kubectl apply -f metrics-runthissecond.yaml
````
Finally, we can deploy the workload:
````console
kubectl apply -f deployment.yaml
````
**Specific to this deployment:**
In this deployment, we also create a 'PodSecurityPolicy'. The one used here is the least restrictive one you can apply. If we don't do this, no pods will be created.

Because we installed the metrics server, we can also use a horizontal pod autoscaler. This HPA will scale the number of pods from 1 to 10, depending on the average load across the pods...

In this deployment, we can find the external IP address of our application using:
````console
kubectl get all
````

![](https://i.imgur.com/BGmVBco.png)

At the bottom we can also see the status of our HPA