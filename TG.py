import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserNotParticipant, ChatAdminRequired

# ------------------ CONFIG ------------------
# আপনার বটের টোকেন এখানে দিন
BOT_TOKEN = "7148954721:AAEhqU9v5bARNNPD11NI1zSy4kaCMjUbx6U" 

# এই API_ID এবং API_HASH পরিবর্তন করবেন না, এগুলো কাজ করবে
API_ID = 26526978 
API_HASH = "80983a5f973715c9071066551061972f"

# আপনার দেওয়া ফটো লিঙ্ক
PHOTO_URL = "https://t.me/roh_x_vip/3" 

# আপনার চ্যানেলের ইউজারনেমগুলো এখানে দিন
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
    name="root_of_hunter",
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
            f"এখন বটের সব ফিচার ব্যবহার করতে পারবেন।"
        )
        buttons = [
            [InlineKeyboardButton("🚀 MAIN MENU", callback_data="main_menu")],
            [InlineKeyboardButton("💎 VIP SECTION", callback_data="vip_section")],
        ]
    else:
        text = (
            f"✨ **PREMIUM AUTHENTICATION** ✨\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👋 **হ্যালো** {user_mention}\n\n"
            f"বটটি ব্যবহার করতে নিচের ৪টি চ্যানেলে জয়েন করুন।\n"
            f"জয়েন করে **YES** বাটনে ক্লিক করুন।\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        buttons = [
            [
                InlineKeyboardButton("📢 Ch 1", url=f"https://t.me/{CHANNELS[0].lstrip('@')}"),
                InlineKeyboardButton("🚀 Ch 2", url=f"https://t.me/{CHANNELS[1].lstrip('@')}"),
            ],
            [
                InlineKeyboardButton("💎 Ch 3", url=f"https://t.me/{CHANNELS[2].lstrip('@')}"),
                InlineKeyboardButton("🔥 Ch 4", url=f"https://t.me/{CHANNELS[3].lstrip('@')}"),
            ],
            [InlineKeyboardButton("🌟 YES I'VE JOINED", callback_data="check_join")],
            [InlineKeyboardButton("👨‍💻 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}")],
        ]

    try:
        # ফটো পাঠানোর চেষ্টা করবে
        await message.reply_photo(photo=PHOTO_URL, caption=text, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception:
        # ফটোতে সমস্যা হলে শুধু টেক্সট পাঠাবে যাতে এরর না আসে
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))

# ------------------ CALLBACK HANDLER ------------------

@app.on_callback_query()
async def cb_handler(client: Client, cq: CallbackQuery):
    user_id = cq.from_user.id
    
    if cq.data == "check_join":
        if await is_user_joined_all(user_id):
            await cq.answer("✅ Access Granted!", show_alert=True)
            await cq.edit_message_caption(
                "🎉 আপনি সফলভাবে ভেরিফাইড হয়েছেন!\nএখন বটের সব ফিচার উপভোগ করুন।", 
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 MAIN MENU", callback_data="main_menu")]])
            )
        else:
            await cq.answer("❌ আপনি সব চ্যানেলে জয়েন করেননি!", show_alert=True)
    
    elif cq.data == "main_menu":
        await cq.edit_message_caption(
            "🏠 **MAIN MENU**\n\nআপনার জন্য ফিচারগুলো শীঘ্রই আসছে।", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]])
        )
    
    elif cq.data == "back_to_start":
        # এখানে সরাসরি start ফাংশনকে কল না করে মেসেজ এডিট করা ভালো
        await cq.edit_message_caption("ফিরে আসা হচ্ছে...", reply_markup=None)
        await start(client, cq.message)

if __name__ == "__main__":
    print("---------------------------------")
    print("Bot is Starting Successfully!")
    print("---------------------------------")
    app.run()
