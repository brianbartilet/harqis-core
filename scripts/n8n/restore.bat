@echo off
setlocal

REM Check for backup file argument
if "%~1"=="" (
    echo Usage: %~nx0 ^<n8n_data_YYYYMMDD.tgz^>
    exit /b 1
)

set "BACKUP_FILE=%~1"

REM Create the empty volume first
docker volume create n8n_data

REM Restore into it
docker run --rm ^
    -v n8n_data:/data ^
    -v "%CD%:/backup" ^
    alpine sh -c "cd /data && tar xzf /backup/%BACKUP_FILE%"

endlocal
