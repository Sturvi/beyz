#!/bin/bash

echo "🔄 Перезапуск проекта Barber Booking Platform..."
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Остановка контейнеров
echo -e "${YELLOW}1. Остановка всех контейнеров...${NC}"
docker-compose down -v 2>/dev/null || true
docker rm -f barber_postgres barber_web 2>/dev/null || true
echo -e "${GREEN}✓ Контейнеры остановлены${NC}"
echo ""

# Очистка volumes (опционально)
read -p "Очистить базу данных? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo -e "${YELLOW}2. Очистка volumes...${NC}"
    docker volume rm beyz_postgres_data 2>/dev/null || true
    rm -rf ./pgdata 2>/dev/null || true
    echo -e "${GREEN}✓ Volumes очищены${NC}"
else
    echo -e "${YELLOW}2. Пропуск очистки volumes${NC}"
fi
echo ""

# Пересборка образов
echo -e "${YELLOW}3. Пересборка Docker образов...${NC}"
docker-compose build --no-cache
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Образы успешно собраны${NC}"
else
    echo -e "${RED}✗ Ошибка при сборке образов${NC}"
    exit 1
fi
echo ""

# Запуск контейнеров
echo -e "${YELLOW}4. Запуск контейнеров...${NC}"
docker-compose up -d
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Контейнеры запущены${NC}"
else
    echo -e "${RED}✗ Ошибка при запуске контейнеров${NC}"
    echo -e "${YELLOW}Попробуйте использовать упрощенную версию:${NC}"
    echo "docker-compose -f docker-compose.simple.yml up"
    exit 1
fi
echo ""

# Ожидание запуска
echo -e "${YELLOW}5. Ожидание инициализации (30 сек)...${NC}"
sleep 30

# Проверка статуса
echo -e "${YELLOW}6. Проверка статуса контейнеров...${NC}"
docker-compose ps
echo ""

# Вывод логов
echo -e "${YELLOW}7. Последние логи:${NC}"
docker-compose logs --tail=20
echo ""

# Финальное сообщение
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Проект успешно запущен!${NC}"
echo ""
echo -e "Веб-интерфейс: ${GREEN}http://localhost:12000${NC}"
echo -e "Админ-панель:  ${GREEN}http://localhost:12000/admin/${NC}"
echo ""
echo -e "Тестовый пользователь:"
echo -e "  Email:  ${YELLOW}admin@barber.com${NC}"
echo -e "  Пароль: ${YELLOW}admin123${NC}"
echo ""
echo -e "Полезные команды:"
echo -e "  docker-compose logs -f         ${YELLOW}# Просмотр логов${NC}"
echo -e "  docker-compose down            ${YELLOW}# Остановка${NC}"
echo -e "  docker-compose restart         ${YELLOW}# Перезапуск${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
