# Быстрое решение проблемы с Docker

## Проблема
```
dependency failed to start: container beyz-db-1 exited (1)
```

## Решение (выберите один из вариантов)

### 🔥 Вариант 1: Быстрая очистка и перезапуск (РЕКОМЕНДУЕТСЯ)

```bash
# Остановите и очистите всё
docker-compose down -v

# Запустите заново
docker-compose up --build -d

# Просмотрите логи
docker-compose logs -f
```

### 🚀 Вариант 2: Используйте упрощенную версию

```bash
# Остановите старые контейнеры
docker-compose down -v

# Запустите упрощенную версию
docker-compose -f docker-compose.simple.yml up --build
```

### 🎯 Вариант 3: Автоматический скрипт

**Linux/Mac:**
```bash
chmod +x restart.sh
./restart.sh
```

**Windows:**
```cmd
restart.bat
```

### 🔧 Вариант 4: Проверьте, что порты свободны

**Linux/Mac:**
```bash
# Проверка портов
lsof -i :12000
lsof -i :12001

# Если заняты, убейте процессы
kill -9 <PID>
```

**Windows:**
```powershell
# Проверка портов
netstat -ano | findstr "12000"
netstat -ano | findstr "12001"

# Убить процесс
taskkill /PID <PID> /F
```

### 💻 Вариант 5: Запуск без Docker (локальная БД)

Если Docker не работает, используйте PostgreSQL локально:

1. **Установите PostgreSQL 15**
2. **Создайте базу:**
   ```sql
   CREATE USER barber_user WITH PASSWORD 'barber_password';
   CREATE DATABASE barber_db OWNER barber_user;
   ```
3. **Создайте файл `.env`:**
   ```env
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   DATABASE_NAME=barber_db
   DATABASE_USER=barber_user
   DATABASE_PASSWORD=barber_password
   SECRET_KEY=your-secret-key
   DEBUG=True
   ```
4. **Запустите проект:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или venv\Scripts\activate для Windows
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser --email admin@barber.com
   python manage.py runserver 12000
   ```

## После успешного запуска

Откройте в браузере:
- **Главная страница:** http://localhost:12000
- **Админ-панель:** http://localhost:12000/admin/

**Тестовый пользователь:**
- Email: `admin@barber.com`
- Пароль: `admin123`

## Всё ещё не работает?

Смотрите подробный гайд: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

Или отправьте мне вывод команды:
```bash
docker-compose logs db
```
