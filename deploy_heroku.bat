@echo off
echo ================================
echo    Heroku Deployment Script
echo ================================
echo.

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Heroku CLI not found!
    echo Please install Heroku CLI first:
    echo https://devcenter.heroku.com/articles/heroku-cli
    echo.
    pause
    exit /b 1
)

echo ✅ Heroku CLI found!
echo.

REM Login to Heroku
echo 🔐 Logging into Heroku...
heroku auth:whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo Please login to Heroku:
    heroku login
    if %errorlevel% neq 0 (
        echo ❌ Heroku login failed
        pause
        exit /b 1
    )
)

echo ✅ Logged into Heroku!
echo.

REM Prompt for app name
set /p APP_NAME="Enter your Heroku app name (or press Enter for auto-generated): "

REM Create Heroku app
echo 🚀 Creating Heroku app...
if "%APP_NAME%"=="" (
    heroku create
) else (
    heroku create %APP_NAME%
)

if %errorlevel% neq 0 (
    echo ❌ Failed to create Heroku app
    pause
    exit /b 1
)

echo ✅ Heroku app created!
echo.

REM Set environment variables
echo 🔧 Setting environment variables...
heroku config:set SECRET_KEY="heroku-production-secret-key-change-this"
heroku config:set FLASK_ENV="production"

echo ✅ Environment variables set!
echo.

REM Add PostgreSQL database (optional)
set /p ADD_DB="Add free PostgreSQL database? (y/N): "
if /i "%ADD_DB%"=="y" (
    echo 🗄️ Adding PostgreSQL database...
    heroku addons:create heroku-postgresql:mini
    echo ✅ Database added!
    echo.
)

REM Deploy to Heroku
echo 📦 Deploying to Heroku...
git push heroku main

if %errorlevel% neq 0 (
    echo ❌ Deployment failed
    pause
    exit /b 1
)

echo ✅ Deployment successful!
echo.

REM Open the app
echo 🌐 Opening your app...
heroku open

echo.
echo ================================
echo    Deployment Complete! 🎉
echo ================================
echo.
echo Your Flask Student Portal is now live on Heroku!
echo.
echo Admin login:
echo Username: admin
echo Password: admin123
echo.
echo To view logs: heroku logs --tail
echo To restart: heroku restart
echo.
pause
