#!/bin/sh

if [[ "$DATABASE" = "postgres" ]]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python3 manage.py makemigrations
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input --clear
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$ADMIN_USER', '$ADMIN_MAIL', '$ADMIN_PASSWORD', first_name='$ADMIN_FIRST_NAME', last_name='$ADMIN_LAST_NAME')" | python3 manage.py shell
gunicorn backend.wsgi -b 0.0.0.0:8000
