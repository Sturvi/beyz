# 🔥 Быстрое решение проблемы

## Проблема
Pillow не установлен + миграции не применились

## Решение (выполните команды по порядку):

### Вариант 1: Полная пересборка (РЕКОМЕНДУЕТСЯ)

```bash
# 1. Остановите контейнеры
docker-compose down -v

# 2. Пересоберите образ с новыми зависимостями
docker-compose build --no-cache

# 3. Запустите заново
docker-compose up -d

# 4. Проверьте логи
docker-compose logs -f web
```

### Вариант 2: Быстрое обновление без пересборки

```bash
# 1. Установите Pillow в работающий контейнер
docker-compose exec web pip install Pillow==10.2.0

# 2. Примените миграции
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# 3. Создайте суперпользователя
docker-compose exec web python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@barber.com').exists():
    User.objects.create_superuser('admin@barber.com', 'admin123', role='ADMIN')
    print('Superuser created!')
EOF

# 4. Перезапустите web
docker-compose restart web
```

### Вариант 3: Использование скрипта

```bash
chmod +x restart.sh
./restart.sh
```

## После выполнения

Откройте браузер:
- http://localhost:12000

Должна открыться страница авторизации!

**Логин:** admin@barber.com
**Пароль:** admin123

---

## Если всё ещё не работает

Запустите диагностику:
```bash
chmod +x check.sh
./check.sh
```

И отправьте мне вывод.
