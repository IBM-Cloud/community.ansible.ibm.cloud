#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Copyright IBM Corp. 2022.
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: ibm_container_cluster_worker
author: Janardhana Anipireddy (@areddy548)
version_added: "1.0.0"
short_description: return the  IKS cluster worker resource
requirements: []
description:
    -- Retrieve an IBM Cloud 'ibm_container_cluster_worker' resource .
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
    api_command:
        description:
            - command for the worker update
        required: True
        type: dict
        suboptions:
            action:
                description:
                    - The action to perform on the worker node.
                required: True
                type: str
                choices:
                    - os_reboot
                    - reload
                    - update
            force:
                description:
                    -   Setting force flag to true will ignore if the master is unavailable during 'os_reboot" and 'reload' action
                required: True
                type : bool
'''


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


EXAMPLES = r'''
# reload the worker node of a cluster
- ibm_container_cluster_worker:
    name: "{{ name }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    worker_id: "{{ worker_id }}"
    api_command:
        action: "reload"
        force: true

# reboot the worker node of a cluster
- ibm_container_cluster_worker:
    name: "{{ name }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    resource_group_id: "{{ resource_group_id }}"
    worker_id: "{{ worker_id }}"
    api_command:
        action: "os_reboot"
        force: true

# update the worker node of a cluster
- ibm_container_cluster_worker:
    name: "{{ name }}"
    ibmcloud_api_key: "{{ ibmcloud_api_key }}"
    resource_group_id: "{{ resource_group_id }}"
    worker_id: "{{ worker_id }}"
    api_command:
        action: "update"
        force: true

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
            required=True),
        api_command=dict(
            type='dict',
            required=True,
            options=dict(
                action=dict(
                    type='str',
                    choices=['os_reboot', 'reload', 'update'],
                    required=True
                ),
                force=dict(
                    type='bool',
                    required=True
                ),
            ),
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    name = module.params["name"]
    resource_group_id = module.params["resource_group_id"]
    worker_id = module.params["worker_id"]
    ibmcloud_api_key = module.params["ibmcloud_api_key"]
    api_command = module.params["api_command"]

    sdk = Worker(
        cluster_id=name,
        worker_id=worker_id
    )

    authenticator = Authenticator(
        api_key=ibmcloud_api_key,
    )

    module.params["iam_token"] = authenticator.get_iam_token()

    # update cluster worker node.
    is_error, has_changed, worker_reload_response = sdk.update_worker_node(
        module.params)
    if not is_error:
        module.exit_json(
            changed=has_changed,
            worker_reload_response=worker_reload_response)
    else:
        module.fail_json(
            msg="Error listing worker info",
            meta=worker_reload_response)


def main():
    run_module()


if __name__ == '__main__':
    main()
