## Welcome to EcoQuest!

# Installation and Setup
This program uses `pipenv` to install and manage dependecies in the `Pipfile`
Pipenv documentation is here:  https://docs.pipenv.org/
If you cannot install pipenv directly per the instructions you can perform the following:
```
python3 -m venv .venv
source .venv/bin/activate   # activate virtualenv on linux
pip install pipenv
```

https://lincolnloop.com/insights/using-pyprojecttoml-in-your-django-project/

Within the virtual environment, then you can install EcoQuest by:
```
pipenv install
```

The ChatGPT content generator requires an API key in order to run it.
You can create your own free account and generate the API key.
Information for getting an OpenAI trial account is here:
https://platform.openai.com/docs/guides/gpt

To run the app from the command line, you need to add the API key to your bash terminal session.
You can do this by adding this line to your `.bashrc` file: 
```
export OPENAI_API_KEY=<enter_api_key_here>
```

# Running the Project

To run the Django app (within pipenv or the )
```
python3 manage.py runserver
```

The program will automatically run on port 8000

# Data Admin Guidance

## Admin Django Superuser

To run the project you need to create a superuser for yourself.
That way you can view the information through the admin interface (including adding users)
```
python manage.py createsuperuser
```

## Sqlite3 db 
To migrate sqlite db models
```
python manage.py makemigrations
python manage.py migrate
```

## Postgres db migration

To use the postgres db first install postgres onto your machine and set the postgres user to `postgres` to match 
what is in the settings.py file.

```
sudo -u postgres psql  # to connect to postgres
```

Within the postgres command line utility do the following:
```
\password postgres  # set password for user postgres to "postgres"
CREATE DATABASE eco_db;  # create the eco_db
\c eco_db   # to connect to the eco_db
\q   # to quit
```

In the command line inside the project type the following
```
python manage.py migrate --run-syncdb  # sync to the postgres db
python manage.py loaddata data.json  # to load data to the new database
```

# Endpoints available

*  Splash page: http://127.0.0.1:8000/
* Admin site:  http://127.0.0.1:8000/admin
*  EcoEducation EndPoint:  http://127.0.0.1:8000/api/eco-education
  - GET returns a list of all education activities logged in the db
  - POST adds 5 points for user and accepts an optional "text" input to log what was read to db (future chatgpt seeding)
* EcoEducation single user activity list endpoint: http://127.0.0.1:8000/api/eco-transport/<int:pk>
* EcoEducation Text Endpoint http://127.0.0.1:8000/api/eco-education-text/<int:pk> 
  - GET returns "text" keyword with text that is customized to the "user_id" pk based on their profile information.
*  Ecotransport list endpoint: http://127.0.0.1:8000/api/eco-transport   (supports List i.e. provides list of challenges recorded for the authenticated user, and Create i.e. an authenticated user can record a challenge)
*  Ecotransport single user activity view endpoint: http://127.0.0.1:8000/api/eco-transport/<int:pk>  (fetches data for a specific activity for the authenticated user)
*  EcoMeals Endpoint: http://127.0.0.1:8000/api/eco-meals (GET request returns all entries by all users; POST request adds plant-based meal logged by user and calculates total points and co2 emissions reduced by eating plant-based.)
*  EcoMeals Single User View Endpoint:  http://127.0.0.1:8000/api/eco-meals/<int:pk> (GET request returns all plant-based meals logged by user as well as total points and co2 emissions reduced by each meal.)

 
 # Testing
You can use `httpie` tool included in the dev dependencies to test.  For pk URL try something like this:

```
http GET http://127.0.0.1:8000/api/eco-education-text/1
```
