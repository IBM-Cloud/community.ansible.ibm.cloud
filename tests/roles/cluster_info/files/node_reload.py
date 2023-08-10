#!/usr/bin/python

import requests
import os
import json
import sys
import time

IAM_KEY = os.environ['IC_IAM_TOKEN']

class IKS_API:
 
    # Class Variable
    BASE_URL = 'https://containers.cloud.ibm.com/global/'
 
    # The init method or constructor
    def __init__(self, cluster_id, worker_id):
 
        # Instance Variable
        self.cluster_id = cluster_id
        self.worker_id  = worker_id

    def get_status(self,status_code):
        if status_code == 200 or status_code == 204:
            status = "OK. Request successfully processed"
        elif status_code == 401:
            status = "Unauthorized. The IAM token is invalid or expired."
        elif status_code == 404:
            status = "Not found. The specified cluster could not be found."
        elif status_code == 500:
            status = "Internal Server Error. IBM Cloud Kubernetes Service is currently unavailable."
        else:
            status = "ERROR. status_code mismatch"
        return status

    
    def get_node_operation(self,op):
        
        '''
        Node operation Menu: 

            1- Single-Node-Failure
            2- Sequential-Multi-Node-Failure
            3- Simultaneous-Multi-Node-Failure
            4- List Worker Nodes
        '''
        if op == 1:
            node_operation = "Single-Node-Failure"
        elif op == 2:
            node_operation = "Sequential-Multi-Node-Failure"
        elif op == 3:
            node_operation = "Simultaneous-Multi-Node-Failure"
        elif op == 4:
            node_operation = "List-Worker-Nodes"
        else:
            node_operation = "ERROR: Invalid operation"
        return node_operation


    # Method to get the list of owrker nodes from cluster
    def list_worker_nodes(self):
        headers = {"Authorization": IAM_KEY}
        TARGET_URL = ('v1/clusters/{0}/workers'.format(self.cluster_id))
        response = requests.get(
                        IKS_API.BASE_URL+TARGET_URL,
                        headers=headers
                    )
        print(response.json())
        return response.json() 

    # Method to reload a node from cluster
    def reload_node(self, cluster_id, worker_id):
        data = {'action': 'reload','force': True}
        headers = {"Authorization": IAM_KEY}
        TARGET_URL = ('v1/clusters/{0}/workers/{1}'.format(cluster_id,worker_id))
        response = requests.put(
                        IKS_API.BASE_URL+TARGET_URL,
                        headers=headers,
                        json=data
                    )
        print("Status = ", self.get_status(response.status_code))


    # Method to check whether given node is active or not
    def is_node_active(self, node_id):
        worker_nodes = self.list_worker_nodes()
        for node in worker_nodes:
            if node['id'] == node_id and node['status'] == "Ready":
                return True
        return False 

    # Method to make Sequential Node failure
    def sequential_node_failure(self):
        worker_nodes = self.list_worker_nodes()
        print("Number of worker_nodes = ", len(worker_nodes))
        for node in worker_nodes:
            for key, value in node.items():
                # trigger node reload
                if key == "id":
                    print("Reloading Node {0} in Cluster {1}".format(value,self.cluster_id))
                    self.reload_node(self.cluster_id,value)
                    time.sleep(20)
                    while self.is_node_active(value) ==  False:
                        print('Wait for 1 min: state to become READY')
                        time.sleep(120)


    # Method to make Simultaneous Node failure
    def simultaneous_node_failure(self):
        worker_nodes = self.list_worker_nodes()
        print("Number of worker_nodes = ", len(worker_nodes))
        for node in worker_nodes:
            for key, value in node.items():
                # trigger node reload
                if key == "id":
                    print("Reloading Node {0} in Cluster {1}".format(value,self.cluster_id))
                    self.reload_node(self.cluster_id,value)
          
 
    # Set Cluster ID
    def set_cluster_id(self, cluster_id):
        self.cluster_id = cluster_id

    # Set Worker ID
    def set_worker_id(self, worker_id):
        self.worker_id = worker_id
 
    # Retrieves clusterID
    def get_cluster_id(self):
        return self.cluster_id

    # Retrieves Worker ID
    def get_worker_id(self):
        return self.worker_id

       
 
if __name__ == "__main__":
    '''
    Command Line Arguments: 

    sys.argv[1]- Node operation
    sys.argv[2]- Cluster ID
    sys.argv[3]- Worker Node ID
    '''
    
    apiObj = IKS_API(sys.argv[2],sys.argv[3]) 
    
    '''
    Node operation Menu: 

    1- Single-Node-Failure
    2- Sequential-Multi-Node-Failure
    3- Simultaneous-Multi-Node-Failure
    4- List worker nodes
    '''

    node_operation_kind = apiObj.get_node_operation(int(sys.argv[1]))
    print("Node Operation: ",node_operation_kind)
    if node_operation_kind == "Single-Node-Failure":
        apiObj.reload_node(sys.argv[2],sys.argv[3])
    elif node_operation_kind == "Sequential-Multi-Node-Failure":
        apiObj.sequential_node_failure()
    elif node_operation_kind == "Simultaneous-Multi-Node-Failure":
        apiObj.simultaneous_node_failure()
    elif node_operation_kind == "List-Worker-Nodes":
        apiObj.list_worker_nodes()
    else:
        print("ERROR: INVALID OPERATION")
