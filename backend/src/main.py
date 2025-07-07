"""
CloudBoost AI - Complete Business Automation Platform
Main Flask Application with Real Functionality
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# Import configuration and database
from .config import get_config
from .database import init_database, create_tables, health_check, get_database_stats

# Import all services
from .services.ai_service import AIService
from .services.communication_service import CommunicationService
from .services.social_service import SocialService
from .services.crm_service import CRMService
from .services.content_service import ContentService
from .services.automation_service import AutomationService
from .services.analytics_service import AnalyticsService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Load configuration
config = get_config()
app.config.from_object(config)

# Initialize extensions
cors = CORS(app, origins=config.CORS_ORIGINS, supports_credentials=True)
jwt = JWTManager(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[config.RATELIMIT_DEFAULT]
)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Initialize database
db = init_database(app)

# Initialize services
ai_service = AIService(config)
communication_service = CommunicationService(config)
social_service = SocialService(config)
crm_service = CRMService(db)
content_service = ContentService(db, ai_service)
automation_service = AutomationService(db, ai_service, communication_service)
analytics_service = AnalyticsService(db)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """System health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': health_check(),
        'integrations': config.get_integration_status(),
        'version': '1.0.0'
    })

# System status endpoint
@app.route('/status', methods=['GET'])
@jwt_required()
def system_status():
    """Detailed system status"""
    return jsonify({
        'database_stats': get_database_stats(),
        'integrations': config.get_integration_status(),
        'uptime': datetime.utcnow().isoformat(),
        'environment': os.environ.get('FLASK_ENV', 'development')
    })

# Authentication endpoints
@app.route('/auth/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """User login"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Import here to avoid circular imports
        from .models.user import User
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password) and user.status == 'active':
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Create access token
            access_token = create_access_token(
                identity=user.id,
                additional_claims={
                    'tenant_id': user.tenant_id,
                    'role': user.role,
                    'email': user.email
                }
            )
            
            return jsonify({
                'access_token': access_token,
                'user': user.to_dict(),
                'expires_in': 86400  # 24 hours
            })
        
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/auth/register', methods=['POST'])
@limiter.limit("3 per minute")
def register():
    """User registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name', 'tenant_domain']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        from .models.user import User, Tenant
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Get or create tenant
        tenant = Tenant.query.filter_by(domain=data['tenant_domain']).first()
        if not tenant:
            tenant = Tenant(
                name=data.get('tenant_name', data['tenant_domain']),
                domain=data['tenant_domain'],
                status='active'
            )
            db.session.add(tenant)
            db.session.flush()
        
        # Create user
        user = User(
            tenant_id=tenant.id,
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data.get('role', 'user'),
            status='active'
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

# Dashboard endpoint
@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    """Main dashboard with real-time data"""
    try:
        user_id = get_jwt_identity()
        
        # Get dashboard data
        dashboard_data = {
            'stats': analytics_service.get_dashboard_stats(user_id),
            'recent_activities': analytics_service.get_recent_activities(user_id),
            'kpis': analytics_service.get_kpis(user_id),
            'notifications': analytics_service.get_notifications(user_id),
            'quick_actions': [
                {'name': 'Create Content', 'url': '/content/create', 'icon': 'pen'},
                {'name': 'New Campaign', 'url': '/campaigns/create', 'icon': 'megaphone'},
                {'name': 'Add Customer', 'url': '/crm/customers/create', 'icon': 'user-plus'},
                {'name': 'Schedule Post', 'url': '/social/schedule', 'icon': 'calendar'}
            ]
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return jsonify({'error': 'Failed to load dashboard'}), 500

# Content Management endpoints
@app.route('/content', methods=['GET'])
@jwt_required()
def get_content():
    """Get content list"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        content_type = request.args.get('type')
        
        content_list = content_service.get_content_list(user_id, page, per_page, content_type)
        return jsonify(content_list)
        
    except Exception as e:
        logger.error(f"Get content error: {e}")
        return jsonify({'error': 'Failed to fetch content'}), 500

@app.route('/content', methods=['POST'])
@jwt_required()
def create_content():
    """Create new content"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        content = content_service.create_content(user_id, data)
        return jsonify(content.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Create content error: {e}")
        return jsonify({'error': 'Failed to create content'}), 500

@app.route('/content/<int:content_id>', methods=['GET'])
@jwt_required()
def get_content_detail(content_id):
    """Get content details"""
    try:
        user_id = get_jwt_identity()
        content = content_service.get_content_by_id(user_id, content_id)
        
        if not content:
            return jsonify({'error': 'Content not found'}), 404
        
        return jsonify(content.to_dict())
        
    except Exception as e:
        logger.error(f"Get content detail error: {e}")
        return jsonify({'error': 'Failed to fetch content'}), 500

@app.route('/content/<int:content_id>', methods=['PUT'])
@jwt_required()
def update_content(content_id):
    """Update content"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        content = content_service.update_content(user_id, content_id, data)
        if not content:
            return jsonify({'error': 'Content not found'}), 404
        
        return jsonify(content.to_dict())
        
    except Exception as e:
        logger.error(f"Update content error: {e}")
        return jsonify({'error': 'Failed to update content'}), 500

