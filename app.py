"""
Mashup Assignment - Program 2
Flask Web Application with Email Service
Author: Student
Roll Number: 102303784
"""

from flask import Flask, render_template, request, jsonify
import os
import shutil
import re
import zipfile
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from yt_dlp import YoutubeDL
import threading

# Configure FFmpeg paths BEFORE importing pydub
# Try Windows path first (local development)
FFMPEG_PATH = r"C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"

# If not found, FFmpeg should be in system PATH (production/Linux)
if os.path.exists(FFMPEG_PATH):
    os.environ['PATH'] = FFMPEG_PATH + os.pathsep + os.environ.get('PATH', '')

# NOW import pydub after setting PATH
from pydub import AudioSegment

app = Flask(__name__)

# FFmpeg location (already set in PATH above)
FFMPEG_LOCATION = FFMPEG_PATH if os.path.exists(FFMPEG_PATH) else None

# Configure pydub to use FFmpeg explicitly
if FFMPEG_LOCATION:
    AudioSegment.converter = os.path.join(FFMPEG_LOCATION, 'ffmpeg.exe')
    AudioSegment.ffmpeg = os.path.join(FFMPEG_LOCATION, 'ffmpeg.exe')
    AudioSegment.ffprobe = os.path.join(FFMPEG_LOCATION, 'ffprobe.exe')
    # Also set as environment variable
    os.environ['FFMPEG_BINARY'] = os.path.join(FFMPEG_LOCATION, 'ffmpeg.exe')
    os.environ['FFPROBE_BINARY'] = os.path.join(FFMPEG_LOCATION, 'ffprobe.exe')

# Email configuration (use environment variables for security)
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_EMAIL = os.environ.get('SMTP_EMAIL', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def create_directories():
    """Create necessary directories"""
    directories = ['downloads', 'audios', 'trimmed', 'output']
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)


def download_videos(singer_name, num_videos):
    """Download YouTube videos"""
    downloaded_files = []
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        # Anti-bot detection measures
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    # Add FFmpeg location if found
    if FFMPEG_LOCATION:
        ydl_opts['ffmpeg_location'] = FFMPEG_LOCATION
    
    # Use cookies if available
    if os.path.exists('youtube_cookies.txt'):
        ydl_opts['cookiefile'] = 'youtube_cookies.txt'
    
    search_query = f"ytsearch{num_videos}:{singer_name}"
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(search_query, download=True)
    
    for file in os.listdir('downloads'):
        if file.endswith('.mp3'):
            downloaded_files.append(os.path.join('downloads', file))
    
    return downloaded_files


def process_audio(downloaded_files):
    """Copy audio files to audios folder"""
    audio_files = []
    for file_path in downloaded_files:
        filename = os.path.basename(file_path)
        audio_path = os.path.join('audios', filename)
        shutil.copy(file_path, audio_path)
        audio_files.append(audio_path)
    return audio_files


def trim_audio(audio_files, duration):
    """Trim first Y seconds from each audio"""
    trimmed_files = []
    duration_ms = duration * 1000
    
    # Set ffmpeg/ffprobe paths for this process
    if FFMPEG_LOCATION:
        AudioSegment.converter = os.path.join(FFMPEG_LOCATION, 'ffmpeg.exe')
        AudioSegment.ffmpeg = os.path.join(FFMPEG_LOCATION, 'ffmpeg.exe')
        AudioSegment.ffprobe = os.path.join(FFMPEG_LOCATION, 'ffprobe.exe')
    
    for audio_path in audio_files:
        try:
            print(f"  Trimming: {os.path.basename(audio_path)}")
            audio = AudioSegment.from_mp3(audio_path)
            trimmed_audio = audio[:duration_ms]
            
            filename = os.path.basename(audio_path)
            trimmed_path = os.path.join('trimmed', f"trimmed_{filename}")
            trimmed_audio.export(trimmed_path, format='mp3')
            trimmed_files.append(trimmed_path)
            print(f"    ✓ Trimmed successfully")
        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
    
    return trimmed_files


def merge_audios(trimmed_files, output_file):
    """Merge all audio files"""
    # Set ffmpeg/ffprobe paths for this process
    if FFMPEG_LOCATION:
        AudioSegment.converter = os.path.join(FFMPEG_LOCATION, 'ffmpeg.exe')
        AudioSegment.ffmpeg = os.path.join(FFMPEG_LOCATION, 'ffmpeg.exe')
        AudioSegment.ffprobe = os.path.join(FFMPEG_LOCATION, 'ffprobe.exe')
    
    combined = AudioSegment.empty()
    
    for trimmed_path in trimmed_files:
        audio = AudioSegment.from_mp3(trimmed_path)
        combined += audio
    
    combined.export(output_file, format='mp3')


def create_zip(mp3_file, zip_file):
    """Create zip file containing the mp3"""
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(mp3_file, os.path.basename(mp3_file))


