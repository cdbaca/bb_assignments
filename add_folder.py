import requests
import json
from requests.packages import urllib3
import get_token, db_connect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cur = None
conn = None

def course_list():
    query = '''
                select distinct
                cm.course_id
                from course_main cm
	                inner join course_term ct on ct.crsmain_pk1 = cm.pk1
	                inner join term t on t.pk1 = ct.term_pk1
                where t.name like '%[ENTER TERM HERE]%'
                    and t.name similar to '%(Distance|SOM|Online|Rhema|Doctoral|Graduate Distance|Session)%'
	                and cm.pk1 not in (select crsmain_pk1 from course_course)'''

    course_list = []

    cur = db_connect.connect()

    cur.execute(query)
    print("List of courses that will have folder added:")
    for record in cur.fetchall():
        print(record)

    print("--------------------------")
    answer = input("Do you want to add a new folder to these courses? y/n ")

    if answer == 'y':
        cur.execute(query)
        for record in cur.fetchall():
            print("Appending to list: {0}".format(record))
            course_list.append(record)
    elif answer == 'n':
        pass
    else:
        print("Not a valid answer, no folders will be added.")

    return (course_list)

def main():
    # create data folder if not created and get auth token
    get_token.data_folder()
    auth_token = get_token.store_token()

    # create list of courses tuples with courses to add folder to
    course_ids = course_list()
    print(course_ids)

    # get folder name
    folder_name = input("What do you want to title the folder being created? ")

    # folder data
    j = """{{
      "title": "{0}",
      "body": "",
      "description": "",
      "position": 4,
      "launchInNewWindow": false,
      "reviewable": true,
      "availability": {{
        "available": "Yes",
        "allowGuests": true,
        "allowObservers": true,
        "adaptiveRelease": {{
          "start": "2022-08-29T06:00:00.000Z",
          "end": "2022-12-09T05:59:59.080Z"
        }}
      }},
      "contentHandler": {{"id":"resource/x-bb-folder"}}
    }}""".format(folder_name)
    j = json.loads(j)

    # API Endpoints / string variables
    base_url = 'blackboard.sagu.edu'
    assign_path_one = '/learn/api/public/v1/courses/courseId:'
    assign_path_two = '/contents'

    # add folder to courses in course_ids tuples list
    session = requests.session()
    for record in course_ids:
        for course in record:
            r = session.post('https://' + base_url + assign_path_one + course + assign_path_two,
                 data=json.dumps(j),
                 headers={'Authorization':auth_token, 'Content-Type':'application/json'},
                 verify=False
                 )
            print(f"Status Code: {r.status_code}, Response: {r.json()}")

if __name__ == '__main__':
    main()

if cur is not None:
     cur.close()
if conn is not None:
     conn.close()