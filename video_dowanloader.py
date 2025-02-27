from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp
import os

# Replace with your own values | استبدل بالقيم الخاصة بك
API_ID = 'ENTER CODE '
API_HASH = 'ENTER HASH '
BOT_TOKEN = 'ENTER TOKEN FROM BOTFATHER '

# إنشاء العميل | Create client
app = Client("video_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# أمر لبدء المحادثة | Command to start conversation
@app.on_message(filters.command("start"))
def start(client: Client, message: Message):
    message.reply_text("send url ")

# أمر لتحميل الفيديو | Command to download video
@app.on_message(filters.text & ~filters.command("start"))
def download_video(client: Client, message: Message):
    try:
        url = message.text
        ydl_opts = {
            'format': 'best',  # أفضل جودة متاحة| Best quality available
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # حفظ الفيديو مع اسم الملف الأصلي | Save video with original file name
            'quiet': True,  # Hide unnecessary output | إخفاء output غير ضروري
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            message.reply_text("Loading...")
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

            message.reply_text("It is being sent")
            with open(file_path, "rb") as video_file:
                client.send_video(message.chat.id, video_file, caption="Sent successfully")

            # حذف الفيديو بعد الإرسال | Delete video after sending 
            os.remove(file_path)
    except Exception as e:
        message.reply_text(f"An error occurred: {e}")

# Turn on the bot  | تشغيل البوت
app.run()