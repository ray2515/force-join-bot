import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = -1002487079466  # your private channel ID
INVITE_LINK = "https://t.me/+IG7paWpyaLpiOWM9"

app = Client(
    "join_required_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.group & ~filters.service)
async def enforce_join(client, message):
    user_id = message.from_user.id

    try:
        member = await client.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ["left", "kicked"]:
            raise Exception
    except:
        from pyrogram.types import ChatPermissions
import time

@app.on_message(filters.group & ~filters.service)
async def enforce_join(client, message):
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
            # 🔇 Mute user for 5 minutes
            await client.restrict_chat_member(
                chat_id,
                user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=None
            )

            await message.reply(
                "🚫 Join our channel to chat here.\n\n🔇 You are muted for 5 minutes.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Join Channel", url=INVITE_LINK)]
                ])
            )
        except:
            pass
        await message.reply(
            "🚫 To send messages in this group, you must join our channel.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Join Channel", url=INVITE_LINK)]
            ])
        )

app.run()
