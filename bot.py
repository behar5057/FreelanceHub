import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from config import Config
from database import init_db, Session, User

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main_menu_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🔍 Browse Freelancers"), KeyboardButton("📌 Post a Job")],
        [KeyboardButton("🗂 Categories"), KeyboardButton("⭐ Upgrade to Pro")],
        [KeyboardButton("📊 My Dashboard"), KeyboardButton("🛟 Help Center")]
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Save user to database
    with Session() as session:
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        if not db_user:
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name or ""
            )
            session.add(db_user)
            session.commit()
            print(f"✅ New user registered: {user.username}")
    
    welcome_text = """
🤖 Welcome to *FreelanceHub*!

The global marketplace where talent meets opportunity, powered by crypto.

*What would you like to do?*

🔍 *Browse Freelancers* - Find vetted experts for your project
📌 *Post a Job* - Start a new project listing  
🗂 *Categories* - Explore all skills and services
⭐ *Upgrade to Pro* - Unlock premium features
📊 *My Dashboard* - Manage your jobs & earnings
🛟 *Help Center* - Get support

*Choose an option below to begin!*
"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🔍 Browse Freelancers":
        await update.message.reply_text("👥 *Browse Freelancers*\n\nFeature coming soon! You'll be able to search and filter freelancers by category, rating, and budget.", parse_mode='Markdown')
    elif text == "📌 Post a Job":
        await update.message.reply_text("📝 *Post a Job*\n\nJob posting system coming soon! You'll be able to create job posts, set budgets, and find perfect freelancers.", parse_mode='Markdown')
    elif text == "🗂 Categories":
        await show_categories(update, context)
    elif text == "⭐ Upgrade to Pro":
        await show_pro_subscription(update, context)
    elif text == "📊 My Dashboard":
        await show_dashboard(update, context)
    elif text == "🛟 Help Center":
        await help_command(update, context)
    else:
        await update.message.reply_text("Please use the menu buttons below!", reply_markup=main_menu_keyboard())

async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories_text = """
🏷️ *FreelanceHub Categories*

*Available Categories:*
• 🎨 Graphic Design
• ✍️ Writing & Copywriting  
• 🌍 Translation
• 💻 Programming & Tech
• 🎬 Video & Audio Editing
• 🤖 AI Services
• 📈 Marketing & Business
• 🛡️ Cyber Security (PRO)

Select a category from the menu to browse freelancers or post jobs!
"""
    await update.message.reply_text(categories_text, parse_mode='Markdown')

async def show_pro_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pro_text = """
⭐ *FreelanceHub PRO Subscription*

Unlock the full potential of your freelance business!

*For just 10 USDT/month, get:*
✓ **Top Placement** in search results
✓ **Priority Notifications** for new jobs  
✓ **Exclusive PRO Badge** on your profile
✓ **Full Analytics** dashboard
✓ **Faster Acceptance** on high-value jobs
✓ **Access to Premium Categories** like Cyber Security

*Ready to boost your earnings?*

Payment integration coming soon!
"""
    await update.message.reply_text(pro_text, parse_mode='Markdown')

async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    with Session() as session:
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        
        if db_user:
            dashboard_text = f"""
📊 *Your Dashboard*

*Account Info:*
• User: {db_user.first_name} {db_user.last_name}
• Type: {db_user.user_type.title()}
• Balance: {db_user.balance:.2f} USDT
• Member Since: {db_user.created_at.strftime('%Y-%m-%d')}

*Quick Stats:*
• Jobs Posted: 0
• Jobs Completed: 0
• Total Earnings: 0 USDT

*What would you like to do?*
• Create freelancer profile
• Post your first job
• Browse available work
• Check your transactions
"""
        else:
            dashboard_text = "❌ Error loading dashboard. Please try /start again."
    
    await update.message.reply_text(dashboard_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🛟 *FreelanceHub Help Center*

*For Clients:*
• Use *Post a Job* to create new projects
• Pay with USDT or TON securely
• Funds held in escrow until work approval

*For Freelancers:*
• Create your professional profile
• Browse categories to find work
• Submit proposals for jobs

*Payment Methods:*
• **USDT (TRC20)** - Fast, low fees
• **TON** - Instant, in-Telegram payments

*Support:*
Need more help? Contact our support team.

*Coming Soon Features:*
• Escrow payment system
• Freelancer profiles
• Job posting & bidding
• Rating system
• PRO subscriptions
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    profile_text = """
👤 *Profile Management*

Freelancer profile system coming soon!

*You'll be able to:*
• Add your bio and skills
• Upload portfolio items
• Set your hourly rate
• Choose categories
• Set availability status

Stay tuned for updates!
"""
    await update.message.reply_text(profile_text, parse_mode='Markdown')

def main():
    # Initialize database
    init_db()
    
    # Create bot application
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CommandHandler("help", help_command))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    print("🤖 FreelanceHub Bot is starting...")
    print("✅ Bot is LIVE with full menu system!")
    application.run_polling()

if __name__ == '__main__':
    main()
