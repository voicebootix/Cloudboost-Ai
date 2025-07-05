from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class CampaignStatus(enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class MessageStatus(enum.Enum):
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    BOUNCED = "bounced"
    OPENED = "opened"
    CLICKED = "clicked"
    REPLIED = "replied"

class CallStatus(enum.Enum):
    INITIATED = "initiated"
    RINGING = "ringing"
    ANSWERED = "answered"
    COMPLETED = "completed"
    FAILED = "failed"
    BUSY = "busy"
    NO_ANSWER = "no_answer"

class EmailCampaign(Base):
    __tablename__ = 'email_campaign'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Campaign Information
    name = Column(String(200), nullable=False)
    subject = Column(String(500), nullable=False)
    description = Column(Text)
    
    # Email Content
    html_content = Column(Text)
    text_content = Column(Text)
    
    # Campaign Settings
    from_email = Column(String(255), nullable=False)
    from_name = Column(String(100))
    reply_to = Column(String(255))
    
    # Targeting
    recipient_list = Column(JSON)  # List of email addresses
    segment_criteria = Column(JSON)  # Criteria for dynamic segmentation
    
    # Scheduling
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    
    # Tracking
    total_recipients = Column(Integer, default=0)
    total_sent = Column(Integer, default=0)
    total_delivered = Column(Integer, default=0)
    total_bounced = Column(Integer, default=0)
    total_opened = Column(Integer, default=0)
    total_clicked = Column(Integer, default=0)
    total_unsubscribed = Column(Integer, default=0)
    
    # A/B Testing
    is_ab_test = Column(Boolean, default=False)
    ab_test_percentage = Column(Integer, default=50)
    ab_test_winner = Column(String(10))  # 'A' or 'B'
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="email_campaigns")
    user = relationship("User", back_populates="email_campaigns")
    
    def __repr__(self):
        return f'<EmailCampaign {self.name}>'
    
    @property
    def open_rate(self):
        if self.total_delivered > 0:
            return (self.total_opened / self.total_delivered) * 100
        return 0
    
    @property
    def click_rate(self):
        if self.total_delivered > 0:
            return (self.total_clicked / self.total_delivered) * 100
        return 0
    
    @property
    def bounce_rate(self):
        if self.total_sent > 0:
            return (self.total_bounced / self.total_sent) * 100
        return 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'name': self.name,
            'subject': self.subject,
            'description': self.description,
            'html_content': self.html_content,
            'text_content': self.text_content,
            'from_email': self.from_email,
            'from_name': self.from_name,
            'reply_to': self.reply_to,
            'recipient_list': self.recipient_list,
            'segment_criteria': self.segment_criteria,
            'status': self.status.value,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'total_recipients': self.total_recipients,
            'total_sent': self.total_sent,
            'total_delivered': self.total_delivered,
            'total_bounced': self.total_bounced,
            'total_opened': self.total_opened,
            'total_clicked': self.total_clicked,
            'total_unsubscribed': self.total_unsubscribed,
            'is_ab_test': self.is_ab_test,
            'ab_test_percentage': self.ab_test_percentage,
            'ab_test_winner': self.ab_test_winner,
            'open_rate': self.open_rate,
            'click_rate': self.click_rate,
            'bounce_rate': self.bounce_rate,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class SMSCampaign(Base):
    __tablename__ = 'sms_campaign'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Campaign Information
    name = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    description = Column(Text)
    
    # SMS Settings
    from_number = Column(String(20), nullable=False)
    
    # Targeting
    recipient_list = Column(JSON)  # List of phone numbers
    segment_criteria = Column(JSON)  # Criteria for dynamic segmentation
    
    # Scheduling
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    
    # Tracking
    total_recipients = Column(Integer, default=0)
    total_sent = Column(Integer, default=0)
    total_delivered = Column(Integer, default=0)
    total_failed = Column(Integer, default=0)
    total_replies = Column(Integer, default=0)
    
    # Cost tracking
    cost_per_sms = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="sms_campaigns")
    user = relationship("User", back_populates="sms_campaigns")
    
    def __repr__(self):
        return f'<SMSCampaign {self.name}>'
    
    @property
    def delivery_rate(self):
        if self.total_sent > 0:
            return (self.total_delivered / self.total_sent) * 100
        return 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'name': self.name,
            'message': self.message,
            'description': self.description,
            'from_number': self.from_number,
            'recipient_list': self.recipient_list,
            'segment_criteria': self.segment_criteria,
            'status': self.status.value,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'total_recipients': self.total_recipients,
            'total_sent': self.total_sent,
            'total_delivered': self.total_delivered,
            'total_failed': self.total_failed,
            'total_replies': self.total_replies,
            'cost_per_sms': self.cost_per_sms,
            'total_cost': self.total_cost,
            'delivery_rate': self.delivery_rate,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class WhatsAppMessage(Base):
    __tablename__ = 'whatsapp_message'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Message Information
    to_number = Column(String(20), nullable=False)
    from_number = Column(String(20), nullable=False)
    message_type = Column(String(20), default='text')  # text, image, document, template
    
    # Content
    content = Column(Text)
    media_url = Column(String(500))
    media_type = Column(String(50))
    
    # Template messaging
    template_name = Column(String(100))
    template_parameters = Column(JSON)
    
    # Status
    status = Column(Enum(MessageStatus), default=MessageStatus.QUEUED)
    whatsapp_message_id = Column(String(100))
    
    # Delivery tracking
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    read_at = Column(DateTime)
    
    # Response tracking
    is_inbound = Column(Boolean, default=False)
    conversation_id = Column(String(100))
    
    # Error handling
    error_code = Column(String(50))
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="whatsapp_messages")
    user = relationship("User", back_populates="whatsapp_messages")
    
    def __repr__(self):
        return f'<WhatsAppMessage {self.to_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'to_number': self.to_number,
            'from_number': self.from_number,
            'message_type': self.message_type,
            'content': self.content,
            'media_url': self.media_url,
            'media_type': self.media_type,
            'template_name': self.template_name,
            'template_parameters': self.template_parameters,
            'status': self.status.value,
            'whatsapp_message_id': self.whatsapp_message_id,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'is_inbound': self.is_inbound,
            'conversation_id': self.conversation_id,
            'error_code': self.error_code,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CallLog(Base):
    __tablename__ = 'call_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Call Information
    from_number = Column(String(20), nullable=False)
    to_number = Column(String(20), nullable=False)
    direction = Column(String(10), nullable=False)  # 'inbound' or 'outbound'
    
    # Call Status
    status = Column(Enum(CallStatus), default=CallStatus.INITIATED)
    
    # Call Details
    duration_seconds = Column(Integer, default=0)
    recording_url = Column(String(500))
    
    # Timestamps
    initiated_at = Column(DateTime, default=datetime.utcnow)
    answered_at = Column(DateTime)
    ended_at = Column(DateTime)
    
    # Call provider details
    provider_call_id = Column(String(100))
    provider_details = Column(JSON)
    
    # Cost tracking
    cost = Column(Float, default=0.0)
    
    # Notes and outcomes
    notes = Column(Text)
    outcome = Column(String(100))
    follow_up_required = Column(Boolean, default=False)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="call_logs")
    user = relationship("User", back_populates="call_logs")
    
    def __repr__(self):
        return f'<CallLog {self.from_number} -> {self.to_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'from_number': self.from_number,
            'to_number': self.to_number,
            'direction': self.direction,
            'status': self.status.value,
            'duration_seconds': self.duration_seconds,
            'recording_url': self.recording_url,
            'initiated_at': self.initiated_at.isoformat(),
            'answered_at': self.answered_at.isoformat() if self.answered_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'provider_call_id': self.provider_call_id,
            'provider_details': self.provider_details,
            'cost': self.cost,
            'notes': self.notes,
            'outcome': self.outcome,
            'follow_up_required': self.follow_up_required,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }