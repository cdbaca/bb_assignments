# Bb API Assignments Project

The goal of this project is to use Bb DDA data and assignment templates
to automate creating assignments in a large group of courses at once.

The impetus of the project was to create formative assessment assignments
for all courses in a given term. At SAGU, we were previously using "Progress Reports"
to track student course engagement in purely online courses. This was insufficient
for federal regulations, and we needed to add 1-3 assignments to a large number of courses.

## Finding Course Data and Creating JSON Files

[Bb DDA Query](https://github.com/cdbaca/bb_assignments/blob/main/find_course_contents.sql)

- This query should be used to pull the data necessary for running the script.
- Save the contents of the query to a file called "course_data.xlsx" in a subdirectory called "data."
- Run the get_data.py file from the terminal. This will create the JSON files needed for add_assign.py.

## Add Assignments to Bb Instance

- Register as a Bb Developer [here](https://developer.blackboard.com/), register your application, and take note of your app secret & key.
- Create a new file in the main directory called "credentials.py", save your key and secret to those names as variables in that file.
- Once you have confirmed the JSON files in ../data are correct, you can run add_assign.py from the terminal.

## Future Goals

- make a web app