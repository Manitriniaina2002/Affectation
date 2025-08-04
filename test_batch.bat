@echo off
echo Testing batch script execution > test_batch_output.txt
echo Current directory: %CD% >> test_batch_output.txt
dir /b >> test_batch_output.txt
type test_batch_output.txt
pause
