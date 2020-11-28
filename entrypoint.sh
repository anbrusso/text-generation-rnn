#!/bin/sh
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear
#create the test user automatically.
echo "from django.contrib.auth.models import User; User.objects.create_superuser('test', 'test@test.test', 'test')" | python manage.py shell

exec "$@"