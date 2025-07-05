# CloudBoost AI - Step-by-Step Fix Implementation Guide

## 🚀 Phase 1: Immediate Critical Fixes (Week 1-2)

### Step 1: Set Up Proper Environment Configuration

**Create `.env.example` file first:**

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/cloudboost_ai
REDIS_URL=redis://localhost:6379

# Security
JWT_SECRET=your-super-secure-jwt-secret-key-here
ENCRYPTION_KEY=your-32-byte-encryption-key-here

# AI Services
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# Communication Services
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
SENDGRID_API_KEY=your-sendgrid-api-key

# WhatsApp Business
WHATSAPP_TOKEN=your-whatsapp-business-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id

# Social Media APIs
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret

# Application Settings
FLASK_ENV=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
API_RATE_LIMIT=100
```

### Step 2: Fix Security Configuration

**Replace `backend/src/main.py` security section:**

```python
import os
import secrets
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta
import logging

# Initialize Flask app
app = Flask(__name__)

# Secure configuration
def get_secret_key():
    secret_key = os.environ.get('JWT_SECRET')
    if not secret_key:
        if os.environ.get('FLASK_ENV') == 'development':
            secret_key = secrets.token_urlsafe(32)
            print(f"Generated development JWT secret: {secret_key}")
        else:
            raise ValueError("JWT_SECRET environment variable must be set in production")
    return secret_key

def get_cors_origins():
    origins = os.environ.get('CORS_ORIGINS', '')
    if not origins:
        if os.environ.get('FLASK_ENV') == 'development':
            return ['http://localhost:3000', 'http://localhost:5173']
        else:
            raise ValueError("CORS_ORIGINS must be set in production")
    return origins.split(',')

# Security configuration
app.config['SECRET_KEY'] = get_secret_key()
app.config['JWT_SECRET_KEY'] = get_secret_key()
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Database configuration
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL environment variable must be set")

if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS configuration
CORS(app, origins=get_cors_origins(), supports_credentials=True)

# Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"]
)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
```

### Step 3: Create Missing Database Models

**Create `backend/src/models/content.py`:**

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Content(db.Model):
    __tablename__ = 'content'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # social_post, email, etc.
    prompt = db.Column(db.Text, nullable=False)
    generated_content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), nullable=False)
    platform = db.Column(db.String(50))  # facebook, instagram, etc.
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    usage_count = db.Column(db.Integer, default=0)
    performance_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = db.relationship('Tenant', backref='content_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'content_type': self.content_type,
            'generated_content': self.generated_content,
            'language': self.language,
            'platform': self.platform,
            'status': self.status,
            'usage_count': self.usage_count,
            'performance_score': self.performance_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ContentTemplate(db.Model):
    __tablename__ = 'content_templates'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    template_content = db.Column(db.Text, nullable=False)
    variables = db.Column(db.JSON)  # Template variables
    language = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'name': self.name,
            'content_type': self.content_type,
            'template_content': self.template_content,
            'variables': self.variables,
            'language': self.language,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
```

