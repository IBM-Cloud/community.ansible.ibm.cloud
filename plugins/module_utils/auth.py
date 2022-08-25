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

import os
import requests

class Authenticator:
    """
    Use this class to generate IAM TOKEN from API KEY
    """
    # Class Variable
    DEFAULT_SERVICE_URL = 'https://iam.cloud.ibm.com/identity/token'
 
    # The init method or constructor
    def __init__(self, api_key):
 
        # Instance Variable
        self.api_key = api_key
        if api_key == '':
            api_key = os.getenv('IC_API_KEY')
            self.api_key = api_key

    # get_iam_token use to fetch IAM TOKEN using API KEY
    def get_iam_token(self):

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey='+self.api_key

        response = requests.post(
                            Authenticator.DEFAULT_SERVICE_URL,
                            headers=headers,
                            data=data
                        )
        return response.json()['access_token']