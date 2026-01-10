# Deploy to Render - Quick Guide

## Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Step 2: Create Render Account
- Go to https://render.com
- Sign up (free tier)

## Step 3: Create PostgreSQL Database
1. Dashboard → New → PostgreSQL
2. Name: `french-dialogue-db`
3. Plan: Free
4. Click "Create Database"
5. Copy the "Internal Database URL"

## Step 4: Create Web Service
1. Dashboard → New → Web Service
2. Connect your GitHub repo
3. Configure:
   - Name: `french-dialogue-simulator`
   - Environment: Python 3
   - Build Command: `./build.sh`
   - Start Command: `gunicorn core.wsgi:application`

## Step 5: Set Environment Variables
Add these in Render dashboard:
- `SECRET_KEY` = (generate random string)
- `DEBUG` = `False`
- `ALLOWED_HOSTS` = `your-app.onrender.com`
- `DATABASE_URL` = (paste from Step 3)

## Step 6: Deploy
Click "Create Web Service" - Render will build and deploy automatically.

## Step 7: Create Superuser
After deployment, go to Shell tab:
```bash
python manage.py createsuperuser
```

## Your app will be live at:
https://your-app.onrender.com

## Note:
- Free tier sleeps after 15 min inactivity
- Media files are temporary (use S3 for production)
