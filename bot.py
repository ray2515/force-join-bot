import os
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton

# ==============================
# 🔐 ENV VARIABLES
# ==============================
# Make sure these are set in Railway Service → Variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))      # e.g., -1001234567890
INVITE_LINK = os.getenv("INVITE_LINK")        # e.g., https://t.me/+xxxx

# ==============================
# 🤖 BOT INIT
# ==============================
app = Client(
    "force_join_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ==============================
# 🔒 FORCE JOIN + PERMANENT MUTE
# ==============================
@app.on_message(filters.group & ~filters.service)
async def force_join(client, message):
    if not message.from_user:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        member = await client.get_chat_member(CHANNEL_ID, user_id)

        if member.status in ["left", "kicked"]:
            raise Exception

    except:
        try:
            # 🔒 PERMANENT MUTE
            await client.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False
                )
            )

            await message.reply(
                "🚫 You must join our channel to chat here.\n🔒 You are muted until you join.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Join Channel", url=INVITE_LINK)]
                ])
            )

        except Exception as e:
            print("Mute failed:", e)

# ==============================
# 🔓 UNMUTE COMMAND AFTER JOIN
# ==============================
@app.on_message(filters.command("unmute") & filters.group)
async def unmute_user(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        member = await client.get_chat_member(CHANNEL_ID, user_id)

        if member.status not in ["left", "kicked"]:
            await client.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )
            await message.reply("✅ You joined the channel. You are unmuted.")
        else:
            await message.reply("❌ Join the channel first.")

    except Exception as e:
        print("Unmute error:", e)

# ==============================
# 🚀 START BOT
# ==============================
app.run()


