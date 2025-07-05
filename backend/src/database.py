"""
CloudBoost AI Database Module
Unified database configuration and model management
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask-SQLAlchemy instance
db = SQLAlchemy()
migrate = Migrate()

# Base class for all models
Base = declarative_base()

# Database session management
engine = None
Session = None

def init_database(app: Flask):
    """Initialize database with Flask app"""
    global engine, Session
    
    # Configure SQLAlchemy with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Create engine
    database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
    engine_options = app.config.get('SQLALCHEMY_ENGINE_OPTIONS', {})
    
    if database_url.startswith('sqlite'):
        # SQLite specific configuration
        engine_options.update({
            'poolclass': StaticPool,
            'pool_pre_ping': True,
            'connect_args': {'check_same_thread': False}
        })
    
    engine = create_engine(database_url, **engine_options)
    Session = scoped_session(sessionmaker(bind=engine))
    
    logger.info(f"Database initialized: {database_url}")
    return db

def create_tables():
    """Create all database tables"""
    try:
        # Import all models to ensure they're registered
        from .models.user import User, Tenant, BusinessProfile, APIKey
        from .models.content import Content, ContentTemplate, ContentSchedule
        from .models.crm import Customer, Lead, Deal, Pipeline, Activity
        from .models.communication import EmailCampaign, SMSCampaign, WhatsAppMessage, CallLog
        from .models.social import SocialAccount, SocialPost, SocialEngagement
        from .models.automation import Workflow, WorkflowStep, WorkflowExecution
        from .models.analytics import Analytics, Report, KPI
        
        # Create all tables
        db.create_all()
        logger.info("All database tables created successfully")
        
        # Create initial data
        create_initial_data()
        
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

def create_initial_data():
    """Create initial data for the application"""
    try:
        # Check if we need to create initial data
        from .models.user import Tenant, User
        
        # Create default tenant if it doesn't exist
        default_tenant = Tenant.query.filter_by(domain='default').first()
        if not default_tenant:
            default_tenant = Tenant(
                name='Default Organization',
                domain='default',
                subscription_plan='enterprise',
                status='active'
            )
            db.session.add(default_tenant)
            db.session.commit()
            logger.info("Created default tenant")
        
        # Create admin user if it doesn't exist
        admin_user = User.query.filter_by(email='admin@cloudboost.ai').first()
        if not admin_user:
            admin_user = User(
                tenant_id=default_tenant.id,
                email='admin@cloudboost.ai',
                first_name='Admin',
                last_name='User',
                role='admin',
                status='active'
            )
            admin_user.set_password('Admin@123')
            db.session.add(admin_user)
            db.session.commit()
            logger.info("Created admin user")
        
        # Create default business profile
        from .models.user import BusinessProfile
        business_profile = BusinessProfile.query.filter_by(tenant_id=default_tenant.id).first()
        if not business_profile:
            business_profile = BusinessProfile(
                tenant_id=default_tenant.id,
                business_name='CloudBoost AI',
                industry='Technology',
                description='Complete Business Automation Platform for South Asia',
                website_url='https://cloudboost.ai',
                country='India',
                city='Mumbai',
                target_audience='Small and Medium Businesses in South Asia',
                brand_voice='Professional, Innovative, and Customer-Centric',
                unique_selling_proposition='AI-Powered Business Automation Made Simple',
                primary_language='en',
                secondary_languages='["hi", "ta", "te", "bn"]',
                brand_colors='{"primary": "#2563eb", "secondary": "#64748b", "accent": "#10b981"}'
            )
            db.session.add(business_profile)
            db.session.commit()
            logger.info("Created default business profile")
        
        # Create default CRM pipeline
        from .models.crm import Pipeline
        pipeline = Pipeline.query.filter_by(tenant_id=default_tenant.id, is_default=True).first()
        if not pipeline:
            pipeline = Pipeline(
                tenant_id=default_tenant.id,
                user_id=admin_user.id,
                name='Default Sales Pipeline',
                description='Standard sales pipeline for new leads',
                stages=[
                    {"name": "Prospecting", "probability": 10},
                    {"name": "Qualification", "probability": 25},
                    {"name": "Proposal", "probability": 50},
                    {"name": "Negotiation", "probability": 75},
                    {"name": "Closed Won", "probability": 100},
                    {"name": "Closed Lost", "probability": 0}
                ],
                is_default=True,
                is_active=True
            )
            db.session.add(pipeline)
            db.session.commit()
            logger.info("Created default CRM pipeline")
        
        # Create sample content templates
        from .models.content import ContentTemplate, ContentType
        templates = [
            {
                'name': 'Blog Post Template',
                'description': 'Standard blog post template',
                'content_type': ContentType.BLOG_POST,
                'template_body': '# {{title}}\n\n{{introduction}}\n\n## Key Points\n\n{{main_content}}\n\n## Conclusion\n\n{{conclusion}}',
                'variables': ['title', 'introduction', 'main_content', 'conclusion'],
                'category': 'Blog',
                'is_public': True
            },
            {
                'name': 'Social Media Post',
                'description': 'Engaging social media post template',
                'content_type': ContentType.SOCIAL_POST,
                'template_body': '🚀 {{hook}}\n\n{{content}}\n\n{{call_to_action}}\n\n{{hashtags}}',
                'variables': ['hook', 'content', 'call_to_action', 'hashtags'],
                'category': 'Social Media',
                'is_public': True
            },
            {
                'name': 'Email Campaign',
                'description': 'Professional email campaign template',
                'content_type': ContentType.EMAIL,
                'template_body': 'Subject: {{subject}}\n\nHi {{name}},\n\n{{greeting}}\n\n{{main_message}}\n\n{{call_to_action}}\n\nBest regards,\n{{sender_name}}',
                'variables': ['subject', 'name', 'greeting', 'main_message', 'call_to_action', 'sender_name'],
                'category': 'Email',
                'is_public': True
            }
        ]
        
        for template_data in templates:
            existing = ContentTemplate.query.filter_by(name=template_data['name']).first()
            if not existing:
                template = ContentTemplate(
                    tenant_id=default_tenant.id,
                    user_id=admin_user.id,
                    **template_data
                )
                db.session.add(template)
        
        db.session.commit()
        logger.info("Created sample content templates")
        
        logger.info("Initial data creation completed")
        
    except Exception as e:
        logger.error(f"Error creating initial data: {e}")
        db.session.rollback()
        raise

def get_db_session():
    """Get database session"""
    return Session()

def close_db_session(session):
    """Close database session"""
    session.close()

def health_check():
    """Check database health"""
    try:
        # Try to execute a simple query
        result = db.session.execute(text('SELECT 1'))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

def backup_database(backup_path: str):
    """Backup database (for SQLite)"""
    try:
        if engine.url.drivername == 'sqlite':
            import shutil
            db_path = engine.url.database
            shutil.copy2(db_path, backup_path)
            logger.info(f"Database backed up to: {backup_path}")
            return True
        else:
            logger.warning("Backup not implemented for non-SQLite databases")
            return False
    except Exception as e:
        logger.error(f"Database backup failed: {e}")
        return False

def get_database_stats():
    """Get database statistics"""
    try:
        stats = {}
        
        # Get table counts
        from .models.user import User, Tenant
        from .models.content import Content
        from .models.crm import Customer, Lead, Deal
        from .models.communication import EmailCampaign, SMSCampaign
        from .models.social import SocialPost
        from .models.automation import Workflow
        
        stats['users'] = User.query.count()
        stats['tenants'] = Tenant.query.count()
        stats['content_items'] = Content.query.count()
        stats['customers'] = Customer.query.count()
        stats['leads'] = Lead.query.count()
        stats['deals'] = Deal.query.count()
        stats['email_campaigns'] = EmailCampaign.query.count()
        stats['sms_campaigns'] = SMSCampaign.query.count()
        stats['social_posts'] = SocialPost.query.count()
        stats['workflows'] = Workflow.query.count()
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {}

# Database event handlers
@db.event.listens_for(db.engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragma for better performance"""
    if 'sqlite' in str(db.engine.url):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=1000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.close()

# Export main components
__all__ = [
    'db', 'migrate', 'Base', 'Session',
    'init_database', 'create_tables', 'create_initial_data',
    'get_db_session', 'close_db_session', 'health_check',
    'backup_database', 'get_database_stats'
]