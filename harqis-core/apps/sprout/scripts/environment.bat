set ENV_ENV_APP_PATH=C:\GIT\harqis-core\apps\sprout\core
set PYTHONPATH=C:\GIT\harqis-core

cd %ENV_ENV_APP_PATH%

git pull

call venv\Scripts\activate.bat