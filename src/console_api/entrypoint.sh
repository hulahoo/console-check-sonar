python manage.py migrate --noinput
gunicorn api.wsgi:application --bind 0.0.0.0:8000