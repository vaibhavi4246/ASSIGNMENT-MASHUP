# 🚀 QUICK START GUIDE - MASHUP ASSIGNMENT

## ⚡ 5-Minute Setup

### Step 1: Install FFmpeg
```powershell
# Check if installed
ffmpeg -version

# If not installed, download from: https://ffmpeg.org/download.html
# Or use Chocolatey: choco install ffmpeg
```

### Step 2: Setup Python Environment
```powershell
# Navigate to project
cd c:\Users\ASUS\ASSIGNMENT-MASHUP

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt
```

---

## 🎵 PROGRAM 1: Command Line

### Run It
```powershell
python 102203579.py "Sharry Maan" 15 30 output.mp3
```

### Expected Output
```
============================================================
🎵 MASHUP TOOL - COMMAND LINE VERSION
============================================================

📋 Input Parameters:
  Singer Name    : Sharry Maan
  Number of Videos: 15
  Audio Duration : 30 seconds
  Output File    : output.mp3

✓ Created directories: downloads/, audios/, trimmed/

🎵 Searching for 'Sharry Maan' videos on YouTube...
Downloading 15 videos...
  [1/15] Downloaded: Sharry Maan Song 1
  [2/15] Downloaded: Sharry Maan Song 2
  ...
✓ Successfully downloaded 15 audio files

🎧 Processing audio files...
✓ Processed 15 audio files

✂️  Trimming first 30 seconds from each audio...
✓ Trimmed 15 audio files

🔗 Merging 15 audio files...
✓ Successfully created: output.mp3
  File size: 5.23 MB
  Duration: 450.00 seconds

🧹 Cleaning up temporary files...
✓ Cleanup completed

============================================================
✅ MASHUP COMPLETED SUCCESSFULLY
============================================================
📊 Summary:
  Total videos downloaded : 15
  Total audios trimmed    : 15
  Final output file       : C:\Users\ASUS\ASSIGNMENT-MASHUP\output.mp3
============================================================
```

---

## 🌐 PROGRAM 2: Web Application

### Step 1: Setup Email (Gmail)
```powershell
# Set environment variables
$env:SMTP_EMAIL="your-email@gmail.com"
$env:SMTP_PASSWORD="your-16-char-app-password"
```

**Get App Password:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Click "App passwords"
4. Select "Mail" → Generate
5. Copy the 16-char password

### Step 2: Run Web App
```powershell
python app.py
```

### Step 3: Open Browser
```
http://localhost:5000
```

### Step 4: Fill Form
- Singer Name: `Sharry Maan`
- Number of Videos: `15`
- Duration: `30`
- Email: `your-email@example.com`

### Step 5: Check Email
Wait 2-5 minutes → Check inbox/spam → Download ZIP → Extract → Play MP3

---

## ✅ Validation Rules

| Parameter | Rule | Example |
|-----------|------|---------|
| Singer Name | Not empty | "Sharry Maan" |
| Number of Videos | Must be > 10 | 15, 20, 25 |
| Audio Duration | Must be > 20 | 25, 30, 40 |
| Email | Valid format | user@example.com |

---

## 🐛 Common Issues & Fixes

### Issue: `ffmpeg not found`
```powershell
# Install FFmpeg first
# Windows: Download from ffmpeg.org and add to PATH
# Or: choco install ffmpeg
```

### Issue: `Script execution disabled`
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: `Email not sent`
```powershell
# Check environment variables
python -c "import os; print(os.environ.get('SMTP_EMAIL'))"

# Make sure you used App Password, not regular password
# Enable 2FA first on Google Account
```

### Issue: `No videos downloaded`
- Check internet connection
- Try different singer name
- Some videos may be restricted

---

## 📝 Test Commands

### Test Program 1
```powershell
# Valid tests
python 102203579.py "Arijit Singh" 12 25 test1.mp3
python 102203579.py "Diljit Dosanjh" 15 30 test2.mp3

# Should fail - N <= 10
python 102203579.py "Singer" 10 30 fail.mp3

# Should fail - Y <= 20  
python 102203579.py "Singer" 15 20 fail.mp3

# Should fail - wrong parameter count
python 102203579.py "Singer" 15
```

---

## 📂 File Structure

```
ASSIGNMENT-MASHUP/
├── 102203579.py          # ← Program 1 (CLI)
├── app.py                # ← Program 2 (Web)
├── requirements.txt      # ← Dependencies
├── README.md            # ← Full documentation
├── QUICKSTART.md        # ← This file
├── .env.example         # ← Email config template
└── templates/
    ├── index.html       # ← Home page
    └── result.html      # ← Success page
```

---

## 🎯 What Each Program Does

### Program 1 (102203579.py)
1. Takes command-line input
2. Downloads YouTube videos
3. Extracts audio
4. Trims audio clips
5. Merges into one MP3
6. Saves output file

### Program 2 (app.py)
1. Shows web form
2. Validates input
3. Does same as Program 1
4. Creates ZIP file
5. Emails ZIP to user
6. Shows success page

---

## 💡 Pro Tips

1. **For Program 1**: Use quotes around singer name if it has spaces
   ```powershell
   python 102203579.py "Sharry Maan" 15 30 output.mp3  # ✅ Good
   python 102203579.py Sharry Maan 15 30 output.mp3    # ❌ Bad
   ```

2. **For Program 2**: Keep the terminal running while processing

3. **Email**: Always check spam folder if you don't see the email

4. **Testing**: Start with small numbers (12 videos, 25 seconds) for faster testing

5. **Cleanup**: Programs automatically clean up temporary files

---

## 📊 Assignment Requirements Checklist

### Program 1 ✅
- [x] CLI with 4 parameters
- [x] Downloads N videos (N > 10)
- [x] Uses yt-dlp
- [x] Converts to audio
- [x] Trims Y seconds (Y > 20)
- [x] Uses pydub
- [x] Merges audios
- [x] Validates inputs
- [x] Error handling

### Program 2 ✅
- [x] Flask web app
- [x] Form with all fields
- [x] Input validation
- [x] Email validation (regex)
- [x] Generates ZIP
- [x] Sends email
- [x] SMTP integration
- [x] Error handling

---

## 🎓 Assignment Submission

Make sure you have:
1. ✅ `102203579.py` - Working CLI program
2. ✅ `app.py` - Working web app
3. ✅ `templates/` folder with HTML files
4. ✅ `requirements.txt` - All dependencies
5. ✅ `README.md` - Documentation

---

## 📞 Need Help?

1. Read the full `README.md`
2. Check troubleshooting section
3. Verify all prerequisites
4. Test with examples provided

---

**You're all set! Good luck! 🎵✨**
