# 🚀 Команды для запуска проекта

## Проблема: Pillow не установлен

### Решение для Docker (выполняйте по порядку):

```bash
# Перейдите в директорию проекта
cd /home/emin/PycharmProjects/beyz

# Обновите код (если нужно)
git pull origin claude/barber-booking-platform-011CUpwAHPegXbnRAJfEU3DD

# Остановите контейнеры и очистите volumes
docker-compose down -v

# Пересоберите образ с Pillow
docker-compose build --no-cache

# Запустите
docker-compose up -d

# Подождите 30-40 секунд

# Проверьте логи
docker-compose logs web

# Если всё OK, откройте http://localhost:12000
```

### Решение для локального запуска (без Docker):

```bash
# Перейдите в директорию проекта
cd /home/emin/PycharmProjects/beyz

# Активируйте venv
source .venv/bin/activate

# Установите Pillow
pip install Pillow==10.2.0

# Создайте миграции
python manage.py makemigrations

# Примените миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser --email admin@barber.com

# Запустите сервер
python manage.py runserver 8000

# Откройте http://localhost:8000
```

---

## Автоматические скрипты

### Linux/Mac:
```bash
chmod +x fix_pillow.sh
./fix_pillow.sh
```

### Windows:
```cmd
fix_pillow.bat
```

---

## Проверка что Pillow установлен

### В Docker:
```bash
docker-compose exec web python -c "import PIL; print(f'Pillow {PIL.__version__} установлен!')"
```

### Локально:
```bash
source .venv/bin/activate
python -c "import PIL; print(f'Pillow {PIL.__version__} установлен!')"
```

---

## Полезные команды

### Просмотр логов в реальном времени:
```bash
docker-compose logs -f web
```

### Вход в контейнер:
```bash
docker-compose exec web bash
```

### Проверка миграций:
```bash
# Docker
docker-compose exec web python manage.py showmigrations

# Локально
python manage.py showmigrations
```

### Применение миграций вручную:
```bash
# Docker
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Локально
python manage.py makemigrations
python manage.py migrate
```

### Создание суперпользователя:
```bash
# Docker
docker-compose exec web python manage.py createsuperuser

# Локально
python manage.py createsuperuser
```

---

## Если ничего не помогает

1. **Полная очистка Docker:**
   ```bash
   docker-compose down -v
   docker system prune -f
   docker-compose up --build -d
   ```

2. **Проверка requirements.txt:**
   ```bash
   cat requirements.txt
   # Должно быть:
   # Django==5.0.1
   # psycopg2-binary==2.9.9
   # python-decouple==3.8
   # gunicorn==21.2.0
   # Pillow==10.2.0
   ```

3. **Запуск диагностики:**
   ```bash
   chmod +x check.sh
   ./check.sh
   ```
