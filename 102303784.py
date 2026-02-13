"""
Mashup Assignment - Program 1
Command Line Mashup Tool
Author: Student
Roll Number: 102203579
"""

import sys
import os
import shutil
import re
from yt_dlp import YoutubeDL
from pydub import AudioSegment


def validate_inputs(singer_name, num_videos, duration, output_file):
    """Validate command line inputs"""
    errors = []
    
    if not singer_name or singer_name.strip() == "":
        errors.append("Singer name cannot be empty")
    
    try:
        num_videos = int(num_videos)
        if num_videos <= 10:
            errors.append(f"Number of videos must be > 10 (got {num_videos})")
    except ValueError:
        errors.append("Number of videos must be an integer")
    
    try:
        duration = int(duration)
        if duration <= 20:
            errors.append(f"Audio duration must be > 20 seconds (got {duration})")
    except ValueError:
        errors.append("Audio duration must be an integer")
    
    if not output_file.endswith('.mp3'):
        errors.append("Output file must have .mp3 extension")
    
    return errors


def create_directories():
    """Create necessary directories for downloads"""
    directories = ['downloads', 'audios', 'trimmed']
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)
    print("✓ Created directories: downloads/, audios/, trimmed/")


def download_videos(singer_name, num_videos):
    """Download YouTube videos of the singer"""
    print(f"\n🎵 Searching for '{singer_name}' videos on YouTube...")
    
    downloaded_files = []
    
    # yt-dlp options with anti-bot measures
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
        'ignoreerrors': True,
        # Anti-bot detection measures
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    # Use cookies if available
    if os.path.exists('youtube_cookies.txt'):
        ydl_opts['cookiefile'] = 'youtube_cookies.txt'
        print("  Using cookies file for authentication")
    
    search_query = f"ytsearch{num_videos}:{singer_name}"
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading {num_videos} videos...")
            info = ydl.extract_info(search_query, download=True)
            
            if 'entries' in info:
                for idx, entry in enumerate(info['entries'], 1):
                    if entry:
                        print(f"  [{idx}/{num_videos}] Downloaded: {entry.get('title', 'Unknown')}")
            
        # Get downloaded mp3 files
        for file in os.listdir('downloads'):
            if file.endswith('.mp3'):
                downloaded_files.append(os.path.join('downloads', file))
        
        print(f"✓ Successfully downloaded {len(downloaded_files)} audio files")
        return downloaded_files
    
    except Exception as e:
        print(f"❌ Error downloading videos: {str(e)}")
        raise


def convert_to_audio(downloaded_files):
    """Convert downloaded files to audio (already done by yt-dlp)"""
    audio_files = []
    
    print(f"\n🎧 Processing audio files...")
    for idx, file_path in enumerate(downloaded_files, 1):
        try:
            # Copy to audios folder
            filename = os.path.basename(file_path)
            audio_path = os.path.join('audios', filename)
            shutil.copy(file_path, audio_path)
            audio_files.append(audio_path)
            print(f"  [{idx}/{len(downloaded_files)}] Processed: {filename}")
        except Exception as e:
            print(f"  ⚠ Warning: Could not process {file_path}: {str(e)}")
    
    print(f"✓ Processed {len(audio_files)} audio files")
    return audio_files


def trim_audio(audio_files, duration):
    """Trim first Y seconds from each audio file"""
    print(f"\n✂️  Trimming first {duration} seconds from each audio...")
    
    trimmed_files = []
    duration_ms = duration * 1000  # Convert to milliseconds
    
    for idx, audio_path in enumerate(audio_files, 1):
        try:
            # Load audio file
            audio = AudioSegment.from_mp3(audio_path)
            
            # Trim first Y seconds
            trimmed_audio = audio[:duration_ms]
            
            # Save trimmed audio
            filename = os.path.basename(audio_path)
            trimmed_path = os.path.join('trimmed', f"trimmed_{filename}")
            trimmed_audio.export(trimmed_path, format='mp3')
            
            trimmed_files.append(trimmed_path)
            print(f"  [{idx}/{len(audio_files)}] Trimmed: {filename}")
        
        except Exception as e:
            print(f"  ⚠ Warning: Could not trim {audio_path}: {str(e)}")
    
    print(f"✓ Trimmed {len(trimmed_files)} audio files")
    return trimmed_files


