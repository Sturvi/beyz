@echo off
chcp 65001 > nul
echo ================================================
echo    Диагностика Barber Booking Platform
echo ================================================
echo.

echo [1/6] Проверка Docker...
docker --version
if errorlevel 1 (
    echo ✗ Docker не найден! Установите Docker Desktop
    pause
    exit /b 1
)
echo ✓ Docker установлен
echo.

echo [2/6] Проверка Docker Compose...
docker-compose --version
if errorlevel 1 (
    echo ✗ Docker Compose не найден!
    pause
    exit /b 1
)
echo ✓ Docker Compose установлен
echo.

echo [3/6] Статус контейнеров:
docker-compose ps
echo.

echo [4/6] Проверка портов...
netstat -ano | findstr "12000"
netstat -ano | findstr "12001"
echo.

echo [5/6] Последние логи PostgreSQL:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
docker-compose logs --tail=30 db
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [6/6] Последние логи Django:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
docker-compose logs --tail=30 web
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [ТЕСТ] Попытка подключения к http://localhost:12000
curl -s http://localhost:12000 > nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Сервер отвечает!
    echo Откройте в браузере: http://localhost:12000
) else (
    echo ✗ Сервер не отвечает!
    echo.
    echo Возможные причины:
    echo   1. Контейнер web не запущен
    echo   2. Django упал с ошибкой
    echo   3. Миграции не применились
    echo   4. База данных недоступна
    echo.
    echo Попробуйте:
    echo   docker-compose down -v
    echo   docker-compose up --build
)
echo.

echo ================================================
echo            Полезные команды
echo ================================================
echo.
echo Просмотр логов в реальном времени:
echo   docker-compose logs -f
echo.
echo Перезапуск контейнеров:
echo   docker-compose restart
echo.
echo Остановка контейнеров:
echo   docker-compose down
echo.
echo Вход в контейнер web:
echo   docker-compose exec web bash
echo.
echo ================================================
echo.
pause
