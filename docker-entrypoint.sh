#!/bin/bash

echo "Creating migrations"
python3 manage.py makemigrations --settings=goodbullschedules.settings.docker scraper scheduler

echo "Migrating"
python3 manage.py migrate --settings=goodbullschedules.settings.docker
python3 manage.py migrate --settings=goodbullschedules.settings.docker scraper
python3 manage.py migrate --settings=goodbullschedules.settings.docker scheduler

echo "Making PDF Directory"
mkdir -p /app/documents/pdfs

echo "Starting"
python3 manage.py runserver --settings=goodbullschedules.settings.docker 0.0.0.0:8000