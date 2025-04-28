# ITSC4155-Jupiter
Team Jupiter's Git Repository for ITSC4155 Spring 2025.

Registration Tracker is an application that allows students at UNCC to create and save graduation timelines or course planners through an intuitive and informative website. With our application, students can:

* Manage/edit their plans for graduation
* Handle errors in registration plans
* Store registration plans/graduation timelines in a database

Additionally, student advisors can:

* Provide students with feedback on created plans
* Suggest edits or new plans altogether

Our technologies include Python, SQLite for relational databases, and Streamlit as our front-end framework and server host.

RUNNING INSTRUCTIONS:

1. Clone the repository using git clone https://github.com/ksotoenc/ITSC4155-Jupiter
2. Change working directories to /registration_tracker using this command: cd {your_root}/ITSC4155-Jupiter/registration_tracker
3. Install dependencies using this command: pip install -r requirements.txt
4. Change directories to /app using this command: cd app
5. Run our app: streamlit run home.py
6. Use these credentials to log in - username: uname, password: pword

TO RUN UNIT TESTS:
1. Change working directories to /unit_tests. Use this command: cd {your_root}/ITSC4155-Jupiter/registration_tracker/app/unit_tests
2. Run bash script driver. Use this command: ./driver.sh
3. Alternatively, if Step 2 does not work, run each unit test file inside unit_tests individually. Use this command: python {filename}