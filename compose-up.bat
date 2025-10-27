@echo off
setlocal enabledelayedexpansion

REM ==========================================
REM Validate input (argument = env file path)
REM ==========================================
if "%~1"=="" (
    echo ❌ ERROR: Please provide an .env file as argument.
    echo Usage: %~nx0 path_to_env_file
    echo Example: %~nx0 .env
    pause
    exit /b 1
)

set ENV_FILE=%~1

if not exist "%ENV_FILE%" (
    echo ❌ ERROR: .env file not found: "%ENV_FILE%"
    pause
    exit /b 1
)

REM ==========================================
REM Define compose file and project name
REM ==========================================
set COMPOSE_FILE=%~dp0docker-compose.yaml
set PROJECT_NAME=harqis-core

echo ==========================================
echo 📦 Docker Compose Launcher
echo ✅ Using env file: %ENV_FILE%
echo ✅ Using compose: %COMPOSE_FILE%
echo ✅ Project name: %PROJECT_NAME%
echo ==========================================

REM ==========================================
REM Start fresh containers using the provided .env
REM ==========================================
docker compose -p "%PROJECT_NAME%" down -v

docker compose --env-file "%ENV_FILE%" ^
    -f "%COMPOSE_FILE%" ^
    -p "%PROJECT_NAME%" up -d --force-recreate --build

echo Done! Check stack with:
echo    docker compose -p %PROJECT_NAME% ps

pause
endlocal
