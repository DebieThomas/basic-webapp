# Commonly used commands

There are a couple of kubectl commands we use regularly. You can find them here.


**Login to the vSphere Kubernetes cluster**
````console
kubectl vsphere login --server=<IP_or_master_hostname> --insecure-skip-tls-verify
````

**Login to a Tanzu guest cluster**
````console
kubectl vsphere login --insecure-skip-tls-verify --tanzu-kubernetes-cluster-namespace research-concept --tanzu-kubernetes-cluster-name tkg01 --server=ip-of-vsphere-cluster
````

**Show available contexts**
````console
kubectl config get-contexts
````

**Switch context**
````console
kubectl config use-context <context>
````

**Apply yaml file**
````console
kubectl apply -f ./<name-of-file>.yaml
````

**Remove applied yaml file**
````console
kubectl delete -f ./<name-of-file>.yaml
````

**Show info for all running**
````console
kubectl get all
````

**Show details for all running**
````console
kubectl describe all
````

**Show logs for pod**
````console
kubectl logs <name-of-pod>
````
