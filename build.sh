#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

#!/bin/sh
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear