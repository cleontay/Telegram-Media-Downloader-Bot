import telebot
from telebot import apihelper
import requests
from telebot.types import BotCommand
from dotenv import load_dotenv
import os
import yt_dlp
import validators

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOTTOKEN")

class DownloadMode:
    AUDIO_MODE = "audio"
    VIDEO_MODE = "video"

bot = telebot.TeleBot(BOT_TOKEN)

apihelper.API_URL = "http://telegram-api-server:8081/bot{0}/{1}"

bot.set_my_commands([
    BotCommand("download_yt_video", "Download Youtube Video"),
    BotCommand("download_yt_audio", "Download Youtube Audio"),
])

def file_ext_check(filepath):
    filename, ext = os.path.splitext(filepath)
    if not ext:
        return f"{filename}.mp3"
    return filepath

def ytdlp_download_hook(d):
        """Simple progress hook function."""
        if d['status'] == 'downloading':
            print(f"Downloading: {d['_percent_str']} at {d['_speed_str']}")
        elif d['status'] == 'finished':
            print('Done downloading!')


def ytdlp_file_download(url, ydl_opts): 
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
        return file_ext_check(filename), info['title']

@bot.message_handler(commands=['download_yt_video'])
def download_yt_video(message):
    bot.send_message(message.chat.id, "Enter Youtube Link (URL)")
    bot.register_next_step_handler(message, handle_yt_download, DownloadMode.VIDEO_MODE)

@bot.message_handler(commands=['download_yt_audio'])
def download_yt_audio(message):
    bot.send_message(message.chat.id, "Enter Youtube Link (URL)")
    bot.register_next_step_handler(message, handle_yt_download, DownloadMode.AUDIO_MODE)

def handle_yt_download(message, mode):
    url = message.text # Replace with your video URL
    print(url)
    if validators.url(url):
        match mode:
            case DownloadMode.AUDIO_MODE:
                ydl_opts = {
                    # 'bestaudio' picks the highest quality audio stream available
                    'format': 'bestaudio/best',
                    # Post-processors to handle the audio conversion
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',      # Change to 'm4a' or 'wav' if preferred
                        'preferredquality': '192',    # Audio bitrate
                    }],
                    'outtmpl': {
                        'default': '/app/Downloads/' + '%(title)s',
                        'final_ext': 'mp3'
                    },
                    'noplaylist': True,
                    'progress_hooks': [ytdlp_download_hook],
                    # 'ffmpeg_location': FFMPEG_PATH, 
                }
            case DownloadMode.VIDEO_MODE:
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # Select best mp4 video and m4a audio, then merge
                    'merge_output_format': 'mp4', # Ensure the final container is mp4
                    'outtmpl': '/app/Downloads/' + '%(title)s.%(ext)s', # Output file name as the video title
                    'noplaylist': True, # Download only the single video if a playlist link is provided
                    'progress_hooks': [ytdlp_download_hook], # Add a hook to monitor progress
                    # 'ffmpeg_location': FFMPEG_PATH, # Uncomment and set if FFmpeg is not in PATH
                }
            case _:
                ydl_opts = None
        
        if ydl_opts is None:
            bot.reply_to(message, f"Mode: {mode} invalid")
            return
        
        filepath, title = ytdlp_file_download(url, ydl_opts)
        
        bot.reply_to(message, f"Downloading: {title}")
        
        with open(filepath, 'rb') as file:
            match mode:
                case DownloadMode.AUDIO_MODE:
                    bot.send_audio(
                        message.chat.id, 
                        file, 
                        timeout=3600
                    )
                case DownloadMode.VIDEO_MODE:
                    bot.send_video(
                        message.chat.id, 
                        file, 
                        timeout=3600
                    )
                case _:
                    bot.reply_to(message, f"Mode: {mode} invalid")
                    return

            os.remove(filepath)
    else:
        bot.reply_to(message, f"URL Unavailable: {url}")

bot.infinity_polling()