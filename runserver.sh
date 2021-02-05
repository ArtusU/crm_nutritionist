python manage.py collectstatic --no-input

python manage.py migrate --no-input

gunicorn --worker-tmp-dir /dev/shm crm.wsgi
