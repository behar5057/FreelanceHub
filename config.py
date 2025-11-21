import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x]
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///freelancehub.db')
    COMMISSION_RATE = float(os.getenv('COMMISSION_RATE', 0.10))
    
    CATEGORIES = {
        'graphic_design': '🎨 Graphic Design',
        'writing': '✍️ Writing & Copywriting', 
        'translation': '🌍 Translation',
        'programming': '💻 Programming & Tech',
        'video_editing': '🎬 Video & Audio Editing',
        'ai_services': '🤖 AI Services',
        'marketing': '📈 Marketing & Business',
        'cyber_security': '🛡️ Cyber Security'
    }
