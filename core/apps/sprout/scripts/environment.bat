set ENV_ENV_APP_PATH=C:\GIT\harqis-core\harqis_core\apps\sprout\core
set PYTHONPATH=C:\GIT\harqis-core\harqis_core

cd %ENV_ENV_APP_PATH%

git pull

call venv\Scripts\activate.bat