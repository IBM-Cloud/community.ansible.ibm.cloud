#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Copyright IBM Corp. 2022.
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

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
author: Umar Ali (@umarali-nagoor)
version_added: "1.0.0"
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
        choices: [ "public", "private", "all"]
        description:
            - Type of ALBs to fetch

    list_bounded_services:
        required: False
        type: bool
        default: null
        description:
            - Mention whether to list down the bounded services or not

    ibmcloud_api_key:
        description:
            - The IBM Cloud API key to authenticate with the IBM Cloud
              platform. This can also be provided via the environment
              variable 'IC_API_KEY'.
        required: True
        type: str

    resource_group_id:
        required: False
        type: str
        description:
            - ID of the resource group that the cluster is in. To check the resource group ID of the cluster, use the GET /v1/clusters/idOrName API.
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
- ibm_container_cluster_info:
    name: "{{ cluster_id }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    resource_group_id: "{{ resource_group_id }}"
    alb_type: "{{ alb_type }}"
    iam_token : "{{ IC_IAM_TOKEN }}"
    list_bounded_services: "{{ list_bounded_services }}"
'''

from ..module_utils.auth import Authenticator
from ..module_utils.sdk.container.cluster import Cluster
from ansible.module_utils.basic import env_fallback
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        name=dict(
            required=True,
            type='str'),
        alb_type=dict(
            required=False,
            choices=["public", "private", "all"],
            type='str'),
        resource_group_id=dict(
            required=False,
            type='str'),
        # iam_token=dict(
        #     required=True,
        #     type='str'),
        list_bounded_services=dict(
            required=False,
            type='bool'),
        ibmcloud_api_key=dict(
            type='str',
            no_log=True,
            fallback=(env_fallback, ['IC_API_KEY']),
            required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
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

    # List the IBM Cloud services that are bound in any Kubernetes namespace
    # in the cluster.
    is_error, has_changed, services = sdk.bounded_services(module.params)

    if not is_error:
        module.exit_json(
            changed=has_changed,
            cluster_info=cluster_info,
            worker_pools=pools,
            worker_nodes=nodes,
            ingress_albs=albs,
            list_bounded_services=services)
    else:
        module.fail_json(msg="Error listing cluster info", meta=services)


def main():
    run_module()


if __name__ == '__main__':
    main()
