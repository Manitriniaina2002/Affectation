@echo off
echo Testing environment... > env_test.txt
echo Current directory: %CD% >> env_test.txt
echo Date: %DATE% %TIME% >> env_test.txt
echo. >> env_test.txt
echo Environment variables: >> env_test.txt
echo --------------------- >> env_test.txt
set >> env_test.txt
echo. >> env_test.txt
echo Directory contents: >> env_test.txt
echo ------------------ >> env_test.txt
dir /b >> env_test.txt

:: Try to display the file
type env_test.txt

:: Pause to see the output
pause
