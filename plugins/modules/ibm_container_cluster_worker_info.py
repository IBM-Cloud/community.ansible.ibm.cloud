#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Copyright IBM Corp. 2022.
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: ibm_container_cluster_worker_info
author: Janardhana Anipireddy (@areddy548)
version_added: "1.0.0"
short_description: Retrieve IBM Cloud 'ibm_container_cluster_worker_info' resource
requirements: []
description:
    -- Retrieve an IBM Cloud 'ibm_container_cluster_worker_info' resource .
options:
    name:
        required: True
        type: str
        default: null
        description:
            - Name or ID of the IKS cluster.
    resource_group_id:
        description:
            - ID of the resource group.
        required: False
        type: str
    worker_id:
        description:
            - ID of the worker
        required: True
        type: str
    ibmcloud_api_key:
        description:
            - The IBM Cloud API key to authenticate with the IBM Cloud
              platform. This can also be provided via the environment
              variable 'IC_API_KEY'.
        required: True
        type: str
'''

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

EXAMPLES = r'''
# Target the worker of cluster which is present in default resource group
- ibm_container_cluster_worker_info:
    name: "{{ name }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    worker_id: "{{ worker_id }}"

# Target the worker of cluster which is present in a particular resource group
- ibm_container_cluster_worker_info:
    name: "{{ name }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    resource_group_id: "{{ resource_group_id }}"
    worker_id: "{{ worker_id }}"

# Target the worker of cluster by name
- ibm_container_cluster_worker_info:
    name: "{{ name }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    resource_group_id: "{{ resource_group_id }}"
    worker_id: "{{ worker_id }}"

# Target the worker of cluster by ID
- ibm_container_cluster_worker_info:
    name: "{{ cluster_id }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    resource_group_id: "{{ resource_group_id }}"
    worker_id: "{{ worker_id }}"
'''

from ansible.module_utils.basic import env_fallback
from ansible.module_utils.basic import AnsibleModule
from ..module_utils.sdk.container.worker import Worker
from ..module_utils.auth import Authenticator


def run_module():
    module_args = dict(
        name=dict(
            required=True,
            type='str'),
        resource_group_id=dict(
            required=False,
            type='str'),
        worker_id=dict(
            required=True,
            type='str'),
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
    resource_group_id = module.params["resource_group_id"]
    worker_id = module.params["worker_id"]
    ibmcloud_api_key = module.params["ibmcloud_api_key"]

    sdk = Worker(
        cluster_id=name,
        worker_id=worker_id
    )

    authenticator = Authenticator(
        api_key=ibmcloud_api_key,
    )

    module.params["iam_token"] = authenticator.get_iam_token()

    # List baisc info a cluster worker.
    is_error, has_changed, worker_info = sdk.basic_worker_info(module.params)

    try:
        if not is_error:
            raise Exception('Error listing worker info')
        module.exit_json(changed=has_changed, worker_info=worker_info)
    except Exception as ex:
        module.fail_json(msg=ex)


def main():
    run_module()


if __name__ == '__main__':
    main()
