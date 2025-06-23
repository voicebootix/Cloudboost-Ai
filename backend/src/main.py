import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta
import logging

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize Flask app
app = Flask(__name__)

# Configuration for Render deployment
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET', 'dev-jwt-secret')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Database configuration for Render
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///cloudboost.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Redis configuration for Render
app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379')

# CORS configuration for Render
cors_origins = os.environ.get('CORS_ORIGINS', '*').split(',')
CORS(app, origins=cors_origins, supports_credentials=True)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'service': 'CloudBoost AI API',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'environment': os.environ.get('FLASK_ENV', 'development')
    })

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'CloudBoost AI API',
        'version': '1.0.0',
        'status': 'running',
        'documentation': '/api/docs'
    })

# API documentation endpoint
@app.route('/api/docs', methods=['GET'])
def api_docs():
    """API documentation endpoint"""
    return jsonify({
        'name': 'CloudBoost AI API',
        'version': '1.0.0',
        'description': 'Complete Business Automation Platform for South Asia',
        'endpoints': {
            'health': '/api/health',
            'auth': '/api/auth/*',
            'content': '/api/content/*',
            'social': '/api/social/*',
            'communication': '/api/communication/*',
            'crm': '/api/crm/*',
            'automation': '/api/automation/*',
            'analytics': '/api/analytics/*'
        },
        'documentation': 'https://docs.cloudboost.ai'
    })

# Import and register blueprints
try:
    from routes.auth import auth_bp
    from routes.content import content_bp
    from routes.social import social_bp
    from routes.communication import communication_bp
    from routes.crm import crm_bp
    from routes.automation import automation_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(content_bp, url_prefix='/api/content')
    app.register_blueprint(social_bp, url_prefix='/api/social')
    app.register_blueprint(communication_bp, url_prefix='/api/communication')
    app.register_blueprint(crm_bp, url_prefix='/api/crm')
    app.register_blueprint(automation_bp, url_prefix='/api/automation')
    
    logger.info("All blueprints registered successfully")
except ImportError as e:
    logger.warning(f"Some blueprints could not be imported: {e}")

# Create database tables
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Invalid token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Authorization token required'}), 401

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting CloudBoost AI API on port {port}")
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    logger.info(f"Database: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

