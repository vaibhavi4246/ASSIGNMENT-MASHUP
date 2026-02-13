# 🎵 MASHUP ASSIGNMENT

Complete implementation of the Mashup Assignment with two programs:
- **Program 1**: Command-line Python tool
- **Program 2**: Flask web application with email service

---

## 📋 Prerequisites

### 1. Python 3.8 or higher
Check your Python version:
```powershell
python --version
```

### 2. FFmpeg
FFmpeg is required for audio processing.

#### Windows Installation:
1. Download FFmpeg from: https://ffmpeg.org/download.html
2. Extract the zip file
3. Add the `bin` folder to your system PATH
4. Verify installation:
```powershell
ffmpeg -version
```

#### Alternative (using Chocolatey):
```powershell
choco install ffmpeg
```

---

## 🚀 Installation

### 1. Clone/Download the project
Navigate to the project directory:
```powershell
cd c:\Users\ASUS\ASSIGNMENT-MASHUP
```

### 2. Create a virtual environment (recommended)
```powershell
python -m venv venv
```

### 3. Activate virtual environment
```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install dependencies
```powershell
pip install -r requirements.txt
```

---

## 📝 PROGRAM 1: Command Line Tool

### Usage
```powershell
python 102203579.py "<SingerName>" <NumberOfVideos> <AudioDuration> <OutputFileName>
```

### Parameters
- **SingerName**: Name of the singer to search (in quotes)
- **NumberOfVideos**: Number of videos to download (must be > 10)
- **AudioDuration**: Duration to trim from each audio in seconds (must be > 20)
- **OutputFileName**: Name of the output MP3 file

### Example
```powershell
python 102203579.py "Sharry Maan" 20 25 output.mp3
```

### What it does:
1. ✅ Validates all inputs (N > 10, Y > 20)
2. 📥 Downloads N YouTube videos of the singer
3. 🎵 Converts videos to MP3 audio
4. ✂️ Trims first Y seconds from each audio
5. 🔗 Merges all trimmed audios into one file
6. 📊 Displays progress and summary

### Output
The program will create a file named `output.mp3` (or your chosen name) containing the merged audio mashup.

---

## 🌐 PROGRAM 2: Flask Web Application

### Email Configuration

Before running the web app, you need to configure email settings.

#### For Gmail Users:

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate an App Password**:
   - Go to Google Account > Security > 2-Step Verification > App passwords
   - Create a new app password for "Mail"
   - Copy the 16-character password

3. **Set environment variables**:

**Windows PowerShell**:
```powershell
$env:SMTP_EMAIL="your-email@gmail.com"
$env:SMTP_PASSWORD="your-app-password"
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
```

**For permanent setup**, add to your PowerShell profile or use:
```powershell
[System.Environment]::SetEnvironmentVariable('SMTP_EMAIL', 'your-email@gmail.com', 'User')
[System.Environment]::SetEnvironmentVariable('SMTP_PASSWORD', 'your-app-password', 'User')
```

### Running the Web App

1. Make sure you're in the project directory with environment activated:
```powershell
cd c:\Users\ASUS\ASSIGNMENT-MASHUP
.\venv\Scripts\Activate.ps1
```

2. Set environment variables (see above)

3. Run the Flask app:
```powershell
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

### Using the Web App

1. Fill in the form:
   - **Singer Name**: e.g., "Sharry Maan"
   - **Number of Videos**: e.g., 20 (must be > 10)
   - **Audio Duration**: e.g., 25 seconds (must be > 20)
   - **Email**: Your valid email address

2. Click "Create Mashup"

3. Wait for processing (2-5 minutes)

4. Check your email inbox/spam folder for the ZIP file

### What it does:
1. ✅ Validates all form inputs
2. 📥 Downloads videos in the background
3. 🎵 Processes and merges audio
4. 📦 Creates a ZIP file
5. 📧 Emails the ZIP file to you
6. ✨ Shows success page

---

## 📁 Project Structure

