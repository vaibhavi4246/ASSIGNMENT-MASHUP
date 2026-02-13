# Mashup Web App - Deployment Guide

## 🚀 Deploy to Railway.app (Recommended)

Railway supports this app perfectly with FFmpeg and long-running processes.

### Steps:

1. **Create Railway Account**
   - Go to: https://railway.app
   - Sign up with GitHub

2. **Install Railway CLI** (Optional)
   ```powershell
   npm install -g @railway/cli
   ```

3. **Push to GitHub**
   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

4. **Deploy on Railway**
   - Click "New Project" on Railway
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect and deploy

5. **Add Environment Variables**
   In Railway dashboard, add:
   - `SMTP_EMAIL` = your email
   - `SMTP_PASSWORD` = your app password
   - `SMTP_SERVER` = smtp.gmail.com
   - `SMTP_PORT` = 587

6. **Add FFmpeg Buildpack**
   Railway should auto-install FFmpeg, but if not:
   - Go to Settings
   - Add buildpack: `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git`

7. **Access Your App**
   - Railway will give you a URL like: `https://your-app.railway.app`

---

## 🌐 Alternative: Deploy to Render.com

### Steps:

1. **Create Render Account**
   - Go to: https://render.com
   - Sign up with GitHub

2. **Push to GitHub** (same as above)

3. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Environment**: Python 3

4. **Add Environment Variables**
   Same as Railway

5. **Install FFmpeg**
   In Render dashboard, add render.yaml:
   ```yaml
   services:
     - type: web
       name: mashup-app
       env: python
       buildCommand: "apt-get update && apt-get install -y ffmpeg && pip install -r requirements.txt"
       startCommand: "gunicorn app:app"
   ```

---

## 📦 What's Included:

- ✅ `Procfile` - Tells server how to run the app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Updated with gunicorn
- ✅ `.gitignore` - Prevents uploading unnecessary files

---

## ⚠️ Important Notes:

1. **Free Tier Limits**:
   - Railway: $5 free credit/month
   - Render: 750 hours/month free

2. **Processing Time**:
   - Mashup takes 3-5 minutes
   - User must wait on result page
   - Email will be sent when done

3. **Storage**:
   - Temporary files are cleaned automatically
   - No persistent storage needed

---

## 🔧 If FFmpeg Doesn't Work:

Some platforms need special configuration. If you get FFmpeg errors:

**For Railway:**
Add this in your project settings → Environment variables:
```
NIXPACKS_PKGS=ffmpeg
```

**For Render:**
Create `render.yaml` in project root:
```yaml
services:
  - type: web
    name: mashup-app
    env: python
    buildCommand: |
      apt-get update
      apt-get install -y ffmpeg
      pip install -r requirements.txt
    startCommand: gunicorn app:app
```

---

## 📧 Email Configuration:

Remember to set these environment variables in your hosting platform:
- `SMTP_EMAIL`
- `SMTP_PASSWORD`
- `SMTP_SERVER=smtp.gmail.com`
- `SMTP_PORT=587`

---

## 🎯 Quick Deploy Commands:

```powershell
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/mashup-app.git

# Push
git push -u origin main
```

Then connect on Railway or Render dashboard!

---

## ✅ Testing After Deployment:

1. Visit your deployed URL
2. Fill the form
3. Submit and wait 3-5 minutes
4. Check email for ZIP file

---

**Need help with deployment? Let me know!**
