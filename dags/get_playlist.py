#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import json
import requests
import base64
import datetime

from airflow.decorators import dag, task
from airflow.models import Variable

API_KEY = Variable.get("AIRFLOW_VAR_API_KEY")
API_SECRET = Variable.get("AIRFLOW_VAR_API_SECRET")
base_url = 'https://api.spotify.com/v1/'
user_id = 'vasco_lopo'

@dag(
    schedule_interval=None,
    start_date=datetime.datetime(2021, 1, 1),
    catchup=False,
    tags=['authenticate', 'ETL'],
)
def ingest_data_into_postgres():

    @task()
    def get_token():
        url = "https://accounts.spotify.com/api/token"

        to_encode_secrets = API_KEY + ':' + API_SECRET
        byte_data = to_encode_secrets.encode('utf-8')
        encoded_data = str(base64.b64encode(byte_data), 'utf-8')
        form = {
            "grant_type": "client_credentials"
        }

        headers = {
            "Authorization": "Basic " + encoded_data,
            "Content-Type" : "application/x-www-form-urlencoded"
        }

        r = requests.post(url, headers=headers, data = form)

        json_result = json.loads(r.content)
        token = json_result["access_token"]

        return token

    @task()
    def get_playlist(headers, base_url, user_id):
        """
        Gets playlist information from specific user
        """
        endpoint = base_url + 'users/' + user_id + '/playlists'
        r = requests.get(endpoint, headers=headers)

        r = r.json()

        return {"request to playlist API": r}

    token = get_token()
    print("successfully grabbed access token")
    headers = {
    'Authorization': 'Bearer {token}'.format(token = token)
    }
    token = get_playlist(headers, base_url, user_id)

tutorial_etl_dag = ingest_data_into_postgres()
