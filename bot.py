import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.getenv("37540714"))
API_HASH = os.getenv("add73db61e292c1702d16b0f664dbd0f")
BOT_TOKEN = os.getenv("8328949950:AAHuiUUoE5oNAcKdzwIhjBZlEljRb67gCFY")

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
        await message.delete()
        await message.reply(
            "🚫 To send messages in this group, you must join our channel.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Join Channel", url=INVITE_LINK)]
            ])
        )

app.run()
