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
assign_path_two = '/contents/createAssignment'
oauth_path = '/learn/api/public/v1/oauth2/token'

# Authorize script and get access token

session = requests.session()
r = session.post('https://'+ base_url + oauth_path, data=payload, auth=(key, secret), verify=False)
print("[auth:setToken()] STATUS CODE: " + str(r.status_code))
res = json.loads(r.text)
print("[auth:setToken()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))

token = res['access_token']
authStr = 'Bearer ' + token

# Query for finding Formative Assessment (changing to Learning Assessment) folders... or whatever other folders
# TODO: use db_connect.py to connect to database and find folders to add the assignment to

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
                        where toc.label like '%Formative Assessment%' 
                        ) toc on toc.crsmain_pk1 = cm.pk1
        where cm.course_id like '%dummy%'
            and cm.pk1 not in (select crsmain_pk1 from course_course)
        order by cm.course_id"""


# open json file produced from get_data.py, use keys as course_id, use value as json string input for API
# TODO: change the json here, or add json directly to script
with open("data/bb_course_data.json", "r") as read_file:
    bb_data = json.load(read_file)

for k,v in bb_data.items():
    course_id = k
    course_specific_data = v
    r = session.post('https://' + base_url + assign_path_one + course_id + assign_path_two,
                 data=json.dumps(course_specific_data),
                 headers={'Authorization':authStr, 'Content-Type':'application/json'},
                 verify=False
                )
    print(f"Status Code: {r.status_code}, Response: {r.json()}")


