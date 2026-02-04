@echo off
echo ====================================================
echo   BookFinder: Team_VK AI Recommender System
echo ====================================================
echo.
echo 1. Checking Dependencies...
pip install -r requirements.txt
echo.
echo 2. Launching AI Recommender Engine...
start "BookFinder API" python run.py
echo.
echo 3. Service Status:
echo    - Main Dashboard: http://127.0.0.1:8000/
echo    - API Documentation: http://127.0.0.1:8000/docs
echo.
echo Press any key to shutdown the batch window (keep the API console open).
pause
