@echo off
REM Script to run all tests on Windows

echo ================================================
echo Workshop Allocation Tool - Test Suite
echo ================================================
echo.

REM Check if pytest is installed
python -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo Error: pytest not found. Please install dependencies:
    echo   pip install -r requirements.txt
    exit /b 1
)

echo Running all tests...
echo.

REM Run tests with coverage
python -m pytest ^
    --cov=. ^
    --cov-report=term-missing ^
    --cov-report=html ^
    -v

if errorlevel 1 (
    echo.
    echo ================================================
    echo X Some tests failed.
    echo ================================================
    exit /b 1
) else (
    echo.
    echo ================================================
    echo * All tests passed!
    echo.
    echo Coverage report generated in htmlcov\index.html
    echo ================================================
)
