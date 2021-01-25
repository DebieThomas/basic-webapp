# Basic web app - adapted for vSphere with Kubernetes

This is a sample application. It might be tempting to use this awesome application in a production environment: **do not use this app in production**.

vSphere with Kubernetes installation
---
For this project I used these guides to create a minimal install of vSphere with Kubernetes:
https://www.virtuallyghetto.com/2020/04/deploying-a-minimal-vsphere-with-kubernetes-environment.html

https://github.com/lamw/vghetto-vsphere-with-kubernetes-external-nsxt-automated-lab-deployment

The deployment script in this repo is the same as in the repo above, this is **not** my own. All credits for it and the guides go to the original creator.

**I will now explain what I had to change and configure in these guides to get it installed**

We need quite a few IP-addresses for the setup, so it might be easier to deploy this in a new network/subnet. VLANs are not required, but the switch you use has to support an MTU of 1600.

These are the addresses I used (some of the numbering might seem unlogical, but that's because I didn't plan the naming and IP-addresses too well in the beginning and was too far in the deployment when I noticed to change it):

**Physical environment:**
| Hostname                   | IP Address                     | Function                     |
|----------------------------|--------------------------------|------------------------------|
| n/a                        | 192.168.0.1                    | Default gateway              |
| esxi1.localdomain          | 192.168.0.31                   | ESXi (vSAN cluster)          |
| esxi2.localdomain          | 192.168.0.21                   | ESXi (vSAN cluster)          |
| esxi0.localdomain          | 192.168.0.41                   | ESXi (vSAN witness & VCSA)   |
| vcenter.localdomain        | 192.168.0.51                   | VCSA                         |
| n/a                        | 192.168.0.40                   | DNS server                   |
| n/a                        | 192.168.0.22                   | vSAN IP for ESXi2            |
| n/a                        | 192.168.0.32                   | vSAN IP for ESXi1            |


**Nested environment:**
(The addresses for K8s Master Control Plane VMs, ingress and egress are ranges, so the whole block of addresses should be free)

| Hostname                   | IP Address                     | Function                     |
|----------------------------|--------------------------------|------------------------------|
| pacific-vcsa-3.cpbu.corp   | 192.168.0.13                   | vCenter Server               |
| pacific-esxi-7.cpbu.corp   | 192.168.0.12                   | ESXi                         |
| pacific-nsx-edge.cpbu.corp | 192.168.0.16                   | NSX-T Edge                   |
| pacific-nsx-ua.cpbu.corp   | 192.168.0.15                   | NSX-T Unified Appliance      |
| n/a                        | 192.168.0.14                   | T0 Static Route Address      |
| n/a                        | 192.168.0.120 to 192.168.0.125 | K8s Master Control Plane VMs |
| n/a                        | 192.168.0.140/27               | Ingress CIDR Range           |
| n/a                        | 192.168.0.160/27               | Engress CIDR Range           |


vSphere installation:
---
Configure a vSphere environment with:

2 big ESXi hosts with at least 8 CPU cores and 64GB RAM. These are going in a vSAN cluster, they need at least 1 SSD and 1 HDD with a minimum capacity of 1TB for the HDD)

1 small ESXi host with at least 4 CPU cores and 24GB RAM. This node will host the VCSA for the physical environment and serve as a vSAN witness host. Make sure this host has a local datastore, plus 2 unused disks for the witness functionality

Also configure a DNS server in your network (a Pi-Hole instance with blocking disabled on 192.168.0.40 in my case. Not at all enterprise software but very easy to configure local DNS entries on) in which you configure the FQDNs of all the entries with a hostname in the tables above.

