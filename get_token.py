import requests
import json
from requests.packages import urllib3
import credentials
import os
import time


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base variables/urls

key = credentials.key
secret = credentials.secret
payload = {
            'grant_type':'client_credentials'
        }

# API endpoints
base_url = 'https://blackboard.sagu.edu'
oauth_path = '/learn/api/public/v1/oauth2/token'

max_age = 60*60
token_path = os.path.join(
    'data',
    'bb.token'
)
# Function to authorize script and get access token

def store_token():
    auth_token = None

    if os.path.isfile(token_path):
        token_age = time.time() - os.path.getmtime(token_path)

        if token_age < max_age:
            with open(token_path, 'r') as infile:
                auth_token = infile.read()

    if not auth_token:
        session = requests.session()
        r = session.post(base_url + oauth_path, data=payload, auth=(key, secret), verify=False)
        print("[auth:setToken()] STATUS CODE: " + str(r.status_code))
        res = json.loads(r.text)
        print("[auth:setToken()] RESPONSE: \n" + json.dumps(res, indent=4, separators=(',', ': ')))
        token = res['access_token']
        auth_token = 'Bearer ' + token

        with open(token_path, 'w') as outfile:
            outfile.write(auth_token)

    return(auth_token)

def data_folder():
    path = '../data'

    if not os.path.exists(path):
        os.makedirs(path)