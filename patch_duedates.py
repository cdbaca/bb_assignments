import requests
from requests.packages import urllib3
import get_token, db_connect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
conn = None
cur = None

# API Endpoints / string variables
base_url = 'blackboard.sagu.edu'
assign_path_one = '/learn/api/public/v2/courses/courseId:'
assign_path_two = '/gradebook/columns'

def get_gradeID():
    term_wildcard = input('Enter a term wildcard for the query: ')
    content_wildcard = input('Enter a content title wildcard for the query: ')

    query = '''
            select
            cm.course_id
            ,gm.title
            ,concat('_',gm.pk1,'_1')
            from course_main cm
                inner join gradebook_main gm on gm.crsmain_pk1 = cm.pk1
                inner join course_term ct on ct.crsmain_pk1 = cm.pk1
                inner join term t on t.pk1 = ct.term_pk1
            where t.name like '%{0}%'
                and t.name not like '%Session%'
                and gm.title like '%{1}%'
                and course_contents_pk1 is not null
            order by course_id, title
            '''.format(term_wildcard, content_wildcard)

    cur = db_connect.connect()

    content_list = []

    cur.execute(query)
    print("List of content to update due dates: ")
    print("*************************************")
    for record in cur.fetchall():
        print(record)

    print("--------------------------")
    answer = input("Do you want to update due dates for this content from these courses? y/n ")

    if answer == 'y':
        cur.execute(query)
        for record in cur.fetchall():
            print("Appending to list: {0}".format(record))
            content_list.append(record)
    elif answer == 'n':
        pass
    else:
        print("Not a valid answer, no content will be deleted.")

    return(content_list)

def main():
    get_token.data_folder()
    auth_token = get_token.store_token()

    content_list = get_gradeID()

    session = requests.session()

    j = """
    {"grading": {"due": "2022-05-28T04:59:00.000Z"}}
    """

    for record in content_list:
        if record[1] is not None:
            print("Updating due date of {0} from {1}".format(record[1], record[0]))
            print("API Endpoint: ", 'https://' + base_url + assign_path_one + record[0] + assign_path_two + '/' + record[2])
            r = session.patch('https://' + base_url + assign_path_one + record[0] + assign_path_two + '/' + record[2],
                         data = j,
                         headers={'Authorization': auth_token, 'Content-Type': 'application/json'},
                         verify=False
                         )

            if r.status_code == 200:
                print("Successfully updated {0} from {1}".format(record[1], record[0]))
                print("--------------")
            else:
                print("Could not update {0}".format(record[0]))
                print(f"Status Code: {r.status_code}")
                print(r.text)
                print("--------------")
        else:
            print("{0} did not have content to update.".format(record[0]))
            print("--------------")

if __name__ == '__main__':
    main()