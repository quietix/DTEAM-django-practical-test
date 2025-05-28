#!/bin/bash

cd src && \
python3 ./manage.py makemigrations && \
python3 ./manage.py migrate

python3 ./manage.py collectstatic --noinput
python3 ./manage.py create_admin
python3 ./manage.py loaddata main/fixtures/initial_data.json

gunicorn --bind 0.0.0.0:8000 CVProject.wsgi
