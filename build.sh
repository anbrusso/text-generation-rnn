#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python textgeneration/manage.py flush --no-input
python textgeneration/manage.py makemigrations
python textgeneration/manage.py migrate
python textgeneration/manage.py collectstatic --no-input --clear