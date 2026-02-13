"""
Test Script for Mashup Assignment
Run this to verify your setup is correct
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 8:
        return True
    else:
        print("  ⚠️  Python 3.8 or higher recommended")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg installed: {version_line}")
            return True
    except FileNotFoundError:
        print("❌ FFmpeg not found")
        print("   Install from: https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        print(f"❌ Error checking FFmpeg: {e}")
        return False

def check_packages():
    """Check if required packages are installed"""
    packages = {
        'flask': 'Flask',
        'yt_dlp': 'yt-dlp',
        'pydub': 'pydub'
    }
    
    all_installed = True
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✓ {name} installed")
        except ImportError:
            print(f"❌ {name} not installed")
            all_installed = False
    
    if not all_installed:
        print("\n  Install packages with: pip install -r requirements.txt")
    
    return all_installed

def check_files():
    """Check if required files exist"""
    required_files = [
        '102303784.py',
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'templates/result.html'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def check_email_config():
    """Check email configuration"""
    smtp_email = os.environ.get('SMTP_EMAIL')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    
    if smtp_email and smtp_password:
        print(f"✓ Email configured: {smtp_email}")
        return True
    else:
        print("⚠️  Email not configured (optional for Program 1)")
        print("   Required for Program 2 (web app)")
        print("   Set: $env:SMTP_EMAIL and $env:SMTP_PASSWORD")
        return False

def main():
    print("=" * 60)
    print("🔍 MASHUP ASSIGNMENT - SETUP VERIFICATION")
    print("=" * 60)
    
    print("\n📦 Checking Python Version...")
    python_ok = check_python_version()
    
    print("\n🎬 Checking FFmpeg...")
    ffmpeg_ok = check_ffmpeg()
    
    print("\n📚 Checking Python Packages...")
    packages_ok = check_packages()
    
    print("\n📁 Checking Project Files...")
    files_ok = check_files()
    
    print("\n📧 Checking Email Configuration...")
    email_ok = check_email_config()
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    if python_ok and ffmpeg_ok and packages_ok and files_ok:
        print("✅ Program 1 (CLI) is ready to use!")
        print("\n   Run: python 102303784.py \"Singer Name\" 15 30 output.mp3")
    else:
        print("❌ Program 1 (CLI) setup incomplete")
        print("   Please fix the issues above")
    
    print()
    
    if python_ok and ffmpeg_ok and packages_ok and files_ok and email_ok:
        print("✅ Program 2 (Web App) is ready to use!")
        print("\n   Run: python app.py")
        print("   Then visit: http://localhost:5000")
    else:
        print("⚠️  Program 2 (Web App) setup incomplete")
        if not email_ok:
            print("   Configure email to use the web app")
        else:
            print("   Please fix the issues above")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
