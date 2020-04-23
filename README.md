# Django-Blog-App
Basic blog site written in Django

![3](https://user-images.githubusercontent.com/20891667/80091830-97127280-8583-11ea-8668-415f4205db64.gif)

## Features ##
- Registration with email verification
- Registration with Social media account

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
  
  
