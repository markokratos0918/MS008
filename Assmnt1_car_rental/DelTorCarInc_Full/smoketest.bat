@echo off
REM ===============================
REM Smoke Test for DelTorCarInc.exe
REM ===============================

set EXE=DelTorCarInc_Release\DelTorCarInc.exe

if not exist "%EXE%" (
    echo [FAIL] Executable not found: %EXE%
    exit /b 1
)

echo [INFO] Running %EXE% for 3 seconds...
start "" /b "%EXE%"
timeout /t 3 >nul
taskkill /im DelTorCarInc.exe /f >nul 2>&1

if %errorlevel%==0 (
    echo [PASS] Smoke test completed successfully.
) else (
    echo [WARN] Executable exited unexpectedly.
)
