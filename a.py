from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, ChatMember
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from pytz import utc  # Fixed Import for APScheduler Timezone

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

# Force Join Message
FORCE_JOIN_MSG = """
⛓️ **𝑮𝑶𝑫𝑭𝑨𝑻𝑯𝑬𝑹 𝑹𝑼𝑳𝑬𝑺** 💀  
🎯 𝑱𝒐𝒊𝒏 𝑶𝑼𝑹 𝑴𝑨𝑭𝑰𝑨 𝑪𝑯𝑨𝑵𝑵𝑬𝑳𝑺 𝑻𝑶 𝑮𝑬𝑻 𝑨𝑪𝑪𝑬𝑺𝑺 👑

🚫 **Without Joining Channels You Can't Chat 🔥**  
"""

# ✅ Check if User is in All Channels
async def is_user_in_channels(context: CallbackContext, user_id):
    for channel_id in CHANNEL_IDS:
        try:
            chat_member = await context.bot.get_chat_member(channel_id, user_id)
            if chat_member.status in [ChatMember.LEFT, ChatMember.KICKED]:
                return False
        except:
            return False
    return True

# ✅ Fetch User Profile Picture
async def get_profile_photo(context: CallbackContext, user_id):
    photos = await context.bot.get_user_profile_photos(user_id)
    if photos.total_count > 0:
        file_id = photos.photos[0][0].file_id
        return file_id
    return None

# ✅ Force Join Welcome Function
async def welcome(update, context):
    new_members = update.message.new_chat_members
    for member in new_members:
        name = member.first_name or "User"
        username = member.username or "Unknown"
        user_id = member.id

        if await is_user_in_channels(context, user_id):
            profile_pic = await get_profile_photo(context, user_id)

            if profile_pic:
                await context.bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=profile_pic,
                    caption=WELCOME_MSG.format(name=name, username=username, user_id=user_id),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text(
                    text=WELCOME_MSG.format(name=name, username=username, user_id=user_id),
                    parse_mode=ParseMode.MARKDOWN
                )
        else:
            buttons = [
                [InlineKeyboardButton(text=name, url=url)] for name, url in CHANNEL_LINKS
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(
                text=FORCE_JOIN_MSG,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            await context.bot.restrict_chat_member(update.message.chat_id, user_id, can_send_messages=False)

# ✅ Check Membership After Sending Message
async def check_membership(update, context):
    user_id = update.message.from_user.id
    
    if not await is_user_in_channels(context, user_id):
        buttons = [
            [InlineKeyboardButton(text=name, url=url)] for name, url in CHANNEL_LINKS
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(
            text="❌ **You're Still Not in All Channels! 🔥**",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        await context.bot.restrict_chat_member(update.message.chat_id, user_id, can_send_messages=False)
    else:
        await context.bot.restrict_chat_member(update.message.chat_id, user_id, can_send_messages=True)

# ✅ Start Command for Admin
async def start(update, context):
    if update.message.from_user.id == ADMIN_ID:
        await update.message.reply_text("👑 **Mafia Bot Successfully Started ✅**")
    else:
        await update.message.reply_text("🔒 **Access Denied!**")

# ✅ Main Bot Function
async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ✅ Fixed APScheduler Timezone Error
    application.job_queue.scheduler.configure(timezone=utc)

    # Add Handlers
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_membership))
    application.add_handler(CommandHandler("start", start))

    # Run the Bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
