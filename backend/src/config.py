import os
import secrets
from pathlib import Path

class Config:
    """Base configuration with automatic setup"""
    
    def __init__(self):
        self.setup_directories()
        self.setup_security()
        self.setup_database()
        self.setup_integrations()
    
    def setup_directories(self):
        """Create necessary directories"""
        dirs = ['logs', 'uploads', 'temp', 'backups']
        for dir_name in dirs:
            Path(dir_name).mkdir(exist_ok=True)
    
    def setup_security(self):
        """Setup security with auto-generated keys"""
        self.SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(32)
        self.JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_urlsafe(32)
        self.ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or secrets.token_urlsafe(32)
        
        # Security headers
        self.SESSION_COOKIE_SECURE = True
        self.SESSION_COOKIE_HTTPONLY = True
        self.SESSION_COOKIE_SAMESITE = 'Lax'
        
        # CORS settings
        cors_origins = os.environ.get('CORS_ORIGINS', '')
        if cors_origins:
            self.CORS_ORIGINS = [origin.strip() for origin in cors_origins.split(',')]
        else:
            self.CORS_ORIGINS = [
                'http://localhost:3000',
                'http://localhost:5173', 
                'http://localhost:8080',
                'http://127.0.0.1:3000',
                'http://127.0.0.1:5173'
            ]
    
    def setup_database(self):
        """Setup database with automatic fallback"""
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            # Auto-configure SQLite for development
            db_path = Path('cloudboost_ai.db')
            database_url = f'sqlite:///{db_path.absolute()}'
            print(f"🗄️ Using SQLite database: {db_path.absolute()}")
        
        # Handle PostgreSQL URL format
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        self.SQLALCHEMY_DATABASE_URI = database_url
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
        }
        
        # Redis setup with fallback
        self.REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
        
    def setup_integrations(self):
        """Setup all third-party integrations with smart defaults"""
        
        # OpenAI Configuration
        self.OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        self.OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.OPENAI_MAX_TOKENS = int(os.environ.get('OPENAI_MAX_TOKENS', '1500'))
        self.AI_ENABLED = bool(self.OPENAI_API_KEY and self.OPENAI_API_KEY != 'your-openai-api-key-here')
        
        # Communication Services
        self.TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
        self.TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
        self.TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
        self.SMS_ENABLED = bool(self.TWILIO_ACCOUNT_SID and self.TWILIO_AUTH_TOKEN)
        
        self.SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
        self.FROM_EMAIL = os.environ.get('FROM_EMAIL', 'noreply@cloudboost.ai')
        self.EMAIL_ENABLED = bool(self.SENDGRID_API_KEY)
        
        self.WHATSAPP_TOKEN = os.environ.get('WHATSAPP_TOKEN')
        self.WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
        self.WHATSAPP_ENABLED = bool(self.WHATSAPP_TOKEN and self.WHATSAPP_PHONE_NUMBER_ID)
        
        # Social Media APIs
        self.FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
        self.FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
        self.FACEBOOK_ENABLED = bool(self.FACEBOOK_APP_ID and self.FACEBOOK_APP_SECRET)
        
        self.LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID')
        self.LINKEDIN_CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET')
        self.LINKEDIN_ENABLED = bool(self.LINKEDIN_CLIENT_ID and self.LINKEDIN_CLIENT_SECRET)
        
        # Rate limiting
        self.RATELIMIT_STORAGE_URL = self.REDIS_URL
        self.RATELIMIT_DEFAULT = os.environ.get('API_RATE_LIMIT', '1000 per day, 100 per hour')
        
        # File uploads
        self.MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
        self.UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
        
        # Application settings
        self.DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
        self.TESTING = False
        
    def get_integration_status(self):
        """Get status of all integrations"""
        return {
            'database': self.SQLALCHEMY_DATABASE_URI.startswith('sqlite') and 'SQLite' or 'PostgreSQL',
            'ai_enabled': self.AI_ENABLED,
            'email_enabled': self.EMAIL_ENABLED,
            'sms_enabled': self.SMS_ENABLED,
            'whatsapp_enabled': self.WHATSAPP_ENABLED,
            'facebook_enabled': self.FACEBOOK_ENABLED,
            'linkedin_enabled': self.LINKEDIN_ENABLED,
            'redis_configured': bool(self.REDIS_URL),
            'security_configured': True
        }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    def setup_security(self):
        super().setup_security()
        # Production-specific security
        self.SESSION_COOKIE_SECURE = True
        self.PREFERRED_URL_SCHEME = 'https'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    def setup_database(self):
        """Use in-memory database for testing"""
        self.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuration selector
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])()