from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

db = SQLAlchemy()

class Tenant(db.Model):
    __tablename__ = 'tenants'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255), unique=True, nullable=False)
    subscription_plan = db.Column(db.String(50), default='basic')
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', backref='tenant', lazy=True)
    business_profiles = db.relationship('BusinessProfile', backref='tenant', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'subscription_plan': self.subscription_plan,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='user')  # admin, manager, user
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    language_preference = db.Column(db.String(10), default='en')
    timezone = db.Column(db.String(50), default='UTC')
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint on email per tenant
    __table_args__ = (db.UniqueConstraint('tenant_id', 'email', name='unique_tenant_email'),)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'status': self.status,
            'language_preference': self.language_preference,
            'timezone': self.timezone,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class BusinessProfile(db.Model):
    __tablename__ = 'business_profiles'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    business_name = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(100))
    description = db.Column(db.Text)
    website_url = db.Column(db.String(500))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    target_audience = db.Column(db.Text)
    brand_voice = db.Column(db.Text)
    unique_selling_proposition = db.Column(db.Text)
    primary_language = db.Column(db.String(10), default='en')
    secondary_languages = db.Column(db.Text)  # JSON array of language codes
    logo_url = db.Column(db.String(500))
    brand_colors = db.Column(db.Text)  # JSON object with color scheme
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'business_name': self.business_name,
            'industry': self.industry,
            'description': self.description,
            'website_url': self.website_url,
            'country': self.country,
            'city': self.city,
            'target_audience': self.target_audience,
            'brand_voice': self.brand_voice,
            'unique_selling_proposition': self.unique_selling_proposition,
            'primary_language': self.primary_language,
            'secondary_languages': self.secondary_languages,
            'logo_url': self.logo_url,
            'brand_colors': self.brand_colors,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class APIKey(db.Model):
    __tablename__ = 'api_keys'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # facebook, google, linkedin, etc.
    key_name = db.Column(db.String(100), nullable=False)
    encrypted_key = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='active')
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'platform': self.platform,
            'key_name': self.key_name,
            'status': self.status,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

