# Python Django Quickstart

This document shall serve as a quickstart guide for users who have some familiarity with Python but not the Django framework.

## Prerequisites

* Python 3.x
* Python virtual environment manager, i.e.: conda, venv, virtualenvwrapper
* PostgreSQL 13 or higher with PG Admin 4
* Python Django code on your local device
* A text editor, i.e. Notepad, Notepad++, or VS Code.
* VS Code (only if debugging)

## Prepare the Environment

1. (CMD) Open a command shell in the source code directory. Specifically, your CWD (current working directory) should be at the same level as the **manage.py** file.
2. (CMD) Create a new, or activate an existing, Python virtual environment. This is useful to keep your base version of Python from being overcrowded with unnecessary pip packages.
3. (GUI) Open PG Admin, right click on the server, select create new > Database and name it **plastics_eol**

## Run the Django Web App

1. Open a command shell in the source code directory. Specifically, your CWD (current working directory) should be at the same level as the **manage.py** file.
2. (CMD) Activate your Python virtual environment
3. (CMD) Install pip dependencies:
[ **pip install -r requirements.txt** ]
4. (CMD) Under the plastics_eol project directory (below manage.py level), create a copy of the settings.py file called **local_settings.py**
5. (TXT) Remove everything from the new local_settings.py file EXCEPT for the **DATABASES** section.
6. (TXT) Modify the **DATABASES** section to reflect your local PostgreSQL instance’s username, password, and database name (plastics_eol).
7. (CMD) Check for code changes that might require new database migrations:
[ **python manage.py makemigrations** ]
8. (CMD) Run database migrations:
[ **python manage.py migrate** ]
9. (CMD) Create a super user to log in with (follow the prompts for username, email, and password):
[ **python manage.py createsuperuser** ]
10. (CMD) Launch the app:
[ **python manage.py runserver** ]
