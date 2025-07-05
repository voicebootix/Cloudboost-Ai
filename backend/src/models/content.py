from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class ContentType(enum.Enum):
    BLOG_POST = "blog_post"
    SOCIAL_POST = "social_post"
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    PRODUCT_DESCRIPTION = "product_description"
    AD_COPY = "ad_copy"
    PRESS_RELEASE = "press_release"

class ContentStatus(enum.Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class ScheduleStatus(enum.Enum):
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Content(Base):
    __tablename__ = 'content'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    title = Column(String(500), nullable=False)
    content_type = Column(Enum(ContentType), nullable=False)
    content_body = Column(Text, nullable=False)
    content_html = Column(Text)
    
    # AI Generation details
    prompt = Column(Text)
    ai_model = Column(String(100))
    ai_generated = Column(Boolean, default=False)
    
    # Metadata
    tags = Column(JSON)
    keywords = Column(JSON)
    target_audience = Column(String(200))
    tone = Column(String(50))
    language = Column(String(10), default='en')
    
    # Status and workflow
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT)
    approved_by = Column(Integer, ForeignKey('user.id'))
    approved_at = Column(DateTime)
    
    # SEO fields
    meta_title = Column(String(200))
    meta_description = Column(String(500))
    slug = Column(String(200))
    
    # Performance tracking
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="content")
    user = relationship("User", foreign_keys=[user_id], back_populates="content")
    approver = relationship("User", foreign_keys=[approved_by])
    schedules = relationship("ContentSchedule", back_populates="content", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Content {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'title': self.title,
            'content_type': self.content_type.value,
            'content_body': self.content_body,
            'content_html': self.content_html,
            'prompt': self.prompt,
            'ai_model': self.ai_model,
            'ai_generated': self.ai_generated,
            'tags': self.tags,
            'keywords': self.keywords,
            'target_audience': self.target_audience,
            'tone': self.tone,
            'language': self.language,
            'status': self.status.value,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
            'slug': self.slug,
            'views': self.views,
            'likes': self.likes,
            'shares': self.shares,
            'comments': self.comments,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'published_at': self.published_at.isoformat() if self.published_at else None
        }

class ContentTemplate(Base):
    __tablename__ = 'content_template'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    name = Column(String(200), nullable=False)
    description = Column(Text)
    content_type = Column(Enum(ContentType), nullable=False)
    
    # Template content
    template_body = Column(Text, nullable=False)
    template_html = Column(Text)
    
    # Variables that can be replaced
    variables = Column(JSON)  # ["{{company_name}}", "{{product_name}}"]
    
    # Template metadata
    category = Column(String(100))
    tags = Column(JSON)
    is_public = Column(Boolean, default=False)
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="content_templates")
    user = relationship("User", back_populates="content_templates")
    
    def __repr__(self):
        return f'<ContentTemplate {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'content_type': self.content_type.value,
            'template_body': self.template_body,
            'template_html': self.template_html,
            'variables': self.variables,
            'category': self.category,
            'tags': self.tags,
            'is_public': self.is_public,
            'usage_count': self.usage_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ContentSchedule(Base):
    __tablename__ = 'content_schedule'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    content_id = Column(Integer, ForeignKey('content.id'), nullable=False)
    
    # Scheduling details
    scheduled_at = Column(DateTime, nullable=False)
    published_at = Column(DateTime)
    
    # Platform details
    platform = Column(String(50), nullable=False)  # 'facebook', 'linkedin', 'twitter', 'instagram'
    platform_account_id = Column(String(100))
    
    # Status
    status = Column(Enum(ScheduleStatus), default=ScheduleStatus.SCHEDULED)
    
    # Response from platform
    platform_post_id = Column(String(100))
    platform_response = Column(JSON)
    error_message = Column(Text)
    
    # Retry mechanism
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="content_schedules")
    content = relationship("Content", back_populates="schedules")
    
    def __repr__(self):
        return f'<ContentSchedule {self.content_id} -> {self.platform}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'content_id': self.content_id,
            'scheduled_at': self.scheduled_at.isoformat(),
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'platform': self.platform,
            'platform_account_id': self.platform_account_id,
            'status': self.status.value,
            'platform_post_id': self.platform_post_id,
            'platform_response': self.platform_response,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }