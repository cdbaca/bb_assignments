# Bb API Assignments Project

The goal of this project is to use Bb DDA data and assignment templates
to automate creating folders and assignments in a large group of courses at once.

The impetus of the project was to create formative assessment assignments
for all courses in a given term. At SAGU, we were previously using "Progress Reports"
to track student course engagement in purely online courses. This was insufficient
for federal regulations, and we needed to add 1-3 assignments to a large number of courses.

## Current Status of Project

### Update 3/24/22

-running ```python3 delete_assign.py``` will take wildcard values for course(s) and assignment(s)
-running ```python3 delete_assign.py``` *will delete courses* if you answer "y". **Pay Attention!**

### Update 3/22/22

- add_folders.py is currently the main script to run via ```python3 add_folders.py```
- This will:
1. Create a directory to store token and other course_id/folder_id data
2. Get and store an access token (after you have verified your app, see below)
3. Add a folder called "Formative Assessments" to the Course Contents and the sidebar of the course.

## Current To Do

- Create new query for finding course_ids in which to place the folder.
- Create new query for finding the folder in which to place assignments.
- Update add_assign.py so that it is putting assignments in the correct place.
- Take command line arguments for the name of the folder and the name of the assignment.

# The below functions will work, but will be deprecated as the project evolves

## Finding Course Data and Creating JSON Files

[Bb DDA Query](https://github.com/cdbaca/bb_assignments/blob/main/find_course_contents.sql)

- This query should be used to pull the data necessary for running the script.
- Save the contents of the query to a file called "course_data.xlsx" in a subdirectory called "data."
- Run ```python3 get_data.py``` from the terminal. This will create the JSON files needed for add_assign.py.

## Add Assignments to Bb Instance

- Register as a Bb Developer [here](https://developer.blackboard.com/), register your application, and take note of your app secret & key.
- Create a new file in the main directory called "credentials.py", save your key and secret to those names as variables in that file.
- Once you have confirmed the JSON files in ../data are correct, you can run add_assign.py from the terminal.
