taskkill /f /im python.exe /t
taskkill /f /im flower.exe /t
taskkill /f /im node.exe /t


call environment.bat

rem call apps/sprout_wf/tasks/scripts/run_celery_scheduler.bat
rem call apps/sprout_wf/tasks/scripts/run_celery_scheduler_dashboard.bat
rem call apps/sprout_wf/tasks/scripts/run_celery_worker.bat

rem call apps/sprout_wf/tasks/scripts/run_flower.bat
rem call apps/sprout_wf/tasks/scripts/run_dashboard.bat