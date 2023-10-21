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

To run the project you need to create a superuser for yourself.
That way you can view the information through the admin interface (including adding users)
```
python manage.py createsuperuser
```

To migrate db models
```
python manage.py makemigrations
python manage.py migrate
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
*  Ecotransport single activity view endpoint: http://127.0.0.1:8000/api/eco-transport/<int:pk>  (fetches data for a specific activity for the authenticated user)


# Testing
You can use httpie in the dev dependencies to test.  Since our URLs are currently setup without a `/` at the end 
make sure a GET with parameters looks something line this:

```
http GET http://127.0.0.1:8000/api/eco-education-text/1
```