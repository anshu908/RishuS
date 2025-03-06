import logging
from googleapiclient.discovery import build
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# API Keys (Replace with your own keys)
TELEGRAM_BOT_TOKEN = "7923532245:AAEU6PMcm_ImVuELVoWV4H5iA2Qn0Fxxtyg"
YOUTUBE_API_KEY = "AIzaSyDpLR48lIr-o88sG7b3-xE4LXZhWo_pN2Y"

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def search_youtube(query):
    """Search YouTube for a video and return the first result link"""
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(q=query, part="snippet", maxResults=1, type="video")
    response = request.execute()

    if "items" in response and len(response["items"]) > 0:
        video_id = response["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return "No results found. Try a different keyword."

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me any video name, and I'll fetch its YouTube link!")

async def handle_message(update: Update, context: CallbackContext) -> None:
    query = update.message.text
    video_link = search_youtube(query)
    await update.message.reply_text(video_link)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
