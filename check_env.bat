@echo off
echo Environment Check Script
echo ========================
echo.

echo Python Version:
python --version
echo.

echo Python Path:
where python
echo.

echo Environment Variables:
echo -------------------
set PATH
echo.

echo Current Directory:
cd
echo.

echo Directory Contents:
dir /b
echo.

echo Test File Creation:
echo Test content > test_file.txt
type test_file.txt
echo.

echo Script completed.
