import requests
from requests.packages import urllib3
import get_token, db_connect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
conn = None
cur = None

# API Endpoints / string variables
base_url = 'blackboard.sagu.edu'
assign_path_one = '/learn/api/public/v1/courses/courseId:'
assign_path_two = '/contents'

def get_contentIDs():
    term_wildcard = input('Enter a course_id wildcard for the query: ')
    content_wildcard = input('Enter a content title wildcard for the query: ')

    query = '''select
                        cm.pk1 as course_pk
                        ,cc.title
                        ,cc.parentId
                        ,course_id
                        ,t.name
                        from course_main cm
                            inner join course_term ct on ct.crsmain_pk1 = cm.pk1
                            inner join term t on t.pk1 = ct.term_pk1
                            left join (
                                        select
                                        crsmain_pk1
                                        ,concat('_', cc.pk1, '_1') as parentId
                                        ,cc.title
                                        from course_contents cc
                                        where
                                            cc.title like '%{0}%'
                                            and cc.title not like '%Zoom Meeting%'
                            ) cc on cc.crsmain_pk1 = cm.pk1
                        where cm.course_id like '%{1}%'
                            and cm.pk1 not in (select crsmain_pk1 from course_course)
                        order by cm.course_id'''.format(content_wildcard, term_wildcard)

    # query = '''
    # select
    #                     cm.pk1 as course_pk
    #                     ,toc.label
    #                     ,toc.parentId
    #                     ,course_id
    #                     ,t.name
    #                     from course_main cm
    #                         inner join course_term ct on ct.crsmain_pk1 = cm.pk1
    #                         inner join term t on t.pk1 = ct.term_pk1
    #                         left join (
    #                                     select
    #                                     crsmain_pk1
    #                                     ,concat('_', toc.pk1, '_1') as parentId
    #                                     ,toc.label
    #                                     from course_toc toc
    #                                     where
    #                                         toc.label = '{0}'
    #                         ) toc on toc.crsmain_pk1 = cm.pk1
    #                     where cm.course_id like '%{1}%'
    #                         and cm.pk1 not in (select crsmain_pk1 from course_course)
	# 						and toc.label is not null
    #                     order by cm.course_id
    # '''.format(content_wildcard, term_wildcard)

    cur = db_connect.connect()

    content_list = []

    cur.execute(query)
    print("List of content to be deleted:")
    for record in cur.fetchall():
        print(record)

    print("--------------------------")
    answer = input("Do you want to delete this content from these courses (if title/id is None, nothing will be deleted)? y/n ")

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

    content_list = get_contentIDs()

    session = requests.session()

    for record in content_list:
        if record[1] is not None:
            print("Deleting {0} from {1}".format(record[1], record[3]))
            print("API Endpoint: ", 'https://' + base_url + assign_path_one + record[3] + assign_path_two + '/' + record[2])
            r = session.delete('https://' + base_url + assign_path_one + record[3] + assign_path_two + '/' + record[2],
                         headers={'Authorization': auth_token, 'Content-Type': 'application/json'},
                         verify=False
                         )

            if r.status_code == 204:
                print("Successfully deleted {0} from {1}".format(record[1], record[3]))
                print("--------------")
            else:
                print("Could not delete content from {0}".format(record[3]))
                print(f"Status Code: {r.status_code}")
                print("--------------")
        else:
            print("{0} did not have content to delete.".format(record[3]))
            print("--------------")

if __name__ == '__main__':
    main()

if cur is not None:
     cur.close()
if conn is not None:
     conn.close()