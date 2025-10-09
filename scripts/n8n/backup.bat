@echo off
setlocal

REM Check for backup name argument
if "%~1"=="" (
    echo Usage: %~nx0 ^<backup_name^>
    exit /b 1
)

set "BACKUP_NAME=%~1"

REM Create tar.gz of the named volume into current folder
docker run --rm ^
    -v n8n_data:/data ^
    -v "%CD%:/backup" ^
    alpine sh -c "cd /data && tar czf /backup/%BACKUP_NAME%.tgz ."

endlocal
