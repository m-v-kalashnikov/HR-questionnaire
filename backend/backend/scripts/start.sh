#!/bin/sh

if [[ "$DATABASE" = "postgres" ]]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

cd backend || exit
python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py migrate --no-input
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'a@a.com', 'admin')" | python3 manage.py shell
python3 manage.py runserver 0.0.0.0:8000
