@echo off
echo Starting Employee Assignment Management System...
python -u -m src.app > app_output.log 2>&1
echo Application has exited with error level %ERRORLEVEL%
type app_output.log
pause