**Create `backend/src/models/customer.py`:**

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(255))
    status = db.Column(db.String(20), default='lead')  # lead, prospect, customer, inactive
    country = db.Column(db.String(10), default='LK')
    city = db.Column(db.String(100))
    address = db.Column(db.Text)
    source = db.Column(db.String(50))  # website, referral, etc.
    lead_score = db.Column(db.Integer, default=0)
    lifetime_value = db.Column(db.Float, default=0.0)
    total_spent = db.Column(db.Float, default=0.0)
    total_orders = db.Column(db.Integer, default=0)
    engagement_score = db.Column(db.Integer, default=50)
    last_contact = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    tags = db.Column(db.JSON)  # Array of tags
    custom_fields = db.Column(db.JSON)  # Custom fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = db.relationship('Tenant', backref='customers')
    deals = db.relationship('Deal', backref='customer', lazy=True)
    activities = db.relationship('Activity', backref='customer', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'status': self.status,
            'country': self.country,
            'city': self.city,
            'address': self.address,
            'source': self.source,
            'lead_score': self.lead_score,
            'lifetime_value': self.lifetime_value,
            'total_spent': self.total_spent,
            'total_orders': self.total_orders,
            'engagement_score': self.engagement_score,
            'last_contact': self.last_contact.isoformat() if self.last_contact else None,
            'notes': self.notes,
            'tags': self.tags or [],
            'custom_fields': self.custom_fields or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Deal(db.Model):
    __tablename__ = 'deals'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    customer_id = db.Column(db.String(36), db.ForeignKey('customers.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    stage = db.Column(db.String(50), default='qualification')
    probability = db.Column(db.Integer, default=20)
    expected_close_date = db.Column(db.Date)
    actual_close_date = db.Column(db.Date)
    description = db.Column(db.Text)
    assigned_to = db.Column(db.String(36))  # User ID
    source = db.Column(db.String(50))
    products = db.Column(db.JSON)  # Array of products
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'customer_id': self.customer_id,
            'title': self.title,
            'value': self.value,
            'currency': self.currency,
            'stage': self.stage,
            'probability': self.probability,
            'expected_close_date': self.expected_close_date.isoformat() if self.expected_close_date else None,
            'actual_close_date': self.actual_close_date.isoformat() if self.actual_close_date else None,
            'description': self.description,
            'assigned_to': self.assigned_to,
            'source': self.source,
            'products': self.products or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    customer_id = db.Column(db.String(36), db.ForeignKey('customers.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # call, email, meeting
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    scheduled_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    outcome = db.Column(db.String(50))  # positive, negative, neutral
    assigned_to = db.Column(db.String(36))  # User ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'customer_id': self.customer_id,
            'activity_type': self.activity_type,
            'subject': self.subject,
            'description': self.description,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'status': self.status,
            'outcome': self.outcome,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
```

## 🧠 Phase 2: Implement Real AI Integration (Week 3-4)

### Step 4: Create AI Service Layer

**Create `backend/src/services/ai_service.py`:**

```python
import openai
import os
from typing import Dict, Optional, List
from src.models.user import BusinessProfile

class AIContentService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    def generate_content(self, content_type: str, prompt: str, language: str, 
                        platform: Optional[str] = None, 
                        business_profile: Optional[BusinessProfile] = None) -> str:
        """Generate AI content with cultural adaptation"""
        
        # Build cultural context
        cultural_context = self._get_cultural_context(language)
        
        # Build business context
        business_context = ""
        if business_profile:
            business_context = f"""
            Business: {business_profile.business_name}
            Industry: {business_profile.industry}
            Brand Voice: {business_profile.brand_voice}
            Target Audience: {business_profile.target_audience}
            USP: {business_profile.unique_selling_proposition}
            """
        
        # Build platform-specific context
        platform_context = ""
        if platform:
            platform_context = self._get_platform_context(platform)
        
        # Create system prompt
        system_prompt = f"""
        You are an expert content creator for South Asian markets with deep cultural understanding.
        
        Cultural Context: {cultural_context}
        Business Context: {business_context}
        Platform Context: {platform_context}
        
        Guidelines:
        1. Respect cultural values and traditions
        2. Use appropriate formality level for the region
        3. Include relevant cultural references when appropriate
        4. Ensure content is engaging and authentic
        5. Follow platform-specific best practices
        
        Content Type: {content_type}
        Language: {language}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"AI content generation failed: {str(e)}")
    
    def _get_cultural_context(self, language: str) -> str:
        """Get cultural context for the specified language/region"""
        contexts = {
            'en': 'Professional, international business tone suitable for global audiences',
            'si': 'Respectful tone honoring Buddhist values and Sri Lankan cultural traditions. Use formal Sinhala expressions.',
            'ta': 'Culturally sensitive approach respecting Tamil traditions and values. Formal and respectful language.',
            'hi': 'Respectful Hindi with consideration for Indian cultural values, festivals, and business traditions.',
            'ur': 'Formal Urdu respecting Islamic values and Pakistani business culture. Professional yet warm tone.',
            'bn': 'Bengali content reflecting Bangladeshi cultural values with warm, respectful communication style.',
            'ne': 'Nepali content honoring local traditions and mountainous culture. Respectful and community-focused.'
        }
        return contexts.get(language, 'Professional, culturally-sensitive business tone')
    
    def _get_platform_context(self, platform: str) -> str:
        """Get platform-specific optimization guidelines"""
        contexts = {
            'facebook': 'Engaging, community-focused content. Use emojis and encourage interaction. Max 2200 characters.',
            'instagram': 'Visual-first content with compelling captions. Use relevant hashtags. Max 2200 characters.',
            'linkedin': 'Professional, business-focused content. Thought leadership tone. Max 3000 characters.',
            'twitter': 'Concise, impactful messages. Use relevant hashtags and mentions. Max 280 characters.',
            'whatsapp': 'Personal, conversational tone. Direct and actionable. Keep messages concise.',
            'email': 'Professional email format with clear subject line and call-to-action.'
        }
        return contexts.get(platform, 'General content optimization for maximum engagement')
    
    def translate_content(self, content: str, target_language: str) -> str:
        """Translate content while preserving cultural context"""
        
        cultural_context = self._get_cultural_context(target_language)
        
        system_prompt = f"""
        You are a professional translator specializing in South Asian languages and cultures.
        
        Translate the following content to {target_language} while:
        1. Preserving the original meaning and intent
        2. Adapting to cultural context: {cultural_context}
        3. Using appropriate formality level
        4. Maintaining brand voice and tone
        5. Ensuring natural, native-sounding language
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Translate this content: {content}"}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
    
    def optimize_for_platform(self, content: str, platform: str) -> str:
        """Optimize existing content for specific platform"""
        
        platform_context = self._get_platform_context(platform)
        
        system_prompt = f"""
        You are a social media optimization expert.
        
        Optimize the following content for {platform}:
        {platform_context}
        
        Ensure the optimized content:
        1. Follows platform best practices
        2. Maintains the original message
        3. Uses appropriate length and format
        4. Includes relevant calls-to-action
        5. Optimizes for engagement
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Optimize this content: {content}"}
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Content optimization failed: {str(e)}")

# Singleton instance
ai_service = AIContentService()
```

### Step 5: Fix Content Generation Route

**Replace the mock content generation in `backend/src/routes/content.py`:**

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.services.ai_service import ai_service
from src.models.content import Content, db
from src.models.user import BusinessProfile
from datetime import datetime

content_bp = Blueprint('content', __name__)

@content_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_content():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['content_type', 'prompt', 'language']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        content_type = data['content_type']
        prompt = data['prompt']
        language = data['language']
        platform = data.get('platform')
        
        # Get business profile for context
        business_profile = BusinessProfile.query.filter_by(tenant_id=tenant_id).first()
        
        # Generate content using AI service
        try:
            generated_content = ai_service.generate_content(
                content_type=content_type,
                prompt=prompt,
                language=language,
                platform=platform,
                business_profile=business_profile
            )
        except Exception as e:
            return jsonify({'error': f'Content generation failed: {str(e)}'}), 500
        
        # Save to database
        content_record = Content(
            tenant_id=tenant_id,
            content_type=content_type,
            prompt=prompt,
            generated_content=generated_content,
            language=language,
            platform=platform,
            status='draft'
        )
        
        db.session.add(content_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'content': generated_content,
            'content_id': content_record.id,
            'metadata': {
                'content_type': content_type,
                'language': language,
                'platform': platform,
                'character_count': len(generated_content),
                'created_at': content_record.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/translate', methods=['POST'])
@jwt_required()
def translate_content():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['content', 'target_language']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        content = data['content']
        target_language = data['target_language']
        
        # Translate using AI service
        try:
            translated_content = ai_service.translate_content(content, target_language)
        except Exception as e:
            return jsonify({'error': f'Translation failed: {str(e)}'}), 500
        
        return jsonify({
            'success': True,
            'original_content': content,
            'translated_content': translated_content,
            'target_language': target_language
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/optimize', methods=['POST'])
@jwt_required()
def optimize_content():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['content', 'platform']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        content = data['content']
        platform = data['platform']
        
        # Optimize using AI service
        try:
            optimized_content = ai_service.optimize_for_platform(content, platform)
        except Exception as e:
            return jsonify({'error': f'Optimization failed: {str(e)}'}), 500
        
        return jsonify({
            'success': True,
            'original_content': content,
            'optimized_content': optimized_content,
            'platform': platform
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## 📱 Phase 3: Implement Real Communication Services (Week 5-6)

### Step 6: Create Communication Service Layer

**Create `backend/src/services/communication_service.py`:**

```python
import os
import requests
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import Dict, Optional

class CommunicationService:
    def __init__(self):
        # WhatsApp (via Facebook Graph API)
        self.whatsapp_token = os.getenv('WHATSAPP_TOKEN')
        self.whatsapp_phone_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        
        # Twilio for SMS and Voice
        self.twilio_client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        ) if os.getenv('TWILIO_ACCOUNT_SID') else None
        
        # SendGrid for Email
        self.sendgrid_client = SendGridAPIClient(
            api_key=os.getenv('SENDGRID_API_KEY')
        ) if os.getenv('SENDGRID_API_KEY') else None
    
    def send_whatsapp_message(self, phone_number: str, message: str) -> Dict:
        """Send WhatsApp message via Facebook Graph API"""
        if not self.whatsapp_token or not self.whatsapp_phone_id:
            return {'success': False, 'error': 'WhatsApp credentials not configured'}
        
        url = f"https://graph.facebook.com/v18.0/{self.whatsapp_phone_id}/messages"
        headers = {
            'Authorization': f'Bearer {self.whatsapp_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'to': phone_number,
            'type': 'text',
            'text': {'body': message}
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'message_id': result['messages'][0]['id'],
                    'status': 'sent',
                    'cost': 0.005  # Approximate cost
                }
            else:
                error_data = response.json()
                return {
                    'success': False,
                    'error': error_data.get('error', {}).get('message', 'Unknown error')
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_whatsapp_template(self, phone_number: str, template_name: str, 
                              parameters: list) -> Dict:
        """Send WhatsApp template message"""
        if not self.whatsapp_token or not self.whatsapp_phone_id:
            return {'success': False, 'error': 'WhatsApp credentials not configured'}
        
        url = f"https://graph.facebook.com/v18.0/{self.whatsapp_phone_id}/messages"
        headers = {
            'Authorization': f'Bearer {self.whatsapp_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'to': phone_number,
            'type': 'template',
            'template': {
                'name': template_name,
                'language': {'code': 'en'},
                'components': [
                    {
                        'type': 'body',
                        'parameters': [{'type': 'text', 'text': param} for param in parameters]
                    }
                ]
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'message_id': result['messages'][0]['id'],
                    'status': 'sent'
                }
            else:
                error_data = response.json()
                return {
                    'success': False,
                    'error': error_data.get('error', {}).get('message', 'Unknown error')
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_sms(self, phone_number: str, message: str) -> Dict:
        """Send SMS via Twilio"""
        if not self.twilio_client:
            return {'success': False, 'error': 'Twilio credentials not configured'}
        
        try:
            message_obj = self.twilio_client.messages.create(
                body=message,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                to=phone_number
            )
            
            return {
                'success': True,
                'message_id': message_obj.sid,
                'status': message_obj.status,
                'cost': float(message_obj.price) if message_obj.price else 0.02
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_email(self, to_email: str, subject: str, content: str, 
                   content_type: str = 'text/html') -> Dict:
        """Send email via SendGrid"""
        if not self.sendgrid_client:
            return {'success': False, 'error': 'SendGrid credentials not configured'}
        
        try:
            message = Mail(
                from_email=os.getenv('FROM_EMAIL', 'noreply@cloudboost.ai'),
                to_emails=to_email,
                subject=subject,
                html_content=content if content_type == 'text/html' else None,
                plain_text_content=content if content_type == 'text/plain' else None
            )
            
            response = self.sendgrid_client.send(message)
            
            return {
                'success': True,
                'message_id': response.headers.get('X-Message-Id', ''),
                'status': 'sent',
                'cost': 0.001  # Approximate cost
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def make_voice_call(self, phone_number: str, message: str) -> Dict:
        """Make voice call via Twilio"""
        if not self.twilio_client:
            return {'success': False, 'error': 'Twilio credentials not configured'}
        
        try:
            # Create TwiML for the call
            twiml_url = f"{os.getenv('APP_BASE_URL')}/api/voice/twiml"
            
            call = self.twilio_client.calls.create(
                twiml=f'<Response><Say>{message}</Say></Response>',
                to=phone_number,
                from_=os.getenv('TWILIO_PHONE_NUMBER')
            )
            
            return {
                'success': True,
                'call_id': call.sid,
                'status': call.status,
                'cost': 0.05  # Approximate cost per minute
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Singleton instance
communication_service = CommunicationService()
```

## 🗄️ Phase 4: Fix Database Operations (Week 7-8)

### Step 7: Fix CRM Routes with Real Database Operations

**Replace mock data in `backend/src/routes/crm.py`:**

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.models.customer import Customer, Deal, Activity, db
from datetime import datetime, timedelta
from sqlalchemy import func, and_

crm_bp = Blueprint('crm', __name__)

@crm_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        search = request.args.get('search')
        country = request.args.get('country')
        
        # Build query
        query = Customer.query.filter_by(tenant_id=tenant_id)
        
        if status:
            query = query.filter_by(status=status)
        
        if search:
            query = query.filter(
                Customer.name.ilike(f'%{search}%') |
                Customer.email.ilike(f'%{search}%') |
                Customer.company.ilike(f'%{search}%')
            )
        
        if country:
            query = query.filter_by(country=country)
        
        # Execute paginated query
        customers = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'customers': [customer.to_dict() for customer in customers.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': customers.total,
                'pages': customers.pages
            },
            'filters': {
                'status': status,
                'search': search,
                'country': country
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if customer already exists
        existing_customer = Customer.query.filter_by(
            tenant_id=tenant_id,
            email=data['email']
        ).first()
        
        if existing_customer:
            return jsonify({'error': 'Customer with this email already exists'}), 400
        
        # Create customer record
        customer = Customer(
            tenant_id=tenant_id,
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            company=data.get('company'),
            status=data.get('status', 'lead'),
            country=data.get('country', 'LK'),
            city=data.get('city'),
            address=data.get('address'),
            source=data.get('source', 'manual'),
            notes=data.get('notes'),
            tags=data.get('tags', []),
            custom_fields=data.get('custom_fields', {})
        )
        
        # Calculate lead score if it's a lead
        if customer.status == 'lead':
            customer.lead_score = calculate_lead_score(data)
        
        # Calculate lifetime value prediction
        customer.lifetime_value = predict_customer_lifetime_value(data)
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Customer created successfully',
            'customer': customer.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/customers/<customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        customer = Customer.query.filter_by(
            id=customer_id, 
            tenant_id=tenant_id
        ).first()
        
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        return jsonify({
            'customer': customer.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/customers/<customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        customer = Customer.query.filter_by(
            id=customer_id, 
            tenant_id=tenant_id
        ).first()
        
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        for field in ['name', 'email', 'phone', 'company', 'status', 'country', 
                     'city', 'address', 'notes', 'tags', 'custom_fields']:
            if field in data:
                setattr(customer, field, data[field])
        
        # Recalculate scores if relevant data changed
        if 'status' in data and data['status'] == 'lead':
            customer.lead_score = calculate_lead_score(data)
        
        customer.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Customer updated successfully',
            'customer': customer.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def calculate_lead_score(lead_data):
    """Calculate lead score based on various factors"""
    score = 0
    
    # Company size scoring
    company_size = lead_data.get('company_size', 'small')
    if company_size == 'enterprise':
        score += 30
    elif company_size == 'medium':
        score += 20
    elif company_size == 'small':
        score += 10
    
    # Source scoring
    source = lead_data.get('source', '')
    source_scores = {
        'referral': 25,
        'website': 15,
        'social_media': 12,
        'email_campaign': 10,
        'cold_outreach': 5
    }
    score += source_scores.get(source, 5)
    
    # Geographic scoring
    country = lead_data.get('country', 'LK')
    country_scores = {
        'LK': 15,  # Sri Lanka
        'IN': 15,  # India
        'PK': 12,  # Pakistan
        'BD': 10,  # Bangladesh
        'NP': 8    # Nepal
    }
    score += country_scores.get(country, 5)
    
    return min(score, 100)  # Cap at 100

def predict_customer_lifetime_value(customer_data):
    """Predict customer lifetime value"""
    base_value = 1000
    
    # Company size multiplier
    company_size = customer_data.get('company_size', 'small')
    if company_size == 'enterprise':
        base_value *= 5
    elif company_size == 'medium':
        base_value *= 2.5
    
    # Country multiplier
    country = customer_data.get('country', 'LK')
    country_multipliers = {
        'IN': 1.2,
        'LK': 1.0,
        'PK': 0.9,
        'BD': 0.8,
        'NP': 0.7
    }
    
    multiplier = country_multipliers.get(country, 1.0)
    
    return round(base_value * multiplier, 2)
```

This gives you a solid foundation to start fixing the CloudBoost AI codebase. Each phase builds on the previous one, gradually replacing mock implementations with real functionality.

**Next Steps:**
1. Start with Phase 1 (Environment & Security)
2. Move to Phase 2 (AI Integration) 
3. Continue with Phase 3 (Communication Services)
4. Complete Phase 4 (Database Operations)

Would you like me to continue with the remaining phases (Social Media Integration, Frontend API Integration, Testing, etc.)?