from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# আপনার দেওয়া ডিটেইলস
API_ID = 35383192
API_HASH = "c895107fcf3589b9fa224638e7817a31"
BOT_TOKEN = "7148954721:AAEhqU9v5bARNNPD11NI1zSy4kaCMjUbx6U"

app = Client("root_of_hunter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    photo_url = "https://t.me/PRIMEBACKUPP/29" 
    
    text = (
        f"✨ **PREMIUM AUTHENTICATION** ✨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 **স্বাগতম** {message.from_user.mention}\n\n"
        f"বটটি ব্যবহার করতে নিচের ৪টি চ্যানেলে জয়েন থাকা বাধ্যতামূলক।\n"
        f"জয়েন করার পর আপনার পছন্দের মোডটি সিলেক্ট করুন।\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )

    # ৪টি চ্যানেল এবং YES/NO বাটন গ্রিড
    buttons = [
        [
            InlineKeyboardButton("📢 Channel 1", url="https://t.me/rootofhunter"),
            InlineKeyboardButton("🚀 Channel 2", url="https://t.me/Rootofhunter_V1")
        ],
        [
            InlineKeyboardButton("💎 Channel 3", url="https://t.me/+PG34lOvCkdc2YmQ1"),
            InlineKeyboardButton("🔥 Channel 4", url="https://t.me/roh_hacking")
        ],
        [
            InlineKeyboardButton("🌟 YES (JOIN VIP)", callback_data="run_yes"),
            InlineKeyboardButton("🛡️ NO (CONTINUE)", callback_data="run_no")
        ],
        [
            InlineKeyboardButton("👨‍💻 ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ", url="https://t.me/Xyz_Zico")
        ]
    ]

    await message.reply_photo(
        photo=photo_url,
        caption=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    
    if data == "run_yes":
        await callback_query.answer("Processing VIP Request...", show_alert=False)
        vip_text = (
            "💎 **WELCOME TO VIP SECTION** 💎\n\n"
            "আপনি VIP মেম্বারশিপের জন্য আবেদন করেছেন। নিচের বাটনে ক্লিক করে VIP চ্যানেলে প্রবেশ করুন।"
        )
        await callback_query.edit_message_caption(
            caption=vip_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 JOIN VIP CONTACT", url="https://t.me/Xyz_Zico")],
                [InlineKeyboardButton("🔙 BACK", callback_data="back_to_start")]
            ])
        )

    elif data == "run_no":
        await callback_query.answer("Access Granted ✅", show_alert=False)
        await callback_query.edit_message_caption(
            caption="✅ **Access Granted!**\n\nআপনি সাধারণ ইউজার হিসেবে বটটি সফলভাবে চালু করেছেন। এখন আপনি কাজ শুরু করতে পারেন।",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 START USING", callback_data="main_menu")]])
        )

    elif data == "back_to_start":
        await start(client, callback_query.message)

print("Root Of Hunter Bot with 4 Channels is Live! 🔥")
app.run()