![](https://i.imgur.com/ZjlgjI9.png)

Put the 2 big ESXi hosts in a cluster with vSAN, DRS and HA enabled. 

Add the small ESXi hosts too the datacenter as well, but not in the cluster. To get it to work as vSAN witness, add a vmkernel adapter with vSAN functionality to this host:

![](https://i.imgur.com/lVl1UeK.png)

---
**If all requirements are met, you can configure vSAN with the vSAN quickstart wizard:**
![](https://i.imgur.com/92OZJn6.png)

Add the physical network interface to the Dswitch:
![](https://i.imgur.com/63PXuh0.png)

Assign static IPs for vSAN traffic to the hosts:
![](https://i.imgur.com/u8fAPLT.png)

In advanced options, choose "two node cluster", I set up these NTP servers:
![](https://i.imgur.com/XKU8Rhh.png)

Claim the HDDs for capacity and the SSDs for cache:
![](https://i.imgur.com/OtIQfBy.png)

Select the small ESXi host as witness:
![](https://i.imgur.com/QvUsgGK.png)

Claim the witness host disks:
![](https://i.imgur.com/WoO3uGV.png)

vSAN setup is now complete

---

When vSAN is fully configured, go to the DSwitch settings and set the MTU to a value of 1600:
![](https://i.imgur.com/x90WFTJ.png)

Using SSH or ESXi shell, run this command on each ESXi node in the vSAN cluster (otherwise you will have problems using nested ESXi instances
```console
esxcli system settings advanced set -o /VSAN/FakeSCSIReservations -i 1
````

Nested vSphere with Kubernetes installation
---

Install PowerShell Core 7.0.0 and PowerCLI 12.0.0 on your pc (other versions might cause problems)

Change the 3 variables in the beginning of the script so they contain the correct values for your vCenter server. Also change the path to the OVA files:
![](https://i.imgur.com/t7fh9Xx.png)

In the minimal version of this script, we use **one** of each of these appliances with at least these specifications:
| Component   | vCPUs  | vMEM (GB) |
|-------------|--------|-----------|
| ESXi        | 4      | 36        |
| VCSA        | 2      | 12        |
| NSX Manager | 4      | 12        |
| NSX Edge    | 8      | 32        |

The script in this repo already contains the necessary changes to make it a minimal install. If you're starting from the original script, you have to change these values too:
```
$configureVSANDiskGroup = 0
$clearVSANHealthCheckAlarm = 0
$moveVMsIntovApp = 0
````
Also check these values:
![](https://i.imgur.com/0RbkoZK.png)
Some of them point to where the nested environment will be deployed to, like VMDatacenter, VMCluster and VMDatastore.

To make it easier I marked all lines that need to be checked/changed with **CHECKTHISLINE**

When the script is adapted to our configuration, we can run it in Powershell Core:
![](https://i.imgur.com/zUYLw2d.png)
![](https://i.imgur.com/wkuMmWp.png)

If, apart from the above two errors, everything completes fine, you can proceed. We will fix these errors manually.

To proceed, SSH into the newly created VCSA. Open a shell (command 'shell') and change the following values in the file */etc/vmware/wcp/wcpsvc.yaml*
```
minmasters 2
maxmasters 2
```
Then, restart the workload management service:
```console
service-control --restart wcp
````

Now, to avoid another error I got we have to do the following:

On every switch (physical (if managed), vswitch, dswitch, nested dswitch) change the MTU to 1600.

On every vmware network (nested & not-nested) under 'security' allow 'promiscuous mode' and 'forged transmits':
![](https://i.imgur.com/VdVPG18.png)

Only after doing these two things, I got everything working.

**Manually fixing the 2 errors in the script:**
In a webbrowser, go to https://ip-of-your-nsxt-manager and login with the credentials 'admin' and 'VMware1!VMware1!' (unless you changed these)

It's possible you get an error message instead of the GUI. If this is the case, wait a while and try again, or try restarting the NSX manager VM (it can take more than 10 minutes for the GUI to come back sometimes)

On the dashboard, click on Tier 0 gateway (disregard differences in the other settings, the NSX T in this screenshot was already running):
![](https://i.imgur.com/tAeFWO6.png)

Click on the 3 dots next to Pacific-T0-Gateway and choose edit

Open the 'interfaces' tab:
![](https://i.imgur.com/Bg2kBbW.png)

Create a new interface with the following settings (IP address can be different depending on your configuration):
![](https://i.imgur.com/7yQFRG8.png)

Save this interface and then go to 'routes' and click on 'static routes':
![](https://i.imgur.com/hymjzjz.png)

Add a static route like this one:
![](https://i.imgur.com/68cLnH4.png)

Next hop looks like this (to your default gateway):
![](https://i.imgur.com/5n7WQAF.png)

---

Enabling workload management
---
Now that everything is configured, you can proceed to enable workload management in the nested vSphere environment. This is mostly just following the wizard with your network settings:
https://github.com/lamw/vghetto-vsphere-with-kubernetes-external-nsxt-automated-lab-deployment#enable-workload-management

Enabling this feature can take quite a while. Seeing a few errors is not abnormal either. If it takes longer than an hour and a half, something is probably wrong.

Do you see 'config status: running'? Congratulations, you now have vSphere 7 with Kubernetes!
![](https://i.imgur.com/itnVyDR.png)

