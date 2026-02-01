from pyrogram import Client, filters, errors
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIGURATION ---
API_ID = 37540714          
API_HASH = "add73db61e292c1702d16b0f664dbd0f"    
BOT_TOKEN = "8328949950:AAHuiUUoE5oNAcKdzwIhjBZlEljRb67gCFY"  
# For private channels, use the Peer ID (starts with -100)
PRIVATE_CHANNEL_ID = -1002487079466 
INVITE_LINK = "https://t.me/+IG7paWpyaLpiOWM9"

app = Client("MuteGatekeeper", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Permission sets
MUTE_PERMISSIONS = ChatPermissions(can_send_messages=False)
UNMUTE_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True
)

async def check_if_joined(user_id):
    try:
        member = await app.get_chat_member(PRIVATE_CHANNEL_ID, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except errors.UserNotParticipant:
        return False
    except Exception as e:
        print(f"Check Error: {e}")
    return False

@app.on_message(filters.group & ~filters.service)
async def enforce_mute(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # If they are already subscribed, do nothing
    if await check_if_joined(user_id):
        return

    # If not subscribed, mute them and notify
    try:
        await client.restrict_chat_member(chat_id, user_id, MUTE_PERMISSIONS)
        
        button = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔓 Join Private Channel", url=INVITE_LINK)
        ]])
        
        await message.reply_text(
            f"🔇 **{message.from_user.first_name}, you have been muted.**\n\n"
            "You cannot speak here until you join our private updates channel. "
            "Once you join, you will be unmuted automatically on your next attempt to chat.",
            reply_markup=button
        )
        # Optional: Delete the user's message that triggered the mute
        await message.delete()
        
    except errors.ChatAdminRequired:
        print("Error: Bot must be admin with 'Restrict Members' permission.")

# Handler to unmute users who have joined
@app.on_message(filters.group & filters.regex(r".*"))
async def check_for_unmute(client, message):
    user_id = message.from_user.id
    if await check_if_joined(user_id):
        await client.restrict_chat_member(message.chat.id, user_id, UNMUTE_PERMISSIONS)

app.run()
