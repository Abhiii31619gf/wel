from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import os

# Bot Token
BOT_TOKEN = '8062163381:AAG6W37aDj50aSG8OHf4QJOtYmkDZzo5kzM'

# 🐱‍💻 Hacker-Style Welcome Message
WELCOME_MSG = """
╔═══════════════════╗
   🐱‍💻 𝐓𝐇𝐄 𝐌𝐀𝐒𝐓𝐄𝐑𝐁𝐇𝐀𝐈𝐘𝐀𝐀 𝐒𝐘𝐒𝐓𝐄𝐌 🖤
╚═══════════════════╝
  
[+] User Connected ✅  
[+] IP Tracing... ✅  
[+] Location: INDIA 🇮🇳  
[+] Target: {name}  
[+] Username: @{username}  
[+] User ID: {user_id}  
[+] Access Granted ✅  

🚩 Joining `Tᴇᴀᴍ Pʀᴏ Nᴇᴛᴡᴏʀᴋ...`
━━━━━━━━━━━━━━━━━━━
💀 𝑪𝒐𝒏𝒏𝒆𝒄𝒕𝒊𝒏𝒈 𝒕𝒐 𝑻𝒉𝒆 𝑻𝒆𝒓𝒎𝒊𝒏𝒂𝒍... ✅  
💀 𝑨𝒄𝒄𝒆𝒔𝒔 𝑮𝒓𝒂𝒏𝒕𝒆𝒅 ✅  
💀 𝑩𝒐𝒕 𝑺𝒆𝒄𝒖𝒓𝒊𝒕𝒚: 𝑨𝒄𝒕𝒊𝒗𝒆 🔥  
━━━━━━━━━━━━━━━━━━━

©️ 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐝 𝐛𝐲: @MasterBhaiyaa 🔱
"""

# Channel Links
CHANNEL_LINKS = [
    ("🔥 Main Channel 🔥", "https://t.me/+dzDDa69LRwNmMjA1"),
    ("💎 Chatting Group 💎", "https://t.me/team_pro_player"),
    ("🔱 Verified Sellers 🔱", "https://t.me/Verified_Sellers_Network"),
    ("🔱 Youtube Channel 🔱", "https://youtube.com/@official_proplayer?si=xtf1qVUgrTXxR6Rp"),
]

def get_profile_photo(bot, user_id):
    file_id = bot.get_user_profile_photos(user_id).photos[0][0].file_id
    new_file = bot.get_file(file_id)
    photo_path = f"{user_id}.jpg"
    new_file.download(photo_path)
    return photo_path

def welcome(update, context):
    new_members = update.message.new_chat_members
    for member in new_members:
        name = member.first_name or "User"
        username = member.username or "Unknown"
        user_id = member.id

        # Download Profile Photo
        try:
            photo_path = get_profile_photo(context.bot, user_id)
        except:
            photo_path = "default.jpg"  # If No Profile Picture
        
        # Create Buttons for Channel Links
        buttons = [
            [InlineKeyboardButton(text=name, url=url)] for name, url in CHANNEL_LINKS
        ]
        keyboard = InlineKeyboardMarkup(buttons)

        # Send the Hacker-Style Welcome Message with Profile Picture
        context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open(photo_path, 'rb'),
            caption=WELCOME_MSG.format(name=name, username=username, user_id=user_id),
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )

        # Delete the downloaded profile picture after sending
        if os.path.exists(photo_path):
            os.remove(photo_path)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
