#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Диагностика Barber Booking Platform          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Проверка Docker
echo -e "${YELLOW}[1/6] Проверка Docker...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker установлен:${NC} $(docker --version)"
else
    echo -e "${RED}✗ Docker не найден! Установите Docker Desktop${NC}"
    exit 1
fi
echo ""

# Проверка docker-compose
echo -e "${YELLOW}[2/6] Проверка Docker Compose...${NC}"
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓ Docker Compose установлен:${NC} $(docker-compose --version)"
else
    echo -e "${RED}✗ Docker Compose не найден!${NC}"
    exit 1
fi
echo ""

# Статус контейнеров
echo -e "${YELLOW}[3/6] Статус контейнеров:${NC}"
docker-compose ps
echo ""

# Проверка портов
echo -e "${YELLOW}[4/6] Проверка портов...${NC}"
if lsof -i :12000 &> /dev/null; then
    echo -e "${GREEN}✓ Порт 12000 занят (это хорошо, если это наш контейнер):${NC}"
    lsof -i :12000
else
    echo -e "${RED}✗ Порт 12000 свободен - контейнер не слушает порт!${NC}"
fi
echo ""

if lsof -i :12001 &> /dev/null; then
    echo -e "${GREEN}✓ Порт 12001 занят (PostgreSQL):${NC}"
    lsof -i :12001
else
    echo -e "${RED}✗ Порт 12001 свободен - PostgreSQL не запущен!${NC}"
fi
echo ""

# Проверка логов БД
echo -e "${YELLOW}[5/6] Последние логи PostgreSQL:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
docker-compose logs --tail=30 db
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Проверка логов Web
echo -e "${YELLOW}[6/6] Последние логи Django:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
docker-compose logs --tail=30 web
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Тест подключения
echo -e "${YELLOW}[ТЕСТ] Попытка подключения к http://localhost:12000${NC}"
if curl -s http://localhost:12000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Сервер отвечает!${NC}"
    echo -e "${GREEN}Откройте в браузере: http://localhost:12000${NC}"
else
    echo -e "${RED}✗ Сервер не отвечает!${NC}"
    echo ""
    echo -e "${YELLOW}Возможные причины:${NC}"
    echo "  1. Контейнер web не запущен"
    echo "  2. Django упал с ошибкой (смотрите логи выше)"
    echo "  3. Миграции не применились"
    echo "  4. База данных недоступна"
    echo ""
    echo -e "${YELLOW}Попробуйте:${NC}"
    echo "  docker-compose down -v"
    echo "  docker-compose up --build"
fi
echo ""

# Рекомендации
echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║             Полезные команды                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Просмотр логов в реальном времени:${NC}"
echo "  docker-compose logs -f"
echo ""
echo -e "${YELLOW}Перезапуск контейнеров:${NC}"
echo "  docker-compose restart"
echo ""
echo -e "${YELLOW}Остановка контейнеров:${NC}"
echo "  docker-compose down"
echo ""
echo -e "${YELLOW}Вход в контейнер web:${NC}"
echo "  docker-compose exec web bash"
echo ""
echo -e "${YELLOW}Проверка миграций:${NC}"
echo "  docker-compose exec web python manage.py showmigrations"
echo ""
