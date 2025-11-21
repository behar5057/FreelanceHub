import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
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
    user = update.effective_user
    
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
            "👥 *Browse Freelancers*\n\n🔧 **Coming Soon!**\n\nYou'll be able to:\n• Search freelancers by category\n• Filter by rating and skills\n• View portfolios and reviews\n• Contact top talent directly\n\nStay tuned! 🚀", 
            parse_mode='Markdown'
        )
    elif text == "📌 Post a Job":
        await update.message.reply_text(
            "📝 *Post a Job*\n\n🔧 **Coming Soon!**\n\nYou'll be able to:\n• Create detailed job posts\n• Set your budget in USDT/TON\n• Choose from 8+ categories\n• Receive proposals from freelancers\n• Use secure escrow payments\n\nComing very soon! 💼", 
            parse_mode='Markdown'
        )
    elif text == "🗂 Categories":
        await update.message.reply_text(
            "🏷️ *FreelanceHub Categories*\n\n*Available Categories:*\n\n🎨 **Graphic Design**\n• Logos & Branding\n• Social Media Graphics\n• Packaging Design\n\n✍️ **Writing & Copywriting**\n• Content Writing\n• Blog Posts\n• Script Writing\n\n🌍 **Translation**\n• Multiple Languages\n• Document Translation\n• Localization\n\n💻 **Programming & Tech**\n• Website Development\n• Mobile Apps\n• APIs & Bots\n\n🎬 **Video & Audio Editing**\n• Video Production\n• Podcast Editing\n• Music Production\n\n🤖 **AI Services**\n• Image Generation\n• AI Chatbots\n• Prompt Engineering\n\n📈 **Marketing & Business**\n• SEO Optimization\n• Social Media Marketing\n• Business Plans\n\n🛡️ **Cyber Security** (PRO)\n• Penetration Testing\n• Security Audits\n• Vulnerability Assessment", 
            parse_mode='Markdown'
        )
    elif text == "⭐ Upgrade to Pro":
        await update.message.reply_text(
            "⭐ *FreelanceHub PRO Subscription*\n\n🚀 **Unlock Premium Features**\n\n*For just 10 USDT/month, get:*\n\n✅ **Top Placement** in search results\n✅ **Priority Notifications** for new jobs\n✅ **Exclusive PRO Badge** on your profile\n✅ **Full Analytics** dashboard\n✅ **Faster Acceptance** on high-value jobs\n✅ **Access to Premium Categories** like Cyber Security\n✅ **Increased Visibility** to clients\n\n*Payment Methods:*\n• USDT (TRC20)\n• TON (Telegram Wallet)\n\n🔧 **PRO subscriptions coming soon!**", 
            parse_mode='Markdown'
        )
    elif text == "📊 My Dashboard":
        user = update.effective_user
        await update.message.reply_text(
            f"📊 *Your Dashboard*\n\n👤 **Account Info**\n• Name: {user.first_name} {user.last_name or ''}\n• Username: @{user.username or 'Not set'}\n• Status: Basic Member\n\n💼 **Freelance Stats**\n• Jobs Posted: 0\n• Jobs Completed: 0\n• Total Earnings: 0 USDT\n• Member Since: Today!\n\n🚀 **Quick Actions**\n• Complete your profile\n• Set your skills\n• Add portfolio items\n• Set your hourly rate\n\n🔧 **Full dashboard coming soon!**", 
            parse_mode='Markdown'
        )
    elif text == "🛟 Help Center":
        await update.message.reply_text(
            "🛟 *FreelanceHub Help Center*\n\n*For Clients:*\n• How to post jobs and hire talent\n• Payment methods and security\n• Managing your projects\n\n*For Freelancers:*\n• Creating your profile\n• Finding and bidding on jobs\n• Getting paid securely\n\n*Payment Methods:*\n💰 **USDT (TRC20)** - Fast, low fees\n⚡ **TON** - Instant Telegram payments\n\n*Security Features:*\n🔒 **Escrow System** - Funds held securely\n⭐ **Rating System** - Build your reputation\n📞 **Support** - Always here to help\n\n*Need immediate assistance?*\nContact our support team through this bot!\n\n🌐 *FreelanceHub - Building the future of work!*", 
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("Please use the menu buttons below! 👇", reply_markup=main_menu_keyboard())

def main():
    # Create bot application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 FreelanceHub Bot Starting...")
    print("✅ Bot is LIVE and running!")
    application.run_polling()

if __name__ == '__main__':
    main()
