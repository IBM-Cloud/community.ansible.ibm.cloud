# coding: utf-8

# (C) Copyright IBM Corp. 2022.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ibm_container_cluster_info
author: Umar Ali (umarali.nagoor@in.ibm.com)
version_added: "1.0"
short_description: return the IKS cluster info
requirements: []
description:
    - Return the IKS cluster details like list of pools, list of worker nodes, list of ALBs, list of bounded services and etc .
options:
    name:
        required: True
        type: str
        default: null
        description:
            - Name or ID of the IKS cluster.
    alb_type:
        required: False
        type: str
        default: null
        choices: [ "public", "private" and "all"]
        description:
            - Type of ALBs to fetch
    
    list_bounded_services:
        required: False
        type: bool
        default: null
        choices: [ "true", "false"]
        description:
            - Mention whether to list down the bounded services or not

    ibmcloud_api_key:
        description:
            - The IBM Cloud API key to authenticate with the IBM Cloud
              platform. This can also be provided via the environment
              variable 'IC_API_KEY'.
        required: True

    resource_group_id:
        required: False
        type: str
        description:
            - ID of the resource group that the cluster is in. To check the resource group ID of the cluster, use the GET /v1/clusters/idOrName API.
    
    iam_token:
        required: True
        type: str
        description:
            - IBM Cloud Identity and Access Management (IAM) token. To retrieve your IAM token, run ibmcloud iam oauth-tokens.
'''


EXAMPLES = r'''
# Target the cluster which is present in default resource group
- ibm_container_cluster_info:
    name: "{{ name }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    alb_type: "{{ alb_type }}"
    iam_token : "{{ IC_IAM_TOKEN }}"
    list_bounded_services: "{{ list_bounded_services }}"

# Target the cluster which is present in a particular resource group
- ibm_container_cluster_info:
    name: "{{ name }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    resource_group_id: "{{ resource_group_id }}"
    alb_type: "{{ alb_type }}"
    iam_token : "{{ IC_IAM_TOKEN }}"
    list_bounded_services: "{{ list_bounded_services }}"

# Target the cluster by name
- ibm_container_cluster_info:
    name: "{{ name }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    resource_group_id: "{{ resource_group_id }}"
    alb_type: "{{ alb_type }}"
    iam_token : "{{ IC_IAM_TOKEN }}"
    list_bounded_services: "{{ list_bounded_services }}"

# Target the cluster by ID
ibm_container_cluster_info:
    name: "{{ cluster_id }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    resource_group_id: "{{ resource_group_id }}"
    alb_type: "{{ alb_type }}"
    iam_token : "{{ IC_IAM_TOKEN }}"
    list_bounded_services: "{{ list_bounded_services }}"
'''

RETURN = r'''
worker_pools:
    description: List of worker pools
    type: list of dictionaries
    sample: [
            {
                "autoscaleEnabled": false,
                "id": "cbftntmd0tmoqpjhtqe0-07e1b20",
                "isBalanced": false,
                "isolation": "public",
                "labels": {
                    "ibm-cloud.kubernetes.io/worker-pool-id": "cbftntmd0tmoqpjhtqe0-07e1b20"
                },
                "machineType": "b3c.4x16.encrypted",
                "name": "default",
                "operatingSystem": "UBUNTU_18_64",
                "reasonForDelete": "",
                "region": "us-south",
                "sizePerZone": 3,
                "state": "active",
                "zones": [
                    {
                        "id": "dal10",
                        "privateVlan": "3249706",
                        "publicVlan": "3249704",
                        "workerCount": 0
                    }
                ]
            },
            {
                "autoscaleEnabled": false,
                "id": "cbftntmd0tmoqpjhtqe0-36505bb",
                "isBalanced": false,
                "isolation": "public",
                "labels": {
                    "ibm-cloud.kubernetes.io/worker-pool-id": "cbftntmd0tmoqpjhtqe0-36505bb"
                },
                "machineType": "b3c.4x16.encrypted",
                "name": "testworkerpool",
                "operatingSystem": "UBUNTU_18_64",
                "reasonForDelete": "",
                "region": "us-south",
                "sizePerZone": 3,
                "state": "active",
                "zones": [
                    {
                        "id": "dal10",
                        "privateVlan": "3249706",
                        "publicVlan": "3249704",
                        "workerCount": 2
                    }
                ]
            },
    ]
