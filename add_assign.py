import requests
import json
from requests.packages import urllib3
import get_token, db_connect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cur = None
conn = None

# API Endpoints / string variables

base_url = 'blackboard.sagu.edu'
assign_path_one = '/learn/api/public/v1/courses/courseId:'
course_id = 'grade_test_course'
assign_path_two = '/contents/createAssignment'

# Function for finding courses and folders to add assignments to
def folder_list():
    term_wildcard = input("What course or group of courses do you want to work with? (e.g., FA22, SP22, etc.) ")
    folder_label = input("What folder in this course or these courses do you want to put the assignment in? ")

    query = """select
            cm.pk1
            ,toc.label
            ,toc.contentId
            ,cm.course_id
            ,t.name as term
            from course_main cm
                inner join course_term ct on ct.crsmain_pk1 = cm.pk1
                inner join term t on t.pk1 = ct.term_pk1
                left join (
                            select
                            toc.crsmain_pk1
                            ,concat('_',toc.course_contents_pk1,'_1') as contentId
                            ,toc.label
                            from course_toc toc
                            where toc.label like '%{0}%' 
                            ) toc on toc.crsmain_pk1 = cm.pk1
            where cm.course_id like '%{1}%'
                and cm.pk1 not in (select crsmain_pk1 from course_course)
				--and t.name similar to '%(Distance|Dual|Online|Extension)%'
				and t.name in (
				                    --'Fall 2022 SAGU at Rhema (A Session) Undergraduate Distance Education',
								   'Fall 2022 SAGU at Rhema (B Session) Undergraduate Distance Education'
								   ,'Fall 2022 Graduate Distance Education B Session Classes'
								   ,'Fall 2022 Undergraduate Online B Sessions'
								   --,'Fall 2022 Undergraduate Online A Sessions'
								   --,'Fall 2022 Graduate Distance Education A Session Classes'
								  	)
            order by cm.course_id""".format(folder_label, term_wildcard)

    folder_list = []

    cur = db_connect.connect()

    cur.execute(query)
    print("List of courses with folder that will have assignment added:")
    for record in cur.fetchall():
        print(record)

    print("--------------------------")
    answer = input("Do you want to add a new assignment to these courses? y/n ")

    if answer == 'y':
        cur.execute(query)
        for record in cur.fetchall():
            print("Appending to list: {0}".format(record))
            folder_list.append(record)
    elif answer == 'n':
        pass
    else:
        print("Not a valid answer, no folders will be added.")

    return (folder_list)

def main():
    # create data folder if not created and get auth token
    # TODO: if token is invalid but .token file was created less than one hour ago, auth_token may not work. Need to check auth_token status.
    get_token.data_folder()
    auth_token = get_token.store_token()

    # get folder/course list to add course
    folders_and_courses = folder_list()

    # get name of assignment
    assignment_name = input("What do you want to name the assignment? (case-sensitive) ")

    # add assignments to folders
    session = requests.session()
    for record in folders_and_courses:
        # assignment json
        j = """{{"parentId": "{0}",
            "title": "{1}",
            "instructions": "<h4>Test Instructions for the Assignment</h4>",
            "description": "test description",
            "position": 0,
            "availability":
                {{"available": "Yes",
                "allowGuests": true,
                "adaptiveRelease":
                    {{"start": "2022-10-24T05:00:00.000Z",
                    "end": "2022-11-14T05:59:59.080Z"}}
                }},
            "grading":
                {{"due": "2022-11-11T05:59:59.000Z",
                "attemptsAllowed": 0,
                "isUnlimitedAttemptsAllowed": true}},
            "score": {{"possible": 5}}
            }}""".format(record[2], assignment_name)

        # add assignment via API
        r = session.post('https://' + base_url + assign_path_one + record[3] + assign_path_two,
                     data=j,
                     headers={'Authorization':auth_token, 'Content-Type':'application/json'},
                     verify=False
                    )
        if r.status_code == 201:
            print(f"Status Code: {r.status_code}, {assignment_name} successfully added to {record[3]}!")
        else:
            print(f"Status Code: {r.status_code}: assignment was not added :(")

if __name__ == '__main__':
    main()

if cur is not None:
    cur.close()
if conn is not None:
    conn.close()