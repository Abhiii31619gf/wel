from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Bot Token
BOT_TOKEN = '8062163381:AAG6W37aDj50aSG8OHf4QJOtYmkDZzo5kzM'

# Welcome Message
WELCOME_MSG = """
🔥 𝑾𝒆𝒍𝒄𝒐𝒎𝒆 𝒕𝒐 【T E A M P R O】 🔥

🌹 *तेरी यादों में कटती है मेरी रातें*
💎 *तेरे ख्वाबों में खो जाती हैं मेरी बातें*  
🖤 *मुझसे मत पूछ मेरे इश्क़ की हद क्या है,*  
🚩 *तेरी खुशी के लिए मैंने खुद को भी भुला दिया।*

💀 𝒀𝒐𝒖𝒓 𝑮𝒐𝒂𝒕 𝑰𝒏𝒇𝒐 💀
╭───────────────╮
🔥 𝐍𝐚𝐦𝐞: {name}
💎 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: @{username}
🔱 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}
╰───────────────╯
 
🚩 𝐉𝐨𝐢𝐧 𝐎𝐮𝐫 𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬:👇  
© @MasterBhaiyaa
"""

# Channel Links
CHANNEL_LINKS = [
    ("🔥 Main Channel 🔥", "https://t.me/+dzDDa69LRwNmMjA1"),
    ("💎 Chatting Group 💎", "https://t.me/team_pro_playerl"),
    ("🔱 Verified Sellers 🔱", "https://t.me/Verified_Sellers_Network"),
]

def welcome(update, context):
    new_members = update.message.new_chat_members
    for member in new_members:
        name = member.first_name or "User"
        username = member.username or "Unknown"
        user_id = member.id
        
        # Create Buttons for Channel Links
        buttons = [
            [InlineKeyboardButton(text=name, url=url)] for name, url in CHANNEL_LINKS
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        
        # Send the Welcome Message
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=WELCOME_MSG.format(name=name, username=username, user_id=user_id),
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()