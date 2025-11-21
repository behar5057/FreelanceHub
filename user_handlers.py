from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from database import Session, User
import logging

logger = logging.getLogger(__name__)

def main_menu_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🔍 Browse Freelancers"), KeyboardButton("📌 Post a Job")],
        [KeyboardButton("🗂 Categories"), KeyboardButton("⭐ Upgrade to Pro")],
        [KeyboardButton("📊 My Dashboard"), KeyboardButton("🛟 Help Center")]
    ], resize_keyboard=True)

def categories_keyboard():
    keyboard = []
    categories = [
        ("🎨 Graphic Design", "category_graphic_design"),
        ("✍️ Writing", "category_writing"),
        ("🌍 Translation", "category_translation"),
        ("💻 Programming", "category_programming"),
        ("🎬 Video Editing", "category_video_editing"),
        ("🤖 AI Services", "category_ai_services"),
        ("📈 Marketing", "category_marketing"),
        ("🛡️ Cyber Security", "category_cyber_security")
    ]
    
    for i in range(0, len(categories), 2):
        row = categories[i:i+2]
        keyboard.append([
            InlineKeyboardButton(text, callback_data=data) for text, data in row
        ])
    
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
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
            print(f"✅ New user registered: {user.username} (ID: {user.id})")
    
    welcome_text = """
🤖 Welcome to *FreelanceHub*!

The global marketplace where talent meets opportunity.

Choose an option below to get started:
"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🔍 Browse Freelancers":
        await update.message.reply_text("👥 *Browse Freelancers* - Coming soon!", parse_mode='Markdown')
    elif text == "📌 Post a Job":
        await post_job_start(update, context)
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
    text = "🏷️ *Select a Category:*"
    await update.message.reply_text(text, reply_markup=categories_keyboard(), parse_mode='Markdown')

async def show_pro_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
⭐ *FreelanceHub PRO*

*Benefits:*
• Top placement in search
• Priority notifications  
• PRO badge
• Analytics dashboard
• Premium categories

*Price:* 10 USDT/month
"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Subscribe Now", callback_data="pro_subscribe")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
    ])
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    with Session() as session:
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        balance = db_user.balance if db_user else 0.0
    
    text = f"""
📊 *Your Dashboard*

*Balance:* {balance:.2f} USDT
*Status:* Basic User

*Quick Actions:*
• Create profile
• Post a job
• Check balance
"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Create Profile", callback_data="create_profile")],
        [InlineKeyboardButton("💰 Check Balance", callback_data="check_balance")],
        [InlineKeyboardButton("⬅️ Main Menu", callback_data="main_menu")]
    ])
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🛟 *Help Center*

*For Clients:* Post jobs & hire talent
*For Freelancers:* Create profile & find work
*Payments:* USDT & TON supported

Need help? Contact support.
"""
    await update.message.reply_text(text, parse_mode='Markdown')

async def post_job_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Select a category for your job:", reply_markup=categories_keyboard())

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 Profile system coming soon!")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    if callback_data.startswith('category_'):
        category_name = callback_data.replace('category_', '').replace('_', ' ').title()
        await query.edit_message_text(f"🎯 You selected: {category_name}\n\nWhat would you like to do?", parse_mode='Markdown')
    elif callback_data == 'pro_subscribe':
        await query.edit_message_text("⭐ PRO subscription - Payment system coming soon!", parse_mode='Markdown')
    elif callback_data == 'main_menu':
        await query.edit_message_text("Returning to main menu...")
        await context.bot.send_message(chat_id=query.message.chat_id, text="Main Menu:", reply_markup=main_menu_keyboard())
    elif callback_data == 'create_profile':
        await query.edit_message_text("👤 Profile creation coming soon!", parse_mode='Markdown')
    elif callback_data == 'check_balance':
        user = query.from_user
        with Session() as session:
            db_user = session.query(User).filter_by(telegram_id=user.id).first()
            balance = db_user.balance if db_user else 0.0
        await query.edit_message_text(f"💰 Your balance: {balance:.2f} USDT", parse_mode='Markdown')