```
ASSIGNMENT-MASHUP/
│
├── 102203579.py          # Program 1: CLI tool
├── app.py                # Program 2: Flask web app
├── requirements.txt      # Python dependencies
├── README.md            # This file
│
└── templates/           # HTML templates for web app
    ├── index.html       # Home page form
    └── result.html      # Success page
```

---

## ⚠️ Important Notes

### Validation Rules
- Number of videos **MUST be > 10**
- Audio duration **MUST be > 20 seconds**
- Email must be in valid format
- All parameters are required

### Error Handling
Both programs include:
- ✅ Input validation
- ✅ Exception handling
- ✅ Clear error messages
- ✅ Progress logging

### Temporary Files
Both programs automatically:
- Create temporary directories
- Clean up after completion
- Handle interruptions gracefully

---

## 🐛 Troubleshooting

### Issue: "ffmpeg not found"
**Solution**: Install FFmpeg and add to PATH (see Prerequisites)

### Issue: "No videos were downloaded"
**Solution**: 
- Check your internet connection
- Try a different singer name
- Some regions may have YouTube restrictions

### Issue: "Email not sent"
**Solution**:
- Verify SMTP environment variables are set
- Check your Gmail app password
- Ensure 2FA is enabled on your Google account
- Check if "Less secure app access" is needed (for older accounts)

### Issue: PowerShell script execution error
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Package installation fails
**Solution**:
```powershell
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

---

## 📧 Email Setup Guide (Detailed)

### Gmail Setup
1. Go to https://myaccount.google.com/
2. Navigate to Security
3. Enable 2-Step Verification
4. Go to App Passwords
5. Select "Mail" and your device
6. Copy the generated password
7. Use this password in SMTP_PASSWORD environment variable

### Other Email Providers
For other email providers, use their SMTP settings:

**Outlook/Hotmail**:
```powershell
$env:SMTP_SERVER="smtp-mail.outlook.com"
$env:SMTP_PORT="587"
```

**Yahoo**:
```powershell
$env:SMTP_SERVER="smtp.mail.yahoo.com"
$env:SMTP_PORT="587"
```

---

## 🎯 Testing Examples

### Program 1 Tests
```powershell
# Valid test
python 102203579.py "Arijit Singh" 15 30 test1.mp3

# Valid test with different duration
python 102203579.py "Diljit Dosanjh" 12 25 test2.mp3

# Should fail - videos <= 10
python 102203579.py "Singer" 10 30 test.mp3

# Should fail - duration <= 20
python 102203579.py "Singer" 15 20 test.mp3
```

### Program 2 Tests
1. Start the web app
2. Try valid inputs
3. Try invalid inputs to see error messages
4. Check email delivery

---

## 📝 Assignment Checklist

### Program 1 ✅
- [x] Command-line interface
- [x] Takes 4 parameters
- [x] Downloads N videos (N > 10)
- [x] Uses yt-dlp for downloading
- [x] Converts to audio
- [x] Trims Y seconds (Y > 20)
- [x] Uses pydub for trimming
- [x] Merges audio files
- [x] Validates inputs
- [x] Error handling
- [x] Progress logging
- [x] Proper output file

### Program 2 ✅
- [x] Flask web service
- [x] HTML form with all fields
- [x] Input validation
- [x] Email validation (regex)
- [x] Background processing
- [x] Creates ZIP file
- [x] Sends email with attachment
- [x] Success/error pages
- [x] SMTP configuration
- [x] Exception handling

---

## 👨‍💻 Author

**Roll Number**: 102203579

---

## 📄 License

This project is for educational purposes as part of an academic assignment.

---

## 🙏 Acknowledgments

- **yt-dlp**: For YouTube video downloading
- **pydub**: For audio processing
- **Flask**: For web framework
- **FFmpeg**: For audio/video conversion

---

## 📞 Support

If you encounter any issues:
1. Check the Troubleshooting section
2. Verify all prerequisites are installed
3. Check environment variables for Program 2
4. Review error messages carefully

---

**Happy Mashup Creating! 🎵**
