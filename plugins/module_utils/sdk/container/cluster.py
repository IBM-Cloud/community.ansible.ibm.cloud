# coding: utf-8

# Copyright 2019 IBM All Rights Reserved.
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
import traceback

try:
    import requests
except ImportError:
    HAS_ANOTHER_LIBRARY = False
    ANOTHER_LIBRARY_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_ANOTHER_LIBRARY = True


class Cluster:
    """Cluster class to support following functionalities.
        * basic_cluster_info
        * list_worker_nodes
        * list_worker_pools
        * list_albs
        * bounded_services
    """
    # Class Variable
    DEFAULT_SERVICE_URL = 'https://containers.cloud.ibm.com/global/'

    # The init method or constructor
    def __init__(self, cluster_id):

        # Instance Variable
        self.cluster_id = cluster_id

    # Method to fetch error code based on status code
    def get_status(self, status_code):
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

    # Method to get the list of worker nodes from cluster
    def basic_cluster_info(self, data):
        headers = {"Authorization": data['iam_token']}
        TARGET_URL = ('/v1/clusters/{0}'.format(data['name']))
        response = requests.get(
            Cluster.DEFAULT_SERVICE_URL + TARGET_URL,
            headers=headers
        )

        if response.status_code == 200 or response.status_code == 204:
            return False, True, response.json()
        elif response.status_code == 401:
            return False, False, response.json()
        elif response.status_code == 404:
            return False, False, response.json()
        elif response.status_code == 500:
            return False, False, response.json()
        else:
            return False, False, response.json()

    # Method to get the list of worker nodes from cluster
    def list_worker_nodes(self, data):
        headers = {"Authorization": data['iam_token']}
        TARGET_URL = ('v1/clusters/{0}/workers'.format(data['name']))
        response = requests.get(
            Cluster.DEFAULT_SERVICE_URL + TARGET_URL,
            headers=headers
        )

        if response.status_code == 200 or response.status_code == 204:
            return False, True, response.json()
        elif response.status_code == 401:
            return False, False, response.json()
        elif response.status_code == 404:
            return False, False, response.json()
        elif response.status_code == 500:
            return False, False, response.json()
        else:
            return False, False, response.json()

    # Method to get the list of worker pools from cluster
    def list_worker_pools(self, data):
        headers = {"Authorization": data['iam_token']}
        TARGET_URL = ('/v1/clusters/{0}/workerpools'.format(data['name']))
        response = requests.get(
            Cluster.DEFAULT_SERVICE_URL + TARGET_URL,
            headers=headers
        )

        if response.status_code == 200 or response.status_code == 204:
            return False, True, response.json()
        elif response.status_code == 401:
            return False, False, response.json()
        elif response.status_code == 404:
            return False, False, response.json()
        elif response.status_code == 500:
            return False, False, response.json()
        else:
            return False, False, response.json()

    # List all ALBs in a cluster.
    def list_albs(self, data):
        headers = {"Authorization": data['iam_token']}
        TARGET_URL = ('/v1/alb/clusters/{0}'.format(data['name']))
        response = requests.get(
            Cluster.DEFAULT_SERVICE_URL + TARGET_URL,
            headers=headers
        )

        if response.status_code == 200 or response.status_code == 204:
            return False, True, response.json()
        elif response.status_code == 401:
            return False, False, response.json()
        elif response.status_code == 404:
            return False, False, response.json()
        elif response.status_code == 500:
            return False, False, response.json()
        else:
            return False, False, response.json()

    # List the IBM Cloud services bound to a cluster across all namespaces.
    def bounded_services(self, data):
        headers = {"Authorization": data['iam_token']}
        TARGET_URL = ('/v1/clusters/{0}/services'.format(data['name']))
        response = requests.get(
            Cluster.DEFAULT_SERVICE_URL + TARGET_URL,
            headers=headers
        )

        if response.status_code == 200 or response.status_code == 204:
            return False, True, response.json()
        elif response.status_code == 401:
            return False, False, response.json()
        elif response.status_code == 404:
            return False, False, response.json()
        elif response.status_code == 500:
            return False, False, response.json()
        else:
            return False, False, response.json()
