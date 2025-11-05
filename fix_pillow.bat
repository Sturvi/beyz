@echo off
chcp 65001 > nul
echo ======================================================
echo   🔧 Полное исправление проблемы с Pillow
echo ======================================================
echo.

REM 1. Обновление кода
echo [1/5] Обновление кода из репозитория...
git pull origin claude/barber-booking-platform-011CUpwAHPegXbnRAJfEU3DD
echo ✓ Код обновлен
echo.

REM 2. Установка Pillow локально
if exist ".venv" (
    echo [2/5] Установка Pillow в локальное окружение ^(.venv^)...
    .venv\Scripts\pip install Pillow==10.2.0
    echo ✓ Pillow установлен локально
) else (
    echo [2/5] Виртуальное окружение .venv не найдено, пропуск...
)
echo.

REM 3. Остановка Docker
echo [3/5] Остановка Docker контейнеров...
docker-compose down -v
echo ✓ Контейнеры остановлены
echo.

REM 4. Пересборка образа
echo [4/5] Пересборка Docker образа ^(это займет 1-2 минуты^)...
docker-compose build --no-cache
if errorlevel 1 (
    echo ✗ Ошибка при сборке образа
    pause
    exit /b 1
)
echo ✓ Образ успешно пересобран с Pillow
echo.

REM 5. Запуск
echo [5/5] Запуск контейнеров...
docker-compose up -d
if errorlevel 1 (
    echo ✗ Ошибка при запуске
    pause
    exit /b 1
)
echo ✓ Контейнеры запущены
echo.

REM Ожидание
echo Ожидание инициализации ^(40 секунд^)...
timeout /t 40 /nobreak > nul
echo.

REM Проверка
echo Проверка статуса контейнеров:
docker-compose ps
echo.

echo Последние логи Django:
docker-compose logs --tail=20 web
echo.

REM Тест подключения
echo Проверка доступности сервера...
timeout /t 5 /nobreak > nul
curl -s http://localhost:12000 > nul 2>&1
if %errorlevel% equ 0 (
    echo ======================================================
    echo ✓ ✓ ✓  УСПЕХ! Сервер работает! ✓ ✓ ✓
    echo ======================================================
    echo.
    echo Откройте в браузере: http://localhost:12000
    echo.
    echo Данные для входа:
    echo   Email:  admin@barber.com
    echo   Пароль: admin123
) else (
    echo ======================================================
    echo ✗ Сервер не отвечает
    echo ======================================================
    echo.
    echo Посмотрите полные логи:
    echo   docker-compose logs web
    echo   docker-compose logs db
)
echo.
pause
