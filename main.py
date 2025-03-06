import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Replace with your Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7923532245:AAEU6PMcm_ImVuELVoWV4H5iA2Qn0Fxxtyg"

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory to store downloaded videos
DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me a YouTube video link, and I'll download it for you!")

async def download_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Please send a valid YouTube video link!")
        return

    await update.message.reply_text("Downloading the video... Please wait.")

    # Video download options
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(info).replace(".webm", ".mp4")

        await update.message.reply_text("Download complete! Uploading video...")

        # Send the downloaded video
        with open(video_filename, "rb") as video:
            await update.message.reply_video(video)

        # Clean up the file
        os.remove(video_filename)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
