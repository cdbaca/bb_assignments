import requests
import json
from requests.packages import urllib3
import credentials
import get_token

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

def main():

    get_token.data_folder()

    # TO DO: find courses that need to be appended to list below
    course_ids = ['grade_test_course']

    auth_token = get_token.store_token()
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

    session = requests.session()

    for course in course_ids:
        r = session.post('https://' + base_url + assign_path_one + course + assign_path_two,
                data=json.dumps(j),
                 headers={'Authorization':auth_token, 'Content-Type':'application/json'},
                 verify=False
             )
        print(f"Status Code: {r.status_code}, Response: {r.json()}")

if __name__ == '__main__':
    main()