def send_email(to_email, zip_file):
    """Send email with zip attachment"""
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        raise Exception("Email configuration not set. Please set SMTP_EMAIL and SMTP_PASSWORD environment variables.")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Mashup Result"
    
    body = """Hello!

Your mashup has been generated successfully. Please find the attached zip file containing your audio mashup.

Thank you for using our Mashup service!

Best regards,
Mashup Team
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach zip file
    with open(zip_file, 'rb') as attachment:
        part = MIMEBase('application', 'zip')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(zip_file)}')
        msg.attach(part)
    
    # Send email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_EMAIL, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()


def cleanup_directories():
    """Clean up temporary directories"""
    directories = ['downloads', 'audios', 'trimmed', 'output']
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)


def process_mashup(singer_name, num_videos, duration, email):
    """Process mashup in background"""
    try:
        print(f"🎵 Starting mashup for {singer_name}...")
        
        # Create directories
        create_directories()
        print("✓ Created directories")
        
        # Download videos
        print(f"⬇️  Downloading {num_videos} videos...")
        downloaded_files = download_videos(singer_name, num_videos)
        print(f"✓ Downloaded {len(downloaded_files)} videos")
        
        if len(downloaded_files) == 0:
            raise Exception("No videos were downloaded")
        
        # Process audio
        print("🎧 Processing audio files...")
        audio_files = process_audio(downloaded_files)
        print(f"✓ Processed {len(audio_files)} audio files")
        
        # Trim audio
        print(f"✂️  Trimming first {duration} seconds...")
        trimmed_files = trim_audio(audio_files, duration)
        print(f"✓ Trimmed {len(trimmed_files)} audio files")
        
        if len(trimmed_files) == 0:
            raise Exception("No audio files were trimmed")
        
        # Merge audios
        print("🔗 Merging audio files...")
        output_mp3 = 'output/mashup.mp3'
        merge_audios(trimmed_files, output_mp3)
        print("✓ Merged audio files")
        
        # Create zip
        print("📦 Creating zip file...")
        output_zip = 'output/mashup.zip'
        create_zip(output_mp3, output_zip)
        print("✓ Created zip file")
        
        # Send email
        print(f"📧 Sending email to {email}...")
        send_email(email, output_zip)
        print("✓ Email sent successfully")
        
        # Cleanup
        print("🧹 Cleaning up...")
        cleanup_directories()
        print("✓ Cleanup completed")
        
        print("✅ Mashup process completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in mashup process: {str(e)}")
        cleanup_directories()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    """Process mashup request"""
    try:
        # Get form data
        singer_name = request.form.get('singer_name', '').strip()
        num_videos = request.form.get('num_videos', '').strip()
        duration = request.form.get('duration', '').strip()
        email = request.form.get('email', '').strip()
        
        # Validate inputs
        errors = []
        
        if not singer_name:
            errors.append("Singer name is required")
        
        try:
            num_videos = int(num_videos)
            if num_videos <= 10:
                errors.append(f"Number of videos must be greater than 10 (got {num_videos})")
        except:
            errors.append("Number of videos must be a valid integer")
        
        try:
            duration = int(duration)
            if duration <= 20:
                errors.append(f"Duration must be greater than 20 seconds (got {duration})")
        except:
            errors.append("Duration must be a valid integer")
        
        if not validate_email(email):
            errors.append("Invalid email format")
        
        if not SMTP_EMAIL or not SMTP_PASSWORD:
            errors.append("Email service not configured. Please set SMTP_EMAIL and SMTP_PASSWORD environment variables.")
        
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
        
        # Start processing in background thread
        thread = threading.Thread(target=process_mashup, args=(singer_name, num_videos, duration, email))
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'message': 'Mashup is being processed. You will receive an email shortly.'})
    
    except Exception as e:
        return jsonify({'success': False, 'errors': [str(e)]}), 500


@app.route('/result')
def result():
    """Result page"""
    return render_template('result.html')


if __name__ == '__main__':
    print("=" * 60)
    print("🎵 MASHUP WEB SERVICE")
    print("=" * 60)
    print("\n📧 Email Configuration:")
    if SMTP_EMAIL and SMTP_PASSWORD:
        print(f"  SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
        print(f"  Email: {SMTP_EMAIL}")
        print("  ✓ Email service configured")
    else:
        print("  ⚠️  Warning: Email not configured!")
        print("  Set environment variables:")
        print("    SMTP_EMAIL=your-email@gmail.com")
        print("    SMTP_PASSWORD=your-app-password")
        print("    SMTP_SERVER=smtp.gmail.com (optional)")
        print("    SMTP_PORT=587 (optional)")
    
    print("\n🎬 FFmpeg Configuration:")
    if FFMPEG_LOCATION:
        print(f"  ✓ FFmpeg found: {FFMPEG_LOCATION}")
    else:
        print("  ⚠️  FFmpeg not detected in PATH")
    
    print("\n🌐 Starting Flask server...")
    print("=" * 60)
    
    # Get port from environment variable (for deployment) or use 5000 for local
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