worker_nodes:
    description: List of worker nodes
    type: list of dictionaries
    sample: [
            {
                "errorMessage": "",
                "errorMessageDate": "",
                "id": "kube-cbftntmd0tmoqpjhtqe0-myclusterda-myworke-00000799",
                "isolation": "public",
                "kubeVersion": "1.23.9_1540",
                "location": "dal10",
                "machineType": "b3c.4x16.encrypted",
                "masterVersionEOS": "",
                "pendingOperation": "",
                "poolName": "myworkerpool2",
                "poolid": "cbftntmd0tmoqpjhtqe0-585fd9f",
                "privateIP": "10.5.113.75",
                "privateVlan": "3249706",
                "publicIP": "169.63.234.226",
                "publicVlan": "3249704",
                "reasonForDelete": "",
                "state": "normal",
                "status": "Ready",
                "statusDate": "2022-08-22T10:03:16+0000",
                "statusDetails": "",
                "targetVersion": "1.23.9_1541",
                "trustedStatus": "unsupported",
                "versionEOS": ""
            },
            {
                "errorMessage": "",
                "errorMessageDate": "",
                "id": "kube-cbftntmd0tmoqpjhtqe0-myclusterda-myworke-00000862",
                "isolation": "public",
                "kubeVersion": "1.23.9_1540",
                "location": "dal10",
                "machineType": "b3c.4x16.encrypted",
                "masterVersionEOS": "",
                "pendingOperation": "",
                "poolName": "myworkerpool2",
                "poolid": "cbftntmd0tmoqpjhtqe0-585fd9f",
                "privateIP": "10.5.113.108",
                "privateVlan": "3249706",
                "publicIP": "169.63.234.230",
                "publicVlan": "3249704",
                "reasonForDelete": "",
                "state": "normal",
                "status": "Ready",
                "statusDate": "2022-08-22T10:03:16+0000",
                "statusDetails": "",
                "targetVersion": "1.23.9_1541",
                "trustedStatus": "unsupported",
                "versionEOS": ""
            },
    ]
alb:
    description: List of ALBs
    type: list of dictionaries
    sample: [
                {
                    "albBuild": "",
                    "albID": "private-crcbftntmd0tmoqpjhtqe0-alb1",
                    "albType": "private",
                    "albip": "",
                    "authBuild": "",
                    "clusterID": "cbftntmd0tmoqpjhtqe0",
                    "createdDate": "",
                    "disableDeployment": false,
                    "enable": false,
                    "name": "",
                    "nlbVersion": "1.0",
                    "numOfInstances": "",
                    "resize": false,
                    "state": "disabled",
                    "status": "disabled",
                    "vlanID": "3249706",
                    "zone": "dal10"
                },
                {
                    "albBuild": "1.2.1_2487_iks",
                    "albID": "public-crcbftntmd0tmoqpjhtqe0-alb1",
                    "albType": "public",
                    "albip": "150.238.60.150",
                    "authBuild": "",
                    "clusterID": "cbftntmd0tmoqpjhtqe0",
                    "createdDate": "",
                    "disableDeployment": false,
                    "enable": true,
                    "name": "",
                    "nlbVersion": "1.0",
                    "numOfInstances": "2",
                    "resize": false,
                    "state": "enabled",
                    "status": "healthy",
                    "vlanID": "3249704",
                    "zone": "dal10"
                }
            ],
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback

from ..module_utils.sdk.container.cluster import Cluster
from ..module_utils.auth import Authenticator


def run_module():
    module_args = dict(
        name=dict(
            required=True,
            type='str'),
        alb_type=dict(
            required=False,
            type='str'),
        resource_group_id=dict(
            required=False,
            type='str'),
        # iam_token=dict(
        #     required=True,
        #     type='str'),
        list_bounded_services=dict(
            required=False,
            type='str'),
        ibmcloud_api_key=dict(
            type='str',
            no_log=True,
            fallback=(env_fallback, ['IC_API_KEY']),
            required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    name = module.params["name"]
    alb_type = module.params["alb_type"]
    resource_group_id = module.params["resource_group_id"]
    list_bounded_services = module.params["list_bounded_services"]
    ibmcloud_api_key = module.params["ibmcloud_api_key"]


    sdk = Cluster(
        cluster_id=name,
    )

    authenticator = Authenticator(
        api_key=ibmcloud_api_key,
    )

    module.params["iam_token"] = authenticator.get_iam_token()

    # List baisc info a cluster.
    is_error, has_changed, cluster_info = sdk.basic_cluster_info(module.params)

    # List all the worker pools that you have in a cluster.
    is_error, has_changed, pools = sdk.list_worker_pools(module.params)

    # List all worker nodes of a cluster
    is_error, has_changed, nodes = sdk.list_worker_nodes(module.params)

    # List all ALBs in a cluster
    is_error, has_changed, albs = sdk.list_albs(module.params)

    # List the IBM Cloud services that are bound in any Kubernetes namespace in the cluster.
    is_error, has_changed, services = sdk.bounded_services(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, cluster_info=cluster_info, worker_pools=pools, worker_nodes=nodes, ingress_albs=albs, list_bounded_services=services)
    else:
        module.fail_json(msg="Error listing cluster info", meta=result)


def main():
    run_module()


if __name__ == '__main__':
    main()