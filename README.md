# Telegram Media Downloader Bot

A powerful Telegram bot built with Python that leverages **yt-dlp** to download and process videos or audio from YouTube and other platforms directly into your chat.

---

## 🚀 Getting Started

### Prerequisites
Before you begin, ensure you have the following installed on your system (e.g., Ubuntu, macOS, or Windows):
* **Python 3.10+**
* **UV**: [Installaion Guide](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)
* **Telegram Bot Token**: Obtain this from [@BotFather](https://t.me/BotFather).
* **Telegram API ID**: Obtain from [Telegram Developer Login](https://my.telegram.org/auth)

### Installation

1. **Clone the Repository:**
   ```bash
   
   git clone https://github.com/cleontay/Telegram-Media-Downloader-Bot.git
   cd YTBot
   
   ```
   
2. **Configuration**
   ```bash
   
   # .env
   USERID=1234567890
   BOTTOKEN=XXXXX:YYYYYYYYY
   
   ```
   
3. **Export uv requirements**
   ```bash
   
   uv export --no-hashes --format requirements-txt > ./Docker/requirements.txt

   ```
   
4. **Build Image**
   ```bash

   docker build -t <appname>:<version> -f Docker/Dockerfile

   ```

5. **Docker compose configuration**
   ```bash
   
   docker compose up --build -d

   ```
   
6. **Usage**
   - Start a chat with the Telegram Bot
   - Type "/" and start using