@app.route('/content/<int:content_id>', methods=['DELETE'])
@jwt_required()
def delete_content(content_id):
    """Delete content"""
    try:
        user_id = get_jwt_identity()
        
        if content_service.delete_content(user_id, content_id):
            return jsonify({'message': 'Content deleted successfully'})
        
        return jsonify({'error': 'Content not found'}), 404
        
    except Exception as e:
        logger.error(f"Delete content error: {e}")
        return jsonify({'error': 'Failed to delete content'}), 500

# AI Content Generation
@app.route('/ai/generate-content', methods=['POST'])
@jwt_required()
def generate_content():
    """Generate content using AI"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        prompt = data.get('prompt')
        content_type = data.get('content_type', 'blog_post')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        generated_content = ai_service.generate_content(prompt, content_type)
        return jsonify(generated_content)
        
    except Exception as e:
        logger.error(f"AI content generation error: {e}")
        return jsonify({'error': 'Failed to generate content'}), 500

# CRM endpoints
@app.route('/crm/customers', methods=['GET'])
@jwt_required()
def get_customers():
    """Get customers list"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        
        customers = crm_service.get_customers(user_id, page, per_page, search)
        return jsonify(customers)
        
    except Exception as e:
        logger.error(f"Get customers error: {e}")
        return jsonify({'error': 'Failed to fetch customers'}), 500

@app.route('/crm/customers', methods=['POST'])
@jwt_required()
def create_customer():
    """Create new customer"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        customer = crm_service.create_customer(user_id, data)
        return jsonify(customer.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Create customer error: {e}")
        return jsonify({'error': 'Failed to create customer'}), 500

# Communication endpoints
@app.route('/communication/email/send', methods=['POST'])
@jwt_required()
def send_email():
    """Send email"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = communication_service.send_email(
            to_email=data.get('to_email'),
            subject=data.get('subject'),
            content=data.get('content'),
            html_content=data.get('html_content')
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Send email error: {e}")
        return jsonify({'error': 'Failed to send email'}), 500

@app.route('/communication/sms/send', methods=['POST'])
@jwt_required()
def send_sms():
    """Send SMS"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = communication_service.send_sms(
            to_number=data.get('to_number'),
            message=data.get('message')
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Send SMS error: {e}")
        return jsonify({'error': 'Failed to send SMS'}), 500

# Social Media endpoints
@app.route('/social/accounts', methods=['GET'])
@jwt_required()
def get_social_accounts():
    """Get social media accounts"""
    try:
        user_id = get_jwt_identity()
        accounts = social_service.get_accounts(user_id)
        return jsonify(accounts)
        
    except Exception as e:
        logger.error(f"Get social accounts error: {e}")
        return jsonify({'error': 'Failed to fetch social accounts'}), 500

@app.route('/social/post', methods=['POST'])
@jwt_required()
def create_social_post():
    """Create social media post"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        post = social_service.create_post(user_id, data)
        return jsonify(post.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Create social post error: {e}")
        return jsonify({'error': 'Failed to create social post'}), 500

# Analytics endpoints
@app.route('/analytics/dashboard', methods=['GET'])
@jwt_required()
def get_analytics_dashboard():
    """Get analytics dashboard"""
    try:
        user_id = get_jwt_identity()
        date_range = request.args.get('date_range', '30d')
        
        analytics = analytics_service.get_dashboard_analytics(user_id, date_range)
        return jsonify(analytics)
        
    except Exception as e:
        logger.error(f"Get analytics error: {e}")
        return jsonify({'error': 'Failed to fetch analytics'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': f'Rate limit exceeded: {e.description}'}), 429

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Invalid token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Authorization token is required'}), 401

# Application startup

def create_app():
    """Create and configure the Flask application"""
    with app.app_context():
        try:
            # Create database tables
            create_tables()
            logger.info("Application started successfully")
        except Exception as e:
            logger.error(f"Application startup error: {e}")
            raise
    return app

# Set app for WSGI servers
app = create_app()

# Welcome endpoint
@app.route('/')
def welcome():
    """Welcome page"""
    return jsonify({
        'message': 'Welcome to CloudBoost AI - Complete Business Automation Platform',
        'version': '1.0.0',
        'features': [
            'AI-Powered Content Generation',
            'Multi-Channel Communication',
            'Social Media Management',
            'CRM & Lead Management',
            'Business Process Automation',
            'Real-Time Analytics'
        ],
        'docs': '/docs',
        'health': '/health',
        'login': '/auth/login'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )

