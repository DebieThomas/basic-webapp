**This is a deployment for running in a Google Kubernetes Engine (GKE)**

I create a cluster on Google Cloud using the 'my first cluster' example Google provides, but changed the location to Europe. This is a cheap cluster good for testing purposes:

![](https://i.imgur.com/SJYr7Sa.png)

You need the Google Cloud SDK installed on your pc to access the cluster (or use Google Cloud shell)

To connect to your cluster, click on it, and click connect:

![](https://i.imgur.com/kCgxMVJ.png)

Then run the command the webpage presents in the Google Cloud SDK shell. The necessary config will automatically be applied to kubectl. You can check if you're in the right context by running:
````console
kubectl config get-contexts
````

![](https://i.imgur.com/lyxQx1J.png)

If there's an asterix next to the Google Cloud one, you're in the correct context. Otherwise switch to it using:
````console
kubectl config use-context <name-of-your-gke-context>
````


We will deploy the application in the default namespace:
````console
kubectl apply -f deployment.yaml
````

**Specific to this deployment:**
In this deployment, we use the 'standard' storageclass. Also, we don't have to configure anything for the horizontal pod autoscaler to work.

We can find the external IP address of our application in the Google Cloud webGUI:

![](https://i.imgur.com/QqxPQFp.png)

