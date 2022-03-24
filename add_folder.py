import requests
import json
from requests.packages import urllib3
import get_token

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API Endpoints / string variables
base_url = 'blackboard.sagu.edu'
assign_path_one = '/learn/api/public/v1/courses/courseId:'
course_id = 'grade_test_course'
assign_path_two = '/contents'

# TODO: write function that will append course_ids to course_ids list
# def course_list():
    # yada yada yada


def main():
    # TODO: add course_list function here
    # course_ids = course_list()
    course_ids = ['grade_test_course']

    # create folder and get token
    get_token.data_folder()
    auth_token = get_token.store_token()

    # folder data
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

    # add folder to courses in course_ids list
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