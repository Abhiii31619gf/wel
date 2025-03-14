import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import signal

# Logging Configuration
logging.basicConfig(level=logging.INFO)

# Bot Configuration
BOT_TOKEN = os.getenv('7949103650:AAGe5fAoTh4XueeZEdMhYS5EYEczVguEoac')
ADMIN_ID = int(os.getenv('1077368861'))

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

# Welcome Message
WELCOME_MSG = """
⫷🔥 𝐓𝐄𝐀𝐌 𝐌𝐀𝐅𝐈𝐀 🔥⫸
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
🎯 𝑱𝒐𝒊𝒏 𝑶𝑼𝑹 𝑴𝑨𝑭𝑰𝑨 𝑪𝑯𝑨𝑵𝑵𝑬𝒍𝑺 𝑻𝑶 𝑮𝑬𝑻 𝑨𝑪𝑪𝑬𝑺𝑺 👑
🚫 **Without Joining Channels You Can't Chat 🔥**  
"""

async def is_user_in_channels(context: CallbackContext, user_id):
    for channel_id in CHANNEL_IDS:
        try:
            chat_member = await context.bot.get_chat_member(channel_id, user_id)
            if chat_member.status in [ChatMember.LEFT, ChatMember.KICKED]:
                return False
        except Exception as e:
            logging.error(f"Error checking membership for user {user_id} in channel {channel_id}: {e}")
            return False
    return True

async def welcome(update, context):
    new_members = update.message.new_chat_members
    for member in new_members:
        name = member.first_name or "User"
        username = member.username or "Unknown"
        user_id = member.id

        if await is_user_in_channels(context, user_id):
            await update.message.reply_text(
                text=WELCOME_MSG.format(name=name, username=username, user_id=user_id),
                parse_mode="Markdown"
            )
        else:
            buttons = [
                [InlineKeyboardButton(text=name, url=url)] for name, url in CHANNEL_LINKS
            ]
            buttons.append([InlineKeyboardButton("✅ Verify Membership", callback_data="verify_membership")])
            keyboard = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(
                text=FORCE_JOIN_MSG,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            await context.bot.restrict_chat_member(update.message.chat_id, user_id, can_send_messages=False)

async def verify_membership(update, context):
    query = update.callback_query
    user_id = query.from_user.id

    if await is_user_in_channels(context, user_id):
        await query.answer("✅ You're now verified!")
        await context.bot.restrict_chat_member(update.message.chat_id, user_id, can_send_messages=True)
    else:
        await query.answer("❌ You're still not in all channels!")

async def check_membership(update, context):
    user_id = update.message.from_user.id
    
    if not await is_user_in_channels(context, user_id):
        buttons = [
            [InlineKeyboardButton(text=name, url=url)] for name, url in CHANNEL_LINKS
        ]
        buttons.append([InlineKeyboardButton("✅ Verify Membership", callback_data="verify_membership")])
        keyboard = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(
            text="❌ **You're Still Not in All Channels! 🔥**",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        await context.bot.restrict_chat_member(update.message.chat_id, user_id, can_send_messages=False)
    else:
        await context.bot.restrict_chat_member(update.message.chat_id, user_id, can_send_messages=True)

async def start(update, context):
    if update.message.from_user.id == ADMIN_ID:
        await update.message.reply_text("👑 **Mafia Bot Successfully Started ✅**")
    else:
        await update.message.reply_text("🔒 **Access Denied!**")

async def main():
    scheduler = AsyncIOScheduler(timezone=pytz.utc)
    application = Application.builder().token(BOT_TOKEN).build()

    # Add Handlers
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_membership))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(verify_membership, pattern="verify_membership"))

    # Run the Bot
    await application.run_polling()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda s, f: asyncio.create_task(shutdown(application)))
    signal.signal(signal.SIGTERM, lambda s, f: asyncio.create_task(shutdown(application)))
    asyncio.run(main())
