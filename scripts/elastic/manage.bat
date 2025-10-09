@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Config (env overrides allowed)
if not defined HOST_PORT_ELASTICSEARCH_HTTP set HOST_PORT_ELASTICSEARCH_HTTP=9200
if not defined SNAP_REPO set SNAP_REPO=local_fs
if not defined SNAP_DIR set SNAP_DIR=..\..\backups\es_snapshots

set "ES=http://localhost:%HOST_PORT_ELASTICSEARCH_HTTP%"

if "%~1"=="" goto :usage

:dispatch
if /I "%~1"=="register"        goto :register
if /I "%~1"=="backup"          goto :backup
if /I "%~1"=="list"            goto :list
if /I "%~1"=="restore"         goto :restore
if /I "%~1"=="restore-prefix"  goto :restorePrefix
if /I "%~1"=="archive"         goto :archive
goto :usage

:register
REM ============================================================================
REM CONFIGURATION
REM ============================================================================
REM All host snapshots will live in SNAP_DIR, e.g. ..\..\backups\es_snapshots
REM but Elasticsearch must see /usr/share/elasticsearch/snapshots inside container
set "SNAP_LOCATION=/usr/share/elasticsearch/snapshots"

REM Resolve host snapshot directory (SNAP_DIR) to absolute path
for /f "delims=" %%i in ("%SNAP_DIR%") do set "ABSOLUTE_DIR=%%~fi"

REM Create host directory if missing
if not exist "%ABSOLUTE_DIR%" (
    echo Creating snapshot directory "%ABSOLUTE_DIR%" ...
    mkdir "%ABSOLUTE_DIR%"
)

REM ============================================================================
REM CHECK HOST ↔ CONTAINER SETUP
REM ============================================================================
echo Checking if container path %SNAP_LOCATION% exists and writable...
docker exec -it elasticsearch sh -lc "test -d %SNAP_LOCATION% -a -w %SNAP_LOCATION% && echo OK || (echo NOT WRITABLE && exit 1)"
if errorlevel 1 (
    echo.
    echo [ERROR] Snapshot path %SNAP_LOCATION% is not accessible inside the container.
    echo Make sure your docker-compose includes:
    echo.
    echo   environment:
    echo     - path.repo=/usr/share/elasticsearch/snapshots
    echo   volumes:
    echo     - "%ABSOLUTE_DIR%:/usr/share/elasticsearch/snapshots"
    echo.
    exit /b 1
)

REM ============================================================================
REM REGISTER REPOSITORY
REM ============================================================================
echo Registering snapshot repo "%SNAP_REPO%" at %ES% -> %SNAP_LOCATION%
curl -s -X PUT "%ES%/_snapshot/%SNAP_REPO%" ^
  -H "Content-Type: application/json" ^
  -d "{\"type\":\"fs\",\"settings\":{\"location\":\"%SNAP_LOCATION%\",\"compress\":true}}"
echo.
goto :eof

:backup
for /f "usebackq delims=" %%t in (`powershell -NoProfile -Command "(Get-Date).ToString('yyyyMMdd-HHmmss')"`) do set "TS=%%t"
set "SNAP=snap-%TS%"
echo Creating snapshot %SNAP% ...
curl -s -X PUT "%ES%/_snapshot/%SNAP_REPO%/%SNAP%?wait_for_completion=true" -H "Content-Type: application/json" -d "{\"indices\":\"*\",\"ignore_unavailable\":true,\"include_global_state\":true}"
echo.
echo Done. Snapshot name: %SNAP%
goto :eof

:list
curl -s "%ES%/_snapshot/%SNAP_REPO%/_all?pretty"
echo.
goto :eof

:restore
if "%~2"=="" (
  echo Missing ^<SNAPSHOT^>
  goto :usage
)
set "SNAP=%~2"
echo Restoring snapshot %SNAP% (includes global state) ...
curl -s -X POST "%ES%/_snapshot/%SNAP_REPO%/%SNAP%/restore" -H "Content-Type: application/json" -d "{\"indices\":\"*\",\"ignore_unavailable\":true,\"include_global_state\":true}"
echo.
goto :eof

:restorePrefix
if "%~2"=="" (
  echo Missing ^<SNAPSHOT^>
  goto :usage
)
set "SNAP=%~2"
set "PREFIX=%~3"
if "%PREFIX%"=="" set "PREFIX=restored_"
echo Restoring snapshot %SNAP% with prefix "%PREFIX%" (no global state) ...
curl -s -X POST "%ES%/_snapshot/%SNAP_REPO%/%SNAP%/restore" -H "Content-Type: application/json" -d "{\"indices\":\"*\",\"ignore_unavailable\":true,\"include_global_state\":false,\"rename_pattern\":\"(.+)\",\"rename_replacement\":\"%PREFIX%\1\",\"indices_options\":{\"expand_wildcards\":\"open,closed\"}}"
echo.
goto :eof

:archive
if not exist "%SNAP_DIR%" (
  echo Snapshot directory "%SNAP_DIR%" does not exist.
  goto :eof
)
for /f "usebackq delims=" %%t in (`powershell -NoProfile -Command "(Get-Date).ToString('yyyyMMdd_HHmmss')"`) do set "TS=%%t"
set "OUT="%SNAP_DIR%"/es_snapshots_%TS%.tgz"
echo Archiving %SNAP_DIR% ^> %OUT%
tar -czf "%OUT%" -C "%SNAP_DIR%" .
echo Created %OUT%
goto :eof

:usage
echo Usage: %~nx0 ^<command^> [args]
echo.
echo Commands:
echo   register
echo   backup
echo   list
echo   restore ^<SNAPSHOT^>
echo   restore-prefix ^<SNAPSHOT^> [PREFIX]
echo   archive
echo.
echo Env (optional):
echo   HOST_PORT_ELASTICSEARCH_HTTP (default: 9200)
echo   SNAP_REPO (default: local_fs)
echo   SNAP_DIR  (default: backup\es_snapshots)
exit /b 1
