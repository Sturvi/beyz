#!/bin/bash

# Ожидание доступности базы данных
echo "Waiting for PostgreSQL..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Применение миграций
echo "Applying migrations..."
python manage.py migrate --noinput

# Сбор статики
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Создание суперпользователя если не существует
echo "Creating superuser if not exists..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@barber.com').exists():
    user = User.objects.create_superuser('admin@barber.com', 'admin123', role='ADMIN')
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
EOF

# Запуск сервера
echo "Starting server..."
python manage.py runserver 0.0.0.0:12000
