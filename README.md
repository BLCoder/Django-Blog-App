# Django-Blog-App
Basic blog site written in Django

![3](https://user-images.githubusercontent.com/20891667/80091830-97127280-8583-11ea-8668-415f4205db64.gif)

## Used Tech Stack ##
1. Django
2. Celery

## Current Features ##
1. Registration with Email verification
2. Registration with Social media authentication(Facebook)
3. Create post

## Run ##
  
1. Install requirements
```bash
pip install -r requirements.txt
```
2. Start Redis Server

3. Migrate the changes of Database
```bash
python manage.py migrate
```
4. Create superuser
```bash
python manage.py createsuperuser
```
5. Run development server
```bash
python manage.py runserver
```
6. Open this url
```bash
127.0.0.1:8000
```
7. And finally you can run celery task by using command
```bash
celery -A project_name worker --pool=solo -l info
```
```bash
celery -A project_name beat -l info
```

## Issues with settings.py ##
you need to set some information in settings.py
```bash
EMAIL_HOST_USER = 'Your Email'
EMAIL_HOST_PASSWORD = 'Your Password'
SOCIAL_AUTH_FACEBOOK_KEY = 'Your App ID' 
SOCIAL_AUTH_FACEBOOK_SECRET = 'Your App Secret'
```


