# Barber Booking Platform - Платформа для онлайн записи в барбершоп

Система управления барбершопом с возможностью онлайн записи клиентов. Проект построен на Django с использованием PostgreSQL.

## Технологический стек

- **Backend**: Django 5.0.1
- **Database**: PostgreSQL 15
- **Frontend**: Django Templates + CSS
- **Containerization**: Docker & Docker Compose

## Особенности

- ✅ Кастомная модель пользователя с авторизацией по email
- ✅ Система ролей (Администратор, Барбер)
- ✅ Профили барберов с дополнительной информацией
- ✅ Современный и адаптивный дизайн
- ✅ Готовая Docker-среда для разработки
- ✅ Полностью на русском языке

## Структура проекта

```
beyz/
├── config/                 # Настройки Django проекта
│   ├── settings.py        # Основные настройки
│   ├── urls.py           # Главный роутинг
│   └── wsgi.py           # WSGI конфигурация
├── accounts/              # Приложение для управления пользователями
│   ├── models.py         # Модели User и BarberProfile
│   ├── views.py          # Представления
│   ├── forms.py          # Формы
│   ├── admin.py          # Админ-панель
│   └── urls.py           # URL маршруты
├── templates/             # HTML шаблоны
│   ├── base.html         # Базовый шаблон
│   └── accounts/         # Шаблоны авторизации
├── static/               # Статические файлы
│   └── css/
│       └── style.css     # Стили проекта
├── docker-compose.yml    # Docker Compose конфигурация
├── Dockerfile            # Docker образ приложения
├── requirements.txt      # Python зависимости
└── manage.py            # Django management скрипт
```

## Модели данных

### User (Пользователь)
- `email` - Email адрес (используется для авторизации)
- `role` - Роль (ADMIN или BARBER)
- `is_active` - Статус активности
- `is_staff` - Доступ к админ-панели
- `date_joined` - Дата регистрации

### BarberProfile (Профиль барбера)
- `user` - Связь с пользователем (OneToOne)
- `first_name` - Имя
- `last_name` - Фамилия
- `phone` - Телефон
- `bio` - О себе
- `photo` - Фото профиля
- `experience_years` - Опыт работы в годах
- `specializations` - Специализации
- `is_available` - Доступность для записи

## Быстрый старт

### Предварительные требования

Убедитесь, что у вас установлены:
- Docker
- Docker Compose

### Запуск проекта

#### Вариант 1: Автоматический скрипт (рекомендуется)

**Linux/Mac:**
```bash
chmod +x restart.sh
./restart.sh
```

**Windows:**
```cmd
restart.bat
```

#### Вариант 2: Ручной запуск

1. **Перейдите в директорию проекта**:
   ```bash
   cd beyz
   ```

2. **Запустите Docker Compose**:
   ```bash
   docker-compose up --build -d
   ```

3. **Дождитесь запуска сервисов** (около 30 секунд):
   - PostgreSQL будет доступна на порту `12001`
   - Django сервер будет доступен на порту `12000`

4. **Проверьте статус**:
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

5. **Откройте браузер и перейдите**:
   ```
   http://localhost:12000
   ```

### ⚠️ Если возникли проблемы

Если при запуске возникла ошибка `dependency failed to start: container beyz-db-1 exited (1)`:

1. **Попробуйте упрощенную версию**:
   ```bash
   docker-compose -f docker-compose.simple.yml up --build
   ```

2. **Очистите старые данные**:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

3. **Смотрите подробные инструкции** в файле [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Тестовые данные для входа

Автоматически создается администратор:
- **Email**: `admin@barber.com`
- **Пароль**: `admin123`
- **Роль**: Администратор

## Доступные команды

### Остановка сервисов
```bash
docker-compose down
```

### Остановка с удалением данных
```bash
docker-compose down -v
```

### Просмотр логов
```bash
docker-compose logs -f
```

### Вход в контейнер приложения
```bash
docker-compose exec web bash
```

### Создание миграций
```bash
docker-compose exec web python manage.py makemigrations
```

### Применение миграций
```bash
docker-compose exec web python manage.py migrate
```

### Создание суперпользователя вручную
```bash
docker-compose exec web python manage.py createsuperuser
```

### Сбор статических файлов
```bash
docker-compose exec web python manage.py collectstatic
```

## Порты

- **12000** - Django веб-сервер
- **12001** - PostgreSQL база данных

## Разработка без Docker

Если вы хотите запустить проект локально без Docker:

1. **Создайте виртуальное окружение**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate  # Windows
   ```

2. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте переменные окружения**:
   Скопируйте `.env.example` в `.env` и заполните данные для подключения к PostgreSQL

4. **Примените миграции**:
   ```bash
   python manage.py migrate
   ```

5. **Создайте суперпользователя**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Запустите сервер**:
   ```bash
   python manage.py runserver 12000
   ```

## Админ-панель Django

Доступ к админ-панели Django:
```
http://localhost:12000/admin/
```

В админ-панели вы можете:
- Управлять пользователями
- Редактировать профили барберов
- Просматривать все данные системы

## Функциональность

### Реализовано
- ✅ Авторизация по email
- ✅ Система ролей (Администратор, Барбер)
- ✅ Профили барберов
- ✅ Личный кабинет
- ✅ Редактирование профиля
- ✅ Красивый UI/UX
- ✅ Адаптивный дизайн

### В планах
- 📅 Система записи клиентов
- 📅 Управление услугами и прайс-листом
- 📅 Календарь записей
- 📅 Уведомления
- 📅 Статистика и отчеты

## Архитектура

Проект следует принципам чистого кода:

- **Модульность**: Каждое приложение отвечает за свою область
- **DRY**: Переиспользование кода через наследование и компоненты
- **SOLID**: Следование принципам объектно-ориентированного программирования
- **Документация**: Все модули и функции документированы
- **Типизация**: Использование type hints для лучшей читаемости

## База данных

PostgreSQL 15 используется как основная СУБД. Схема базы данных автоматически создается через Django ORM.

### Подключение к БД напрямую

```bash
docker-compose exec db psql -U barber_user -d barber_db
```

## Безопасность

- Пароли хешируются с использованием PBKDF2 алгоритма
- CSRF защита включена
- SQL инъекции предотвращены через Django ORM
- XSS защита через автоэскейпинг в шаблонах

## Поддержка

Если у вас возникли вопросы или проблемы, создайте issue в репозитории.

## Лицензия

Проект разработан для личного использования.

---

**Разработано с ❤️ для барбершопов**
