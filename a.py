from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# Bot Token
BOT_TOKEN = '7949103650:AAGe5fAoTh4XueeZEdMhYS5EYEczVguEoac'
ADMIN_ID = 1077368861  # MasterBhaiyaa Admin ID

# Force Join Channels
CHANNEL_IDS = [
    '-1001837163384',  # Main Channel
    '-1001887095834',  # Chatting Group
    '-1002346945256',  # Verified Sellers
]

# Channel Links
CHANNEL_LINKS = [
    ("🔥 Main Channel 🔥", "https://t.me/+dzDDa69LRwNmMjA1"),
    ("💎 Chatting Group 💎", "https://t.me/team_pro_player"),
    ("🔱 Verified Sellers 🔱", "https://t.me/Verified_Sellers_Network"),
    ("🔱 YouTube Channel 🔱", "https://youtube.com/@official_proplayer?si=xtf1qVUgrTXxR6Rp"),
]

# Mafia Welcome Message
WELCOME_MSG = """
⫷🔥 𝐓𝐄𝐀𝐌 𝐏𝐑𝐎 𝐌𝐀𝐅𝐈𝐀 🔥⫸
┏━━━━━━━━━━━━━━━┓
💀 **𝑴𝒂𝒇𝒊𝒂 𝑯𝒂𝒄𝒌𝒆𝒓 𝑪𝒐𝒏𝒏𝒆𝒄𝒕𝒆𝒅** ✅  
👑 **𝑵𝒂𝒎𝒆:** {name}  
🔱 **Username:** @{username}  
🆔 **User ID:** {user_id}  
☠️ **Access: ✅ Granted**  
━━━━━━━━━━━━━━━
"""

FORCE_JOIN_MSG = """
⛓️ **𝑮𝑶𝑫𝑭𝑨𝑻𝑯𝑬𝑹 𝑹𝑼𝑳𝑬𝑺** 💀  
🎯 𝑱𝒐𝒊𝒏 𝑶𝑼𝑹 𝑴𝑨𝑭𝑰𝑨 𝑪𝑯𝑨𝑵𝑵𝑬𝑳𝑺 𝑻𝑶 𝑮𝑬𝑻 𝑨𝑪𝑪𝑬𝑺𝑺 👑

🚫 **Without Joining Channels You Can't Chat 🔥**  
"""

# Function to Check If User is in All Channels
def is_user_in_channels(context, user_id):
    for channel_id in CHANNEL_IDS:
        try:
            chat_member = context.bot.get_chat_member(channel_id, user_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

# Function to Get User Profile Picture
def get_profile_photo(bot, user_id):
    photos = bot.get_user_profile_photos(user_id)
    if photos.total_count > 0:
        file_id = photos.photos[0][0].file_id
        return file_id
    return None

# Welcome New Members
def welcome(update, context):
    new_members = update.message.new_chat_members
    for member in new_members:
        name = member.first_name or "User"
        username = member.username or "Unknown"
        user_id = member.id

        if is_user_in_channels(context, user_id):
            profile_pic = get_profile_photo(context.bot, user_id)
            if profile_pic:
                context.bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=profile_pic,
                    caption=WELCOME_MSG.format(name=name, username=username, user_id=user_id),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=WELCOME_MSG.format(name=name, username=username, user_id=user_id),
                    parse_mode=ParseMode.MARKDOWN
                )
        else:
            buttons = [
                [InlineKeyboardButton(text=name, url=url)] for name, url in CHANNEL_LINKS
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=FORCE_JOIN_MSG,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            context.bot.restrict_chat_member(update.message.chat_id, user_id, can_send_messages=False)

# Check Membership for Every Message
def check_membership(update, context):
    user_id = update.message.from_user.id
    if not is_user_in_channels(context, user_id):
        buttons = [
            [InlineKeyboardButton(text=name, url=url)] for name, url in CHANNEL_LINKS
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="❌ **You're Still Not in All Channels!** 🔥",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        context.bot.restrict_chat_member(update.message.chat_id, user_id, can_send_messages=False)
    else:
        context.bot.restrict_chat_member(update.message.chat_id, user_id, can_send_messages=True)

# Main Function to Run the Bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handle New Members
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    # Check Membership on Every Message
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_membership))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()