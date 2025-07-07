# Manual Heroku Deployment Guide

## The Heroku CLI has compatibility issues on this system. Follow these steps to deploy manually:

### Step 1: Create Heroku Account & App
1. Go to https://heroku.com and create an account (if you don't have one)
2. Go to https://dashboard.heroku.com/apps
3. Click "New" → "Create new app"
4. Choose an app name (e.g., `student-portal-app` or let Heroku generate one)
5. Select a region (US or Europe)
6. Click "Create app"

### Step 2: Connect GitHub Repository
1. In your new Heroku app dashboard, go to the "Deploy" tab
2. Under "Deployment method", select "GitHub"
3. Click "Connect to GitHub" and authorize if needed
4. Search for your repository: `ExampleQ`
5. Click "Connect" next to your repository

### Step 3: Configure Environment Variables
1. Go to the "Settings" tab
2. Click "Reveal Config Vars"
3. Add these environment variables:
   - `SECRET_KEY`: `your-secret-key-here-make-it-long-and-random`
   - `FLASK_ENV`: `production`
   - `DATABASE_URL`: (Leave blank - Heroku will auto-configure PostgreSQL)

### Step 4: Add PostgreSQL Database
1. Go to the "Resources" tab
2. In the "Add-ons" section, search for "Heroku Postgres"
3. Select "Heroku Postgres" and choose the "Hobby Dev - Free" plan
4. Click "Submit Order Form"

### Step 5: Deploy
1. Go back to the "Deploy" tab
2. Scroll down to "Manual deploy"
3. Make sure "main" branch is selected
4. Click "Deploy Branch"
5. Wait for the build to complete

### Step 6: Initialize Database
After deployment, the database needs to be initialized. You'll need to run this command somehow:
```
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all(); from app.models import Admin, Group; admin = Admin(username='admin'); admin.set_password('admin123'); db.session.add(admin); db.session.commit(); print('Admin created!')" --app YOUR-APP-NAME
```

### Alternative: Auto-Deploy
1. In the "Deploy" tab, under "Automatic deploys"
2. Click "Enable Automatic Deploys"
3. This will redeploy whenever you push to the main branch

### Step 7: Test Your App
1. Click "Open app" button in the top right
2. Test the login functionality:
   - Student login: Select a group
   - Admin login: username `admin`, password `admin123`

## Your app files are already configured for Heroku:
- ✅ `Procfile`: Tells Heroku how to run the app
- ✅ `runtime.txt`: Specifies Python version
- ✅ `requirements.txt`: Lists dependencies including PostgreSQL support
- ✅ `wsgi.py`: Entry point for the app
- ✅ Environment variable support in `app/__init__.py`

## If deployment fails:
1. Check the build logs in the "Activity" tab
2. Common issues:
   - Missing dependencies in `requirements.txt`
   - Environment variable configuration
   - Database initialization

## To update the app:
1. Make changes to your code
2. Commit and push to GitHub
3. If auto-deploy is enabled, it will update automatically
4. If not, use "Manual deploy" again

Your app is ready for Heroku deployment! 🚀
