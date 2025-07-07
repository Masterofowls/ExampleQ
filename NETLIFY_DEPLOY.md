# Netlify Deployment Guide

## 🚀 Deploy to Netlify

This Flask Student Portal is ready to deploy to Netlify Functions.

### Prerequisites

1. **Netlify Account**: Sign up at [netlify.com](https://netlify.com)
2. **Git Repository**: Push your code to GitHub, GitLab, or Bitbucket
3. **Netlify CLI** (optional): `npm install -g netlify-cli`

### Method 1: Deploy via Netlify Dashboard (Recommended)

1. **Connect Repository**:
   - Go to [Netlify Dashboard](https://app.netlify.com)
   - Click "New site from Git"
   - Connect your repository

2. **Configure Build Settings**:
   - Build command: `pip install -r requirements.txt`
   - Publish directory: `dist`
   - Functions directory: `netlify/functions`

3. **Set Environment Variables**:
   - Go to Site settings → Environment variables
   - Add these variables:
     ```
     SECRET_KEY=your-secure-secret-key-here
     NETLIFY=true
     FLASK_ENV=production
     ```

4. **Deploy**:
   - Click "Deploy site"
   - Your app will be available at `https://your-site-name.netlify.app`

### Method 2: Deploy via Netlify CLI

1. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**:
   ```bash
   netlify login
   ```

3. **Initialize Site**:
   ```bash
   netlify init
   ```

4. **Set Environment Variables**:
   ```bash
   netlify env:set SECRET_KEY "your-secure-secret-key-here"
   netlify env:set NETLIFY "true"
   netlify env:set FLASK_ENV "production"
   ```

5. **Deploy**:
   ```bash
   netlify deploy --prod
   ```

### Configuration Files

- `netlify.toml`: Main configuration file
- `netlify/functions/app.py`: Netlify Function handler
- `runtime.txt`: Python version specification
- `requirements.txt`: Python dependencies

### Features Supported

✅ **Student Login**: Group selection with dynamic loading
✅ **Admin Login**: Username/password authentication  
✅ **Database**: SQLite with automatic initialization
✅ **Posts Management**: Create, edit, delete posts
✅ **Group Management**: Admin can manage groups
✅ **Responsive Design**: Bootstrap-based UI

### Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | Your secret key | Flask session security |
| `NETLIFY` | `true` | Enable Netlify environment detection |
| `FLASK_ENV` | `production` | Flask environment mode |

### Default Credentials

- **Admin Login**: `admin` / `admin123`
- **Student Login**: Select any city, course, and group

### Troubleshooting

1. **Build Fails**: Check Python version in `runtime.txt`
2. **Function Errors**: Check function logs in Netlify dashboard
3. **Database Issues**: Netlify Functions recreate database on cold starts
4. **Environment Variables**: Ensure all required variables are set

### Support

- Netlify Docs: [docs.netlify.com](https://docs.netlify.com)
- Flask Docs: [flask.palletsprojects.com](https://flask.palletsprojects.com)

---

**Ready to deploy!** 🎉
