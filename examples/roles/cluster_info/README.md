Node Reload
=========

Use this role to execute below failure scenario

* Single node reolad
* Sequential multi-node reload
* Simultaneous multi-node reload

In the case of sequential multi-node reload scenario, nodes attached to a particular cluster will be reloaded one after another. When the node failure ansible playbook got to know that the previous node is back to ready state then it triggers reload for next node.

Whereas in the case of simultaneous multi-node reload scenario, playbook triggers reload request for all attached nodes simultaneously. It will not wait for node to become ready before triggering request for next node.

Inputs:
---------

* Choose one of the option from menu

    1- Single-Node-Failure
    2- Sequential-Multi-Node-Failure
    3- Simultaneous-Multi-Node-Failure
    4- List Worker Nodes

* Cluster ID
* Node ID


Requirements
------------

The below requirements are needed on the host that executes k8s module.

python >= 3.6
kubernetes >= 12.0.0
PyYAML >= 3.11
jsonpatch


How to execute
---------------

Run below commands to export IAM_TOKEN & IMA_REFRESH_TOKEN in your CLI

```
1) APIKEY=<YOUR_API_KEY>

2) export IC_IAM_TOKEN=$(curl -X POST https://iam.cloud.ibm.com/identity/token -H 'Content-Type: application/x-www-form-urlencoded' -d "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=${APIKEY}" 2>/dev/null | jq '.access_token' | tr -d '"')

3) export IC_IAM_REFRESH_TOKEN=$(curl -s -X POST "https://iam.cloud.ibm.com/identity/token" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$APIKEY" -u bx:bx | jq '.refresh_token' | tr -d '"')

4) ansible-playbook <your_playbook_name> -vvv

```