def merge_audios(trimmed_files, output_file):
    """Merge all trimmed audios into one file"""
    print(f"\n🔗 Merging {len(trimmed_files)} audio files...")
    
    try:
        # Start with empty audio
        combined = AudioSegment.empty()
        
        for idx, trimmed_path in enumerate(trimmed_files, 1):
            audio = AudioSegment.from_mp3(trimmed_path)
            combined += audio
            print(f"  [{idx}/{len(trimmed_files)}] Merged: {os.path.basename(trimmed_path)}")
        
        # Export final file
        combined.export(output_file, format='mp3')
        print(f"✓ Successfully created: {output_file}")
        
        # Get file size
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        print(f"  File size: {file_size:.2f} MB")
        print(f"  Duration: {len(combined) / 1000:.2f} seconds")
        
        return True
    
    except Exception as e:
        print(f"❌ Error merging audio files: {str(e)}")
        raise


def cleanup_temp_directories():
    """Clean up temporary directories"""
    print("\n🧹 Cleaning up temporary files...")
    directories = ['downloads', 'audios', 'trimmed']
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
    print("✓ Cleanup completed")


def main():
    """Main function"""
    print("=" * 60)
    print("🎵 MASHUP TOOL - COMMAND LINE VERSION")
    print("=" * 60)
    
    # Check command line arguments
    if len(sys.argv) != 5:
        print("\n❌ Error: Incorrect number of parameters")
        print("\nUsage:")
        print('  python 102203579.py "<SingerName>" <NumberOfVideos> <AudioDuration> <OutputFileName>')
        print("\nExample:")
        print('  python 102203579.py "Sharry Maan" 20 20 output.mp3')
        print("\nParameters:")
        print("  SingerName      : Name of the singer to search")
        print("  NumberOfVideos  : Number of videos to download (must be > 10)")
        print("  AudioDuration   : Duration to trim from each audio in seconds (must be > 20)")
        print("  OutputFileName  : Name of output mp3 file")
        sys.exit(1)
    
    # Parse arguments
    singer_name = sys.argv[1]
    num_videos = sys.argv[2]
    duration = sys.argv[3]
    output_file = sys.argv[4]
    
    print(f"\n📋 Input Parameters:")
    print(f"  Singer Name    : {singer_name}")
    print(f"  Number of Videos: {num_videos}")
    print(f"  Audio Duration : {duration} seconds")
    print(f"  Output File    : {output_file}")
    
    # Validate inputs
    errors = validate_inputs(singer_name, num_videos, duration, output_file)
    if errors:
        print("\n❌ Validation Errors:")
        for error in errors:
            print(f"  • {error}")
        sys.exit(1)
    
    num_videos = int(num_videos)
    duration = int(duration)
    
    try:
        # Create directories
        create_directories()
        
        # Download videos
        downloaded_files = download_videos(singer_name, num_videos)
        
        if len(downloaded_files) == 0:
            print("\n❌ Error: No videos were downloaded")
            sys.exit(1)
        
        # Convert to audio (already done, just organize files)
        audio_files = convert_to_audio(downloaded_files)
        
        # Trim audio files
        trimmed_files = trim_audio(audio_files, duration)
        
        if len(trimmed_files) == 0:
            print("\n❌ Error: No audio files were trimmed")
            sys.exit(1)
        
        # Merge audio files
        merge_audios(trimmed_files, output_file)
        
        # Cleanup
        cleanup_temp_directories()
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ MASHUP COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"📊 Summary:")
        print(f"  Total videos downloaded : {len(downloaded_files)}")
        print(f"  Total audios trimmed    : {len(trimmed_files)}")
        print(f"  Final output file       : {os.path.abspath(output_file)}")
        print("=" * 60)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        cleanup_temp_directories()
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        cleanup_temp_directories()
        sys.exit(1)


if __name__ == "__main__":
    main()
