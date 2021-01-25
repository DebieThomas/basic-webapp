# Migration example

**Note:** The data we are migrating is from an SQL database. This is *definitely not* how you should migrate an SQL database. This is a proof of concept.

We are going to migrate our application from the Tanzu Kubernetes cluster to a GKE cluster.
Right now there is some data in that database:

![](https://i.imgur.com/cdOApTh.png)

We want that data to come with us to the new cluster.

We will begin in the tkg01 cluster:
````console
kubectl config use-context tkg01
````

Scale down the postgres deployment to 0. This way no data is being modified while we are migrating:
````console
kubectl scale deployment.apps/postgres --replicas=0
````

Now we create a new pod. This pod mounts the persistent volume that the postgres pod uses under /data (see datamounter.yaml):
````console
kubectl apply -f .\datamounter.yaml
````

When the pod is up and running, we use 'kubectl cp' to copy the contents to our local machine:
````console
kubectl cp dataaccess:/data data/
````

Now switch to the cluster you want to migrate to:

````console
kubectl config use-context gke_kubernetes-research-302208_europe-west1-c_my-first-cluster-1
````

In this cluster, we will first deploy the persistent volume claim. Don't deploy the rest of the application yet, as we need a clean pvc to copy our previous database to:
````console
kubectl apply -f .\pvc.yaml
````

Then we create a pod to access the pvc (similar to the pod we used to copy the data previously):
````console
kubectl apply -f .\gke-datamounter.yaml
````

When this pod is up and running, we once again use 'kubectl cp' to copy the contents from our local machine, to the persistent volume. When copying is complete, check that the data is there:
````console
kubectl cp ./data dataaccess:/
kubectl exec dataaccess -- ls -la /data
````

We can now dispose of this pod:
````console
kubectl delete -f .\gke-datamounter.yaml
````

Finally, we can apply our complete deployment (I edited the pvc out of this file, as it is already there. The rest of the file is the same as the deployment in the GKE folder):
````console
kubectl apply -f .\deployment_without_pvc.yaml
````

Wait for the deployment to go trough. You should now see that your data is there, on your new cluster!

![](https://i.imgur.com/E0Za2sa.png)
