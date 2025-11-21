import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database setup
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    user_type = Column(String(20), default='client')
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

# Get environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///freelancehub.db')

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    print("✅ Database initialized!")

def main_menu_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🔍 Browse Freelancers"), KeyboardButton("📌 Post a Job")],
        [KeyboardButton("🗂 Categories"), KeyboardButton("⭐ Upgrade to Pro")],
        [KeyboardButton("📊 My Dashboard"), KeyboardButton("🛟 Help Center")]
    ], resize_keyboard=True)

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
    
    welcome_text = """
🤖 Welcome to *FreelanceHub*!

The global freelance marketplace powered by crypto.

*Choose an option below:*
🔍 Browse Freelancers
📌 Post a Job  
🗂 Categories
⭐ Upgrade to Pro
📊 My Dashboard
🛟 Help Center
"""
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard(), parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🔍 Browse Freelancers":
        await update.message.reply_text("👥 Browse Freelancers - Coming soon!", parse_mode='Markdown')
    elif text == "📌 Post a Job":
        await update.message.reply_text("📝 Post a Job - Coming soon!", parse_mode='Markdown')
    elif text == "🗂 Categories":
        await update.message.reply_text("🏷️ Categories:\n• Graphic Design\n• Programming\n• Writing\n• Marketing\n• AI Services\n• Cyber Security", parse_mode='Markdown')
    elif text == "⭐ Upgrade to Pro":
        await update.message.reply_text("⭐ PRO features coming soon!", parse_mode='Markdown')
    elif text == "📊 My Dashboard":
        await update.message.reply_text("📊 Dashboard - Coming soon!", parse_mode='Markdown')
    elif text == "🛟 Help Center":
        await update.message.reply_text("🛟 Help - Contact support for assistance", parse_mode='Markdown')
    else:
        await update.message.reply_text("Please use the menu buttons!", reply_markup=main_menu_keyboard())

def main():
    # Initialize database
    init_db()
    
    # Create bot application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 FreelanceHub Bot Starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
