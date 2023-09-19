#!/bin/bash
rm -r db.sqlite3
python3 manage.py migrate
DJANGO_SUPERUSER_PASSWORD='admin' python3 manage.py createsuperuser --noinput --username='admin' --email='admin@localhost'
python3 manage.py filldb --with_test_data
