#! /usr/bin/bash
python manage.py makemigrations;
python manage.py migrate;

# python manage.py shell --no-input superuser
# data migrations
