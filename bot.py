import os
import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

def main_menu_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🔍 Browse Freelancers"), KeyboardButton("📌 Post a Job")],
        [KeyboardButton("🗂 Categories"), KeyboardButton("⭐ Upgrade to Pro")],
        [KeyboardButton("📊 My Dashboard"), KeyboardButton("🛟 Help Center")]
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    welcome_text = f"""
🤖 Welcome to *FreelanceHub*!

Hello {user.first_name}! 👋

The global freelance marketplace powered by crypto.

*Choose an option below:*
🔍 **Browse Freelancers** - Find talented professionals
📌 **Post a Job** - Hire for your projects  
🗂 **Categories** - Explore all skill categories
⭐ **Upgrade to Pro** - Unlock premium features
📊 **My Dashboard** - Manage your account
🛟 **Help Center** - Get support

*Ready to get started?*
"""
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard(), parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🔍 Browse Freelancers":
        await update.message.reply_text(
            "👥 *Browse Freelancers*\n\n🔧 **Coming Soon!**\n\nYou'll be able to search and filter freelancers by category, rating, and skills.\n\nStay tuned! 🚀", 
            parse_mode='Markdown'
        )
    elif text == "📌 Post a Job":
        await update.message.reply_text(
            "📝 *Post a Job*\n\n🔧 **Coming Soon!**\n\nYou'll be able to create job posts, set budgets in USDT/TON, and receive proposals from freelancers.\n\nComing very soon! 💼", 
            parse_mode='Markdown'
        )
    elif text == "🗂 Categories":
        await update.message.reply_text(
            "🏷️ *FreelanceHub Categories*\n\n*Available Categories:*\n\n🎨 Graphic Design\n✍️ Writing & Copywriting\n🌍 Translation\n💻 Programming & Tech\n🎬 Video & Audio Editing\n🤖 AI Services\n📈 Marketing & Business\n🛡️ Cyber Security (PRO)", 
            parse_mode='Markdown'
        )
    elif text == "⭐ Upgrade to Pro":
        await update.message.reply_text(
            "⭐ *FreelanceHub PRO*\n\n🚀 **Premium Features Coming Soon!**\n\n• Top placement in search\n• Priority notifications\n• PRO badge\n• Analytics dashboard\n• Premium categories\n\n*Price:* 10 USDT/month", 
            parse_mode='Markdown'
        )
    elif text == "📊 My Dashboard":
        user = update.message.from_user
        await update.message.reply_text(
            f"📊 *Your Dashboard*\n\n👤 **Welcome {user.first_name}!**\n\n💼 **Account Status:** Basic Member\n💰 **Balance:** 0 USDT\n🚀 **Complete your profile to get started!**", 
            parse_mode='Markdown'
        )
    elif text == "🛟 Help Center":
        await update.message.reply_text(
            "🛟 *Help Center*\n\n*Need assistance?*\n\n• How to post jobs\n• How to find freelancers\n• Payment methods: USDT & TON\n• Security features\n• Contact support\n\nWe're here to help! 🌐", 
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("Please use the menu buttons below! 👇", reply_markup=main_menu_keyboard())

def main():
    # Create Telegram bot application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the Bot
    print("🤖 FreelanceHub Bot Starting...")
    print("✅ Bot is LIVE and running!")
    application.run_polling()

if __name__ == '__main__':
    main()
