"""
Billico Configuration File - DEMO VERSION
Contains all configuration settings for the application using SQLite
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production-xyz123')
    DEBUG = True
    TESTING = False
    
    # Database Configuration - Using SQLite for demo
    SQLALCHEMY_DATABASE_URI = "sqlite:///billico_demo.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Session Configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    
    # Tesseract OCR Configuration
    TESSERACT_PATH = os.getenv('TESSERACT_PATH', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    TESSERACT_LANG = 'eng'  # Language for OCR
    
    # Image Processing Configuration
    IMAGE_MAX_WIDTH = 2000
    IMAGE_MAX_HEIGHT = 2000
    IMAGE_QUALITY = 95
    
    # Inventory Configuration
    LOW_STOCK_THRESHOLD = 10  # Default threshold for low stock alerts
    MEDIUM_STOCK_THRESHOLD = 50
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Application Settings
    APP_NAME = 'Billico'
    APP_VERSION = '1.0.0'
    APP_DESCRIPTION = 'Smart Inventory Automation Platform'
    
    # Security
    BCRYPT_LOG_ROUNDS = 12
    
    # Error Handling
    PROPAGATE_EXCEPTIONS = True


def get_config():
    """Get configuration"""
    return Config
