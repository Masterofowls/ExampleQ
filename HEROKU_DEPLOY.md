# Heroku Deployment Guide

## Prerequisites
1. **Heroku Account**: Create a free account at https://heroku.com
2. **Heroku CLI**: Install from https://devcenter.heroku.com/articles/heroku-cli

## Deployment Steps

### 1. Install Heroku CLI and Login
```bash
# Install Heroku CLI (if not already installed)
# Then login
heroku login
```

### 2. Create Heroku App
```bash
cd C:\Users\danie\ExampleQ
heroku create your-app-name
```

### 3. Set Environment Variables
```bash
heroku config:set SECRET_KEY="your-production-secret-key-here"
heroku config:set FLASK_ENV="production"
```

### 4. Add PostgreSQL Database (Optional - Free Tier)
```bash
heroku addons:create heroku-postgresql:mini
```

### 5. Deploy to Heroku
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

### 6. Initialize Database
```bash
heroku run python -c "from app import create_app; app = create_app(); print('Database initialized')"
```

### 7. Open Your App
```bash
heroku open
```

## Files Created for Heroku:
- ✅ `Procfile` - Tells Heroku how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Updated with PostgreSQL support
- ✅ `wsgi.py` - WSGI entry point

## Environment Variables:
- `SECRET_KEY` - Your production secret key
- `DATABASE_URL` - Automatically set by Heroku PostgreSQL
- `FLASK_ENV` - Set to "production"

## Free Tier Limitations:
- **550-1000 dyno hours/month** (free)
- **App sleeps after 30 min** of inactivity
- **10,000 PostgreSQL rows** (free tier)

## Admin Login:
- **Username**: admin
- **Password**: admin123

Your Flask Student Portal will be available at: `https://your-app-name.herokuapp.com`
