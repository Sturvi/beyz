@echo off
chcp 65001 > nul
echo ========================================
echo Перезапуск Barber Booking Platform
echo ========================================
echo.

echo [1/6] Остановка контейнеров...
docker-compose down -v 2>nul
docker rm -f barber_postgres barber_web 2>nul
echo ✓ Контейнеры остановлены
echo.

set /p cleanup="Очистить базу данных? (y/N): "
if /i "%cleanup%"=="y" (
    echo [2/6] Очистка volumes...
    docker volume rm beyz_postgres_data 2>nul
    rmdir /s /q pgdata 2>nul
    echo ✓ Volumes очищены
) else (
    echo [2/6] Пропуск очистки volumes
)
echo.

echo [3/6] Пересборка Docker образов...
docker-compose build --no-cache
if errorlevel 1 (
    echo ✗ Ошибка при сборке образов
    pause
    exit /b 1
)
echo ✓ Образы успешно собраны
echo.

echo [4/6] Запуск контейнеров...
docker-compose up -d
if errorlevel 1 (
    echo ✗ Ошибка при запуске контейнеров
    echo Попробуйте: docker-compose -f docker-compose.simple.yml up
    pause
    exit /b 1
)
echo ✓ Контейнеры запущены
echo.

echo [5/6] Ожидание инициализации (30 сек)...
timeout /t 30 /nobreak > nul
echo.

echo [6/6] Проверка статуса...
docker-compose ps
echo.

echo ========================================
echo ✓ Проект успешно запущен!
echo ========================================
echo.
echo Веб-интерфейс: http://localhost:12000
echo Админ-панель:  http://localhost:12000/admin/
echo.
echo Тестовый пользователь:
echo   Email:  admin@barber.com
echo   Пароль: admin123
echo.
echo Полезные команды:
echo   docker-compose logs -f    # Просмотр логов
echo   docker-compose down       # Остановка
echo   docker-compose restart    # Перезапуск
echo ========================================
echo.
pause
