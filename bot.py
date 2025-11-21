import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import Config
from database import init_db
import handlers.handlers_main as handlers_main  # CHANGED THIS LINE

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    # Initialize database
    init_db()
    
    # Create bot application
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Add handlers - UPDATED TO handlers_main
    application.add_handler(CommandHandler("start", handlers_main.start))
    application.add_handler(CommandHandler("profile", handlers_main.profile))
    application.add_handler(CommandHandler("help", handlers_main.help_command))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers_main.handle_message))
    application.add_handler(CallbackQueryHandler(handlers_main.handle_callback))
    
    # Start bot
    print("🤖 FreelanceHub Bot is starting...")
    print("✅ Bot is LIVE and running!")
    application.run_polling()

if __name__ == '__main__':
    main()
