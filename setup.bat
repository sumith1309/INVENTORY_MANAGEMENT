@echo off
echo ========================================
echo Inventory Management Dashboard Setup
echo ========================================
echo.

cd backend

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the backend server, run:
echo   cd backend
echo   venv\Scripts\activate
echo   python app.py
echo.
echo Then open index.html or dashboard.html in your browser
echo.
pause

