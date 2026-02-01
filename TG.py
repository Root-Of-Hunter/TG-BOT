import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserNotParticipant, ChatAdminRequired

# ------------------ CONFIG ------------------
# এখানে আপনার বটের টোকেন দিন
BOT_TOKEN = "7148954721:AAEhqU9v5bARNNPD11NI1zSy4kaCMjUbx6U" 

# এগুলো ডিফল্ট, পরিবর্তন করার দরকার নেই
API_ID = 26526978 
API_HASH = "80983a5f973715c9071066551061972f"

# আপনার দেওয়া নতুন ফটো লিঙ্ক
PHOTO_URL = "https://t.me/roh_x_vip/3" 

# আপনার চ্যানেলগুলোর ইউজারনেম দিন (বটকে অবশ্যই এডমিন করতে হবে)
CHANNELS = [
    "@Link_1",          
    "@Link_2",          
    "@Link_3",          
    "@Link_4",          
]

VIP_LINK = "https://t.me/your_vip_link"
ADMIN_USERNAME = "your_admin_username"

# ------------------ Logging ------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

joined_users = {}

app = Client(
    name="root_hunter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ------------------ FUNCTIONS ------------------

async def is_user_joined_all(user_id: int) -> bool:
    if user_id in joined_users:
        return True
    for channel in CHANNELS:
        try:
            member = await app.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except (UserNotParticipant, ChatAdminRequired):
            return False
        except Exception:
            return False
    joined_users[user_id] = True
    return True

# ------------------ START COMMAND ------------------

@app.on_message(filters.private & filters.command("start"))
async def start(client: Client, message):
    user_id = message.from_user.id
    user_mention = message.from_user.mention

    if await is_user_joined_all(user_id):
        text = (
            f"✨ **WELCOME BACK** {user_mention} ✨\n\n"
            f"🎉 আপনি সফলভাবে ভেরিফাইড আছেন।\n"
            f"নিচের মেনু থেকে ফিচারগুলো ব্যবহার করুন।"
        )
        buttons = [
            [InlineKeyboardButton("🚀 MAIN MENU", callback_data="main_menu")],
            [InlineKeyboardButton("💎 VIP SECTION", callback_data="vip_section")],
            [InlineKeyboardButton("👨‍💻 Admin", url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}")],
        ]
    else:
        text = (
            f"✨ **PREMIUM AUTHENTICATION** ✨\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👋 **হ্যালো** {user_mention}\n\n"
            f"বটটি ব্যবহার করতে নিচের ৪টি চ্যানেলে জয়েন করুন।\n"
            f"জয়েন শেষ হলে **YES** বাটনে ক্লিক করুন।\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        buttons = [
            [
                InlineKeyboardButton("📢 Ch 1", url=f"https://t.me/rootofhunter{CHANNELS[0].lstrip('@')}"),
                InlineKeyboardButton("🚀 Ch 2", url=f"https://t.me/Rootofhunter_V1{CHANNELS[1].lstrip('@')}"),
            ],
            [
                InlineKeyboardButton("💎 Ch 3", url=f"https://t.me/+H3wWMPUq4Zo0MWJl{CHANNELS[2].lstrip('@')}"),
                InlineKeyboardButton("🔥 Ch 4", url=f"https://t.me/ROH_VIP_MOOD_APPS{CHANNELS[3].lstrip('@')}"),
            ],
            [InlineKeyboardButton("🌟 YES I'VE JOINED", callback_data="check_join")],
            [InlineKeyboardButton("👨‍💻 Contact Admin", url=f"https://t.me/Xyz_Zico{ADMIN_USERNAME.lstrip('@')}")],
        ]

    try:
        await message.reply_photo(photo=PHOTO_URL, caption=text, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        logger.error(f"Photo error: {e}")
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))

# ------------------ CALLBACK HANDLER ------------------

@app.on_callback_query()
async def cb_handler(client: Client, cq: CallbackQuery):
    if cq.data == "check_join":
        if await is_user_joined_all(cq.from_user.id):
            await cq.answer("✅ Access Granted!", show_alert=True)
            await cq.edit_message_caption(
                "🎉 আপনি সফলভাবে ভেরিফাইড হয়েছেন!\nএখন বটের সব ফিচার উপভোগ করুন।", 
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 MAIN MENU", callback_data="main_menu")]])
            )
        else:
            await cq.answer("❌ আপনি সব চ্যানেলে জয়েন করেননি!", show_alert=True)
    
    elif cq.data == "main_menu":
        await cq.edit_message_caption(
            "🏠 **MAIN MENU**\n\nআপনার প্রয়োজনীয় টুলসগুলো এখানে পাবেন।", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]])
        )
    
    elif cq.data == "back_to_start":
        await start(client, cq.message)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
