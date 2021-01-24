Run the tkc-runthisfirst.yaml file first. This will create a Tanzu Kubernetes Cluster

This can take a while to properly apply. Wait untill the cluster is fully created.

When the cluster is created, switch to it:

kubectl vsphere login --insecure-skip-tls-verify --tanzu-kubernetes-cluster-namespace research-concept --tanzu-kubernetes-cluster-name tkg01 --server=192.168.0.129

Then we need to install the metrics server, otherwise the hpa will not work.