from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class LeadStatus(enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class LeadSource(enum.Enum):
    WEBSITE = "website"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    REFERRAL = "referral"
    COLD_CALL = "cold_call"
    TRADE_SHOW = "trade_show"
    ADVERTISEMENT = "advertisement"
    ORGANIC = "organic"

class DealStage(enum.Enum):
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class ActivityType(enum.Enum):
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    TASK = "task"
    NOTE = "note"
    WHATSAPP = "whatsapp"
    SMS = "sms"

class Customer(Base):
    __tablename__ = 'customer'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Basic Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    
    # Company Information
    company_name = Column(String(200))
    job_title = Column(String(100))
    department = Column(String(100))
    company_size = Column(String(20))
    industry = Column(String(100))
    
    # Address Information
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    
    # Business Information
    annual_revenue = Column(Float)
    website = Column(String(255))
    linkedin_url = Column(String(255))
    
    # Customer Data
    customer_segment = Column(String(100))
    customer_value = Column(Float, default=0.0)
    lifetime_value = Column(Float, default=0.0)
    
    # Engagement Data
    tags = Column(JSON)
    custom_fields = Column(JSON)
    notes = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_lead = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contact_at = Column(DateTime)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="customers")
    user = relationship("User", back_populates="customers")
    leads = relationship("Lead", back_populates="customer", cascade="all, delete-orphan")
    deals = relationship("Deal", back_populates="customer", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="customer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'mobile': self.mobile,
            'company_name': self.company_name,
            'job_title': self.job_title,
            'department': self.department,
            'company_size': self.company_size,
            'industry': self.industry,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'annual_revenue': self.annual_revenue,
            'website': self.website,
            'linkedin_url': self.linkedin_url,
            'customer_segment': self.customer_segment,
            'customer_value': self.customer_value,
            'lifetime_value': self.lifetime_value,
            'tags': self.tags,
            'custom_fields': self.custom_fields,
            'notes': self.notes,
            'is_active': self.is_active,
            'is_lead': self.is_lead,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_contact_at': self.last_contact_at.isoformat() if self.last_contact_at else None
        }

class Lead(Base):
    __tablename__ = 'lead'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    
    # Lead Information
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Lead Status
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    source = Column(Enum(LeadSource), default=LeadSource.WEBSITE)
    
    # Lead Scoring
    score = Column(Integer, default=0)
    temperature = Column(String(10))  # 'hot', 'warm', 'cold'
    
    # Business Information
    budget = Column(Float)
    expected_close_date = Column(DateTime)
    probability = Column(Integer, default=0)  # 0-100
    
    # Assignment
    assigned_to = Column(Integer, ForeignKey('user.id'))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    converted_at = Column(DateTime)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="leads")
    user = relationship("User", foreign_keys=[user_id], back_populates="leads")
    customer = relationship("Customer", back_populates="leads")
    assigned_user = relationship("User", foreign_keys=[assigned_to])
    activities = relationship("Activity", back_populates="lead", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Lead {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'customer_id': self.customer_id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'source': self.source.value,
            'score': self.score,
            'temperature': self.temperature,
            'budget': self.budget,
            'expected_close_date': self.expected_close_date.isoformat() if self.expected_close_date else None,
            'probability': self.probability,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'converted_at': self.converted_at.isoformat() if self.converted_at else None
        }

class Pipeline(Base):
    __tablename__ = 'pipeline'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Pipeline configuration
    stages = Column(JSON)  # [{"name": "Prospecting", "probability": 10}, ...]
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="pipelines")
    user = relationship("User", back_populates="pipelines")
    deals = relationship("Deal", back_populates="pipeline", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Pipeline {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'stages': self.stages,
            'is_default': self.is_default,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Deal(Base):
    __tablename__ = 'deal'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    pipeline_id = Column(Integer, ForeignKey('pipeline.id'), nullable=False)
    
    # Deal Information
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Deal Status
    stage = Column(Enum(DealStage), default=DealStage.PROSPECTING)
    probability = Column(Integer, default=0)  # 0-100
    
    # Financial Information
    value = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    
    # Deal Timeline
    expected_close_date = Column(DateTime)
    actual_close_date = Column(DateTime)
    
    # Assignment
    assigned_to = Column(Integer, ForeignKey('user.id'))
    
    # Deal Properties
    is_won = Column(Boolean, default=False)
    is_lost = Column(Boolean, default=False)
    lost_reason = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="deals")
    user = relationship("User", foreign_keys=[user_id], back_populates="deals")
    customer = relationship("Customer", back_populates="deals")
    pipeline = relationship("Pipeline", back_populates="deals")
    assigned_user = relationship("User", foreign_keys=[assigned_to])
    activities = relationship("Activity", back_populates="deal", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Deal {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'customer_id': self.customer_id,
            'pipeline_id': self.pipeline_id,
            'title': self.title,
            'description': self.description,
            'stage': self.stage.value,
            'probability': self.probability,
            'value': self.value,
            'currency': self.currency,
            'expected_close_date': self.expected_close_date.isoformat() if self.expected_close_date else None,
            'actual_close_date': self.actual_close_date.isoformat() if self.actual_close_date else None,
            'assigned_to': self.assigned_to,
            'is_won': self.is_won,
            'is_lost': self.is_lost,
            'lost_reason': self.lost_reason,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Activity(Base):
    __tablename__ = 'activity'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Activity can be linked to different entities
    customer_id = Column(Integer, ForeignKey('customer.id'))
    lead_id = Column(Integer, ForeignKey('lead.id'))
    deal_id = Column(Integer, ForeignKey('deal.id'))
    
    # Activity Information
    type = Column(Enum(ActivityType), nullable=False)
    subject = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Activity Status
    is_completed = Column(Boolean, default=False)
    is_high_priority = Column(Boolean, default=False)
    
    # Timing
    scheduled_at = Column(DateTime)
    completed_at = Column(DateTime)
    duration_minutes = Column(Integer)
    
    # Communication details
    phone_number = Column(String(20))
    email_address = Column(String(255))
    
    # Outcome
    outcome = Column(Text)
    next_action = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="activities")
    user = relationship("User", back_populates="activities")
    customer = relationship("Customer", back_populates="activities")
    lead = relationship("Lead", back_populates="activities")
    deal = relationship("Deal", back_populates="activities")
    
    def __repr__(self):
        return f'<Activity {self.subject}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'customer_id': self.customer_id,
            'lead_id': self.lead_id,
            'deal_id': self.deal_id,
            'type': self.type.value,
            'subject': self.subject,
            'description': self.description,
            'is_completed': self.is_completed,
            'is_high_priority': self.is_high_priority,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_minutes': self.duration_minutes,
            'phone_number': self.phone_number,
            'email_address': self.email_address,
            'outcome': self.outcome,
            'next_action': self.next_action,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }