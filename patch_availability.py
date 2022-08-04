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
assign_path_two = '/contents/'

def course_list():
    term_wildcard = input("Enter term wildcard: ")
    content_wildcard = input("What assignment do you want to change availability for? ")

    query = '''
                select
                cm.course_id
                ,cc.title
                ,concat('_',cc.pk1,'_1')
                ,cc.start_date
                ,cc.end_date
                from course_main cm
                    inner join course_contents cc on cc.crsmain_pk1 = cm.pk1
                    inner join course_term ct on ct.crsmain_pk1 = cm.pk1
                    inner join term t on t.pk1 = ct.term_pk1
                where t.name like '%{0}%'
                    and t.name not like '%Session%'
                    and cc.title like '%{1}%'
                    and cm.pk1 not in (select crsmain_pk1 from course_course)
                order by course_id'''.format(term_wildcard, content_wildcard)

    course_list = []

    cur = db_connect.connect()

    cur.execute(query)
    print("List of assignments in courses that you will change dates for:")
    for record in cur.fetchall():
        print(record)

    print("--------------------------")
    answer = input("Do you want to change availability dates for these assignments? y/n ")

    if answer == 'y':
        cur.execute(query)
        for record in cur.fetchall():
            print("Appending to list: {0}".format(record))
            course_list.append(record)
    elif answer == 'n':
        pass
    else:
        print("Not a valid answer, no assignments will be changed.")

    return (course_list)

def main():
    # create data folder if not created and get auth token
    get_token.data_folder()
    auth_token = get_token.store_token()

    # create list of courses tuples with courses to add folder to
    course_ids = course_list()
    print(course_ids)

    # get folder name

    # content data
    j = """{"availability": {"adaptiveRelease": {"start": "2022-05-30T06:00:00.000Z","end": "2022-06-18T05:59:59.080Z"}}}"""

    # change dates for assignments in course_ids tuples list
    session = requests.session()
    for record in course_ids:
        r = session.patch('https://' + base_url + assign_path_one + record[0] + assign_path_two + record[2],
                 data=j,
                 headers={'Authorization':auth_token, 'Content-Type':'application/json'},
                 verify=False
                 )
        print(f"Status Code: {r.status_code}, Response:", r.text)

if __name__ == '__main__':
    main()

if cur is not None:
     cur.close()
if conn is not None:
     conn.close()

# """
# curl --request POST "https://api.viafoura.com/v2/dev.viafoura.com/users/login?password=TeNn!sNum8er1&email=novak@example.com"
# curl --data '{"availability": {"adaptiveRelease": {"start": "2022-05-09T06:00:00.000Z","end": "2022-05-31T05:59:59.080Z"}}}'
#     -X PATCH https://blackboard.sagu.edu//learn/api/public/v1/courses/courseId:{0}/contents/{1}
# """