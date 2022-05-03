# Bb API Assignments Project

The goal of this project is to use Bb DDA data and assignment templates
to automate creating folders and assignments in a large group of courses at once.

The impetus of the project was to create formative assessment assignments
for all courses in a given term. At SAGU, we were previously using "Progress Reports"
to track student course engagement in purely online courses. This was insufficient
for federal regulations, and we needed to add 1-3 assignments to a large number of courses.

## How to use these scripts

1. To use these scripts, you'll need admin access to a Blackboard instance and Blackboard DDA for that instance.
2. Register as a Bb Developer [here](https://developer.blackboard.com/), register your application, and take note of your app secret & key.
3. Register your app in your Blackboard instance under Administrator Panel > REST API Integrations > Create Integration.
4. Clone this repository with ```git clone https://github.com/cdbaca/bb_assignments.git```
5. Create a virtual environment with ```python3 -m venv venv```, and activate the environment.
6. Run ```pip install -r requirements.txt```
7. Create a new file in the bb_assignments directory called "credentials.py". In the file, you'll need the following 
variables (*note: these variable names need to be exact*):
   - App Info:
     - key 
     - secret 
   - DDA Info:
     - hostname 
     - database
     - username
     - pwd
     - port-id
8. To use the scripts:
   - Directly change the selections of courses/terms/assignment/folder names in the sql queries of the scripts.
   - To delete a group of assignments similarly-named assignments (or just one assignment) from a course or group of courses, run ```python3 delete_assign.py```.
   - To add an assignment folder to the table of contents in a course or group of courses, run ```python3 add_folder.py```.
   - To add an assignment to a similarly named folder in a course or group of courses, run ```python3 add_assign.py```

It is suggested to create dummy courses in a dummy term when starting out. Because this uses DDA to query for courses, 
assignments, and folders, it can't be used on a test instance and must be used on a production Blackboard instance. However,
the scripts are built so that you can escape from adding assignments/folders or deleting assignments if the list doesn't 
produce the expected courses or folders.

## Current Status of Project
### Update 5/2/22
- Removed user input with formatted sql strings. This should have been done sooner, as f-string sql queries technically
allows for sql injection. This was not a major issue, as there are several security measures in place (read-only db, IP address limits, etc.).
Still, it was bad practice to keep that in the final code.
- This means that any changes to selection of courses and terms in *any* of the scripts needs to be a direct change to the
.py file itself.
- patch_duedates.py will update gradebook column due dates.

### Update 3/28/22

-The basics of the project all now work:
1. ```python3 delete_assign.py``` will delete a specific assignment based on a (wildcard) from one or multiple courses.
2. ```python3 add_folder.py``` will add a folder (title based on input) to a course or group of courses.
3. ```python3 add_assign.py``` will add an assignment to a course or courses with a specific folder in those courses.

### Update 3/24/22

- running ```python3 delete_assign.py``` will take wildcard values for course(s) and assignment(s)
- running ```python3 delete_assign.py``` *WILL DELETE SELECTED ASSIGNMENTS* if you answer "y". **Pay Attention!**

### Update 3/22/22

- add_folders.py is currently the main script to run via ```python3 add_folders.py```
- This will:
1. Create a directory to store token and other course_id/folder_id data
2. Get and store an access token (after you have verified your app, see below)
3. Add a folder called "Formative Assessments" to the Course Contents and the sidebar of the course.

## Current To Do

- **Fix ```get_token.store_token()```**: currently, if you run on two machines, the auth_token expiration will not sync to the file 
creation time, thus creating an issue with authenticating the API call for a short time
- **Add more options for dates and grades**: currently, the Adaptive Release, Due Date, and Points Possible options are
hard-coded. Need to add ability to update those in the script.