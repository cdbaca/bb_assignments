import requests
import json
from requests.packages import urllib3
import get_token, db_connect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cur = None
conn = None

def user_list():
    course_id = input("What course do you want to disable enrollments from? ")
    
    query = '''
                select
                u.user_id
                from course_users cu
                    inner join course_main cm on cm.pk1 = cu.crsmain_pk1
                    inner join users u on u.pk1 = cu.users_pk1
                where cm.course_id = '{0}'
                    and cu.role = 'S'
                    '''.format(course_id)

    user_list = []

    cur = db_connect.connect()

    cur.execute(query)
    print("List of users that will be disabled folder added:")
    for record in cur.fetchall():
        print(record)

    print("--------------------------")
    answer = input("Do you want to disable these users ? y/n ")

    if answer == 'y':
        cur.execute(query)
        for record in cur.fetchall():
            print("Appending to list: {0}".format(record))
            user_list.append(record)
    elif answer == 'n':
        pass
    else:
        print("Not a valid answer, no folders will be added.")

    return (user_list, course_id)




def main():
    # create data folder if not created and get auth token
    get_token.data_folder()
    auth_token = get_token.store_token()

    # create list of courses tuples with courses to add folder to
    # course_id = input("What course code do you want to delete the enrollment from? ")

    user_ids, course_id = user_list()
    # print(course_ids)

    # get folder name
    # student_id = input("What students do you want removed from the course? ")
    # folder_name = input("What do you want to title the folder being created? ")

    # folder data
    j = """{"availability": 
            {
            "available": "No"
            }
            }"""
    j = json.loads(j)

    # API Endpoints / string variables
    base_url = 'blackboard.sagu.edu'
    assign_path_one = '/learn/api/public/v1/courses/courseId:'
    assign_path_two = '/users/'
    # print('https://' + base_url + assign_path_one + course_id + assign_path_two + student_id)
    # add folder to courses in course_ids tuples list
    session = requests.session()
    for record in user_ids:
        for user in record:
            # print(user)
            # print('https://' + base_url + assign_path_one + course_id + assign_path_two + 'userName:' + user)
            r = session.delete('https://' + base_url + assign_path_one + course_id + assign_path_two + 'userName:' + user,
                    #data=json.dumps(j),
                    headers={'Authorization':auth_token, 'Content-Type':'application/json'},
                    verify=False
                    )
            print(f"Status Code: {r.status_code}") 
            #, Response: {r.json()}")

if __name__ == '__main__':
    main()

if cur is not None:
     cur.close()
if conn is not None:
     conn.close()