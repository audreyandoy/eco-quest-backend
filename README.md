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

The ChatGPT content generator requires a API key in order to run it.
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

To run the project you need to create a superuser for yourself.
That way you can view the information through the admin interface (including adding users)
```
python manage.py createsuperuser
```


# URLS available

*  Admin site:  http://127.0.0.1:8000/admin/
*  EcoEducation App:  http://127.0.0.1:8000/api/eco-education/
