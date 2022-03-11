import requests
import json
from requests.packages import urllib3
import credentials

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base variables/urls

key = credentials.key
secret = credentials.secret
payload = {
            'grant_type':'client_credentials'
        }
base_url = 'blackboard.sagu.edu'

# API Endpoints / string variables

assign_path_one = '/learn/api/public/v1/courses/courseId:'
course_id = 'grade_test_course'
assign_path_two = '/contents'
oauth_path = '/learn/api/public/v1/oauth2/token'

# Authorize script and get access token

session = requests.session()
r = session.post('https://'+ base_url + oauth_path, data=payload, auth=(key, secret), verify=False)
print("[auth:setToken()] STATUS CODE: " + str(r.status_code))
res = json.loads(r.text)
print("[auth:setToken()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))

token = res['access_token']
authStr = 'Bearer ' + token

# TO DO: check if token expired and get new token if necessary



# open json file produced from get_data.py, use keys as course_id, use value as json string input for API

j = """{
  "title": "Formative Assessments",
  "body": "<h1>Formative Assessments are located here</h1>",
  "description": "testing adding folders",
  "position": 4,
  "launchInNewWindow": false,
  "reviewable": true,
  "availability": {
    "available": "Yes",
    "allowGuests": true,
    "allowObservers": true,
    "adaptiveRelease": {
      "start": "2022-02-15T20:40:31.080Z",
      "end": "2022-02-17T20:40:31.080Z"
    }
  },
  "contentHandler": {"id":"resource/x-bb-folder"}
}"""

j = json.loads(j)

# with open("data/bb_course_data.json", "r") as read_file:
#     bb_data = json.load(read_file)

course_ids = ['grade_test_course']

for course in course_ids:
    r = session.post('https://' + base_url + assign_path_one + course + assign_path_two,
                data=json.dumps(j),
                 headers={'Authorization':authStr, 'Content-Type':'application/json'},
                 verify=False
             )
    print(f"Status Code: {r.status_code}, Response: {r.json()}")





