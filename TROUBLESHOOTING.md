# Решение проблем с Docker

Если у вас возникла ошибка `dependency failed to start: container beyz-db-1 exited (1)`, выполните следующие шаги:

## Шаг 1: Очистка старых контейнеров и volumes

```bash
# Остановите все контейнеры проекта
docker-compose down

# Удалите все volumes (это очистит данные БД)
docker-compose down -v

# Проверьте, что не осталось запущенных контейнеров
docker ps -a | grep beyz

# Если остались, удалите их принудительно
docker rm -f beyz-db-1 beyz-web-1 barber_postgres barber_web
```

## Шаг 2: Проверка портов

Убедитесь, что порты 12000 и 12001 не заняты другими процессами:

### Linux/Mac:
```bash
# Проверка порта 12000
lsof -i :12000

# Проверка порта 12001
lsof -i :12001

# Если порт занят, убейте процесс
kill -9 <PID>
```

### Windows (PowerShell):
```powershell
# Проверка портов
netstat -ano | findstr "12000"
netstat -ano | findstr "12001"

# Убить процесс по PID
taskkill /PID <PID> /F
```

## Шаг 3: Проверка логов PostgreSQL

```bash
# Запустите только БД
docker-compose up db

# Посмотрите логи в реальном времени
# Если увидите ошибки, это поможет понять проблему
```

Частые ошибки PostgreSQL:
- `permission denied` - проблема с правами на volume
- `port already in use` - порт 12001 занят другим процессом
- `initdb: error` - проблема с инициализацией базы

## Шаг 4: Запуск с пересборкой

```bash
# Полная пересборка образов
docker-compose build --no-cache

# Запуск с пересборкой
docker-compose up --build

# Или в фоновом режиме
docker-compose up --build -d
```

## Альтернативное решение: Изменить порт БД

Если порт 12001 занят, измените его в `docker-compose.yml`:

```yaml
services:
  db:
    ports:
      - "12002:5432"  # Измените 12001 на 12002
```

## Запуск БД локально (без Docker)

Если Docker продолжает давать сбои, можете использовать PostgreSQL локально:

### 1. Установите PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**MacOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Windows:**
Скачайте установщик с https://www.postgresql.org/download/windows/

### 2. Создайте базу данных

```bash
# Войдите в PostgreSQL
sudo -u postgres psql

# Создайте пользователя и базу
CREATE USER barber_user WITH PASSWORD 'barber_password';
CREATE DATABASE barber_db OWNER barber_user;
GRANT ALL PRIVILEGES ON DATABASE barber_db TO barber_user;
\q
```

### 3. Обновите .env файл

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=barber_db
DATABASE_USER=barber_user
DATABASE_PASSWORD=barber_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 4. Запустите проект без Docker

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте его
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Примените миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser --email admin@barber.com

# Запустите сервер
python manage.py runserver 12000
```

## Проверка работы Docker

```bash
# Проверьте версию Docker
docker --version
docker-compose --version

# Проверьте, что Docker запущен
docker ps

# Проверьте доступное место на диске
df -h
```

## Если ничего не помогает

1. Перезагрузите Docker Desktop (если используете)
2. Очистите все неиспользуемые Docker ресурсы:
   ```bash
   docker system prune -a --volumes
   ```
   ⚠️ Внимание: это удалит ВСЕ неиспользуемые образы и volumes!

3. Проверьте логи Docker:
   ```bash
   docker-compose logs db
   docker-compose logs web
   ```

## Получение помощи

Если проблема сохраняется, предоставьте:
1. Полный вывод `docker-compose logs db`
2. Версию Docker: `docker --version`
3. ОС и её версию
4. Вывод `docker ps -a`
