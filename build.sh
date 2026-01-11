#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@email.com').exists():
    User.objects.create_superuser(email='admin@email.com', password='admin', first_name='Admin', last_name='User')
    print('Admin user created')
else:
    print('Admin user already exists')
END

python manage.py create_sample_data
