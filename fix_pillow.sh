#!/bin/bash

echo "======================================================"
echo "  🔧 Полное исправление проблемы с Pillow"
echo "======================================================"
echo ""

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Обновление кода из репозитория
echo -e "${YELLOW}[1/5] Обновление кода из репозитория...${NC}"
git pull origin claude/barber-booking-platform-011CUpwAHPegXbnRAJfEU3DD
echo -e "${GREEN}✓ Код обновлен${NC}"
echo ""

# 2. Установка Pillow в локальное окружение (если есть venv)
if [ -d ".venv" ]; then
    echo -e "${YELLOW}[2/5] Установка Pillow в локальное окружение (.venv)...${NC}"
    .venv/bin/pip install Pillow==10.2.0
    echo -e "${GREEN}✓ Pillow установлен локально${NC}"
else
    echo -e "${YELLOW}[2/5] Виртуальное окружение .venv не найдено, пропуск...${NC}"
fi
echo ""

# 3. Остановка Docker контейнеров
echo -e "${YELLOW}[3/5] Остановка Docker контейнеров...${NC}"
docker-compose down -v
echo -e "${GREEN}✓ Контейнеры остановлены и volumes очищены${NC}"
echo ""

# 4. Пересборка Docker образа с Pillow
echo -e "${YELLOW}[4/5] Пересборка Docker образа (это займет 1-2 минуты)...${NC}"
docker-compose build --no-cache
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Образ успешно пересобран с Pillow${NC}"
else
    echo -e "${RED}✗ Ошибка при сборке образа${NC}"
    exit 1
fi
echo ""

# 5. Запуск контейнеров
echo -e "${YELLOW}[5/5] Запуск контейнеров...${NC}"
docker-compose up -d
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Контейнеры запущены${NC}"
else
    echo -e "${RED}✗ Ошибка при запуске${NC}"
    exit 1
fi
echo ""

# Ожидание инициализации
echo -e "${YELLOW}Ожидание инициализации (40 секунд)...${NC}"
for i in {40..1}; do
    echo -ne "\rОсталось: $i секунд... "
    sleep 1
done
echo ""
echo ""

# Проверка статуса
echo -e "${YELLOW}Проверка статуса контейнеров:${NC}"
docker-compose ps
echo ""

# Проверка логов
echo -e "${YELLOW}Последние логи Django:${NC}"
docker-compose logs --tail=20 web | grep -E "(Starting|Watching|error|Error|ERROR|Pillow|migrate)"
echo ""

# Тест подключения
echo -e "${YELLOW}Проверка доступности сервера...${NC}"
sleep 5
if curl -s http://localhost:12000 > /dev/null 2>&1; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓ ✓ ✓  УСПЕХ! Сервер работает! ✓ ✓ ✓${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "Откройте в браузере: ${GREEN}http://localhost:12000${NC}"
    echo ""
    echo -e "Данные для входа:"
    echo -e "  Email:  ${YELLOW}admin@barber.com${NC}"
    echo -e "  Пароль: ${YELLOW}admin123${NC}"
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}✗ Сервер не отвечает${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${YELLOW}Посмотрите полные логи:${NC}"
    echo "  docker-compose logs web"
    echo "  docker-compose logs db"
fi
echo ""
