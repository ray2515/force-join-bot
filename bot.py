from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton

# ==============================
# 🔐 HARD-CODED SETTINGS
# ==============================

API_ID = 37540714  # your api_id from my.telegram.org
API_HASH = "add73db61e292c1702d16b0f664dbd0f"  # your api_hash
BOT_TOKEN = "8328949950:AAHuiUUoE5oNAcKdzwIhjBZlEljRb67gCFY"  # your bot token from @BotFather

CHANNEL_ID = -1002487079466  # your private channel id (starts with -100)
INVITE_LINK = "https://t.me/+IG7paWpyaLpiOWM9"  # your private channel invite link

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
            # PERMANENT MUTE until they join
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
# 🔓 AUTOMATIC UNMUTE WHEN USER JOINS CHANNEL
# ==============================
@app.on_chat_member_updated(filters.chat(CHANNEL_ID))
async def auto_unmute(client, update):
    user_id = update.from_user.id
    status = update.new_chat_member.status

    # Only unmute if user joined the channel
    if status in ["member", "administrator", "creator"]:
        try:
            async for dialog in client.get_dialogs():
                if dialog.chat.type in ["supergroup", "group"]:
                    try:
                        # Check if user is currently muted
                        member_info = await client.get_chat_member(dialog.chat.id, user_id)
                        if member_info.can_send_messages is False or member_info.status == "restricted":
                            # Unmute the user
                            await client.restrict_chat_member(
                                chat_id=dialog.chat.id,
                                user_id=user_id,
                                permissions=ChatPermissions(
                                    can_send_messages=True,
                                    can_send_media_messages=True,
                                    can_send_other_messages=True,
                                    can_add_web_page_previews=True
                                )
                            )
                            # Optional confirmation message
                            await client.send_message(
                                chat_id=dialog.chat.id,
                                text=f"✅ {update.from_user.mention} has joined the channel and is now unmuted!"
                            )
                    except Exception:
                        pass  # skip groups where bot can't unmute
        except Exception as e:
            print("Auto-unmute failed:", e)

# ==============================
# 🔓 INITIAL UNMUTE FOR EXISTING MEMBERS
# ==============================

    """Unmute all users who already joined the channel before bot start."""
    try:
        # Get all group dialogs
        async for dialog in client.get_dialogs():
            if dialog.chat.type in ["supergroup", "group"]:
                async for member in client.get_chat_members(dialog.chat.id):
                    if member.user.is_bot:
                        continue
                    # Check if user is in the channel
                    try:
                        channel_member = await client.get_chat_member(CHANNEL_ID, member.user.id)
                        if channel_member.status not in ["left", "kicked"]:
                            # Unmute user if restricted
                            if member.can_send_messages is False or member.status == "restricted":
                                await client.restrict_chat_member(
                                    chat_id=dialog.chat.id,
                                    user_id=member.user.id,
                                    permissions=ChatPermissions(
                                        can_send_messages=True,
                                        can_send_media_messages=True,
                                        can_send_other_messages=True,
                                        can_add_web_page_previews=True
                                    )
                                )
                    except:
                        pass
    except Exception as e:
        print("Initial unmute failed:", e)

# ==============================
# 🚀 START BOT
# ==============================
app.run()
