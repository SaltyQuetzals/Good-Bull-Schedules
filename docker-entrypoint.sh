#!/bin/bash

echo "Creating migrations"
python3 manage.py makemigrations --settings=goodbullschedules.settings.docker

echo "Migrating"
python3 manage.py migrate --settings=goodbullschedules.settings.docker --run-syncdb

echo "Making PDF Directory"
mkdir -p goodbullschedules/documents/pdfs

echo "Starting"
python3 manage.py runserver --settings=goodbullschedules.settings.docker 0.0.0.0:8000