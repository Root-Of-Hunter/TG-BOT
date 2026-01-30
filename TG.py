import telebot # lowercase 'i' হবে
from telebot import types
import sys

# বটের টোকেন
BOT_TOKEN = "8564510212:AAFe42aqhDqEsaeQfIqtJY6NVVwgs3m0U0c"
CHANNEL_USERNAME = "@rootofhunter" 

# বট ইনিশিয়ালাইজ করুন
bot = telebot.TeleBot(BOT_TOKEN)

# চ্যানেলের মেম্বার কিনা চেক করার ফাংশন
def is_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        # মেম্বার স্ট্যাটাস চেক
        return member.status in ['administrator', 'creator', 'member']
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    if is_member(user_id):
        welcome_text = f"স্বাগতম {message.from_user.first_name}!\n\nআপনি চ্যানেলের সদস্য হওয়ায় বট ব্যবহার করতে পারবেন।"
        bot.send_message(message.chat.id, welcome_text)
    else:
        markup = types.InlineKeyboardMarkup()
        channel_btn = types.InlineKeyboardButton("চ্যানেলে জয়িন করুন", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        check_btn = types.InlineKeyboardButton("✅ জয়িন হয়ে গেছি", callback_data="check_membership")
        markup.add(channel_btn, check_btn)
        
        bot.send_message(
            message.chat.id,
            f"হ্যালো {message.from_user.first_name}!\n\nবটটি ব্যবহার করার জন্য আপনাকে আমাদের চ্যানেলে জয়িন হতে হবে।",
            reply_markup=markup
        )

# কলব্যাক কুয়েরি হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "check_membership":
        user_id = call.from_user.id
        
        if is_member(user_id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f"ধন্যবাদ {call.from_user.first_name}! এখন বট ব্যবহার করতে পারবেন।")
        else:
            bot.answer_callback_query(call.id, "❌ আপনি এখনও জয়িন হননি!", show_alert=True)

# মেসেজ হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    
    if not is_member(user_id):
        markup = types.InlineKeyboardMarkup()
        channel_btn = types.InlineKeyboardButton("চ্যানেলে জয়িন করুন", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        check_btn = types.InlineKeyboardButton("✅ জয়িন হয়ে গেছি", callback_data="check_membership")
        markup.add(channel_btn, check_btn)
        
        bot.send_message(message.chat.id, "❌ প্রথমে চ্যানেলে জয়িন করুন!", reply_markup=markup)
        return
    
    bot.reply_to(message, "আপনার মেসেজ পাওয়া গেছে!")

# বট চালু করুন
if __name__ == "__main__":
    print("বট সফলভাবে চালু হয়েছে...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"বট বন্ধ হয়ে গেছে। কারণ: {e}")
