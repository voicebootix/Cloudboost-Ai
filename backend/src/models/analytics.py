from datetime import datetime
from sqlalchemy import Enum, JSON, Float
from sqlalchemy.orm import relationship
import enum

# Import db from database module
from ..database import db

class MetricType(enum.Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class ReportType(enum.Enum):
    CONTENT_PERFORMANCE = "content_performance"
    CAMPAIGN_ANALYTICS = "campaign_analytics"
    CRM_PIPELINE = "crm_pipeline"
    SOCIAL_ENGAGEMENT = "social_engagement"
    REVENUE_ANALYTICS = "revenue_analytics"
    CUSTOMER_ANALYTICS = "customer_analytics"
    AUTOMATION_PERFORMANCE = "automation_performance"
    COMMUNICATION_ANALYTICS = "communication_analytics"

class ReportFrequency(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class Analytics(db.Model):
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    
    # Metric Information
    metric_name = db.Column(db.String(200), nullable=False)
    metric_type = db.Column(Enum(MetricType), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    
    # Metric Value
    value = db.Column(Float, nullable=False)
    
    # Context and Dimensions
    dimensions = db.Column(JSON)  # Additional context like platform, campaign_id, etc.
    
    # Time-based tracking
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.DateTime, nullable=False)  # Date for aggregation
    
    # Tags for filtering
    tags = db.Column(JSON)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="analytics")
    
    def __repr__(self):
        return f'<Analytics {self.metric_name}: {self.value}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'metric_name': self.metric_name,
            'metric_type': self.metric_type.value,
            'category': self.category,
            'value': self.value,
            'dimensions': self.dimensions,
            'timestamp': self.timestamp.isoformat(),
            'date': self.date.isoformat(),
            'tags': self.tags
        }

class Report(db.Model):
    __tablename__ = 'report'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Report Information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    report_type = db.Column(Enum(ReportType), nullable=False)
    
    # Report Configuration
    config = db.Column(JSON)  # Chart types, filters, etc.
    filters = db.Column(JSON)  # Date ranges, dimensions, etc.
    
    # Scheduling
    is_scheduled = db.Column(db.Boolean, default=False)
    frequency = db.Column(Enum(ReportFrequency))
    next_run_at = db.Column(db.DateTime)
    last_run_at = db.Column(db.DateTime)
    
    # Report Recipients
    recipients = db.Column(JSON)  # Email addresses for scheduled reports
    
    # Report Data
    data = db.Column(JSON)  # Cached report data
    chart_config = db.Column(JSON)  # Chart configuration
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="reports")
    user = relationship("User", back_populates="reports")
    
    def __repr__(self):
        return f'<Report {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'report_type': self.report_type.value,
            'config': self.config,
            'filters': self.filters,
            'is_scheduled': self.is_scheduled,
            'frequency': self.frequency.value if self.frequency else None,
            'next_run_at': self.next_run_at.isoformat() if self.next_run_at else None,
            'last_run_at': self.last_run_at.isoformat() if self.last_run_at else None,
            'recipients': self.recipients,
            'data': self.data,
            'chart_config': self.chart_config,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class KPI(db.Model):
    __tablename__ = 'kpi'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # KPI Information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)
    
    # KPI Configuration
    metric_query = db.Column(JSON)  # Query configuration to calculate KPI
    target_value = db.Column(Float)
    warning_threshold = db.Column(Float)
    critical_threshold = db.Column(Float)
    
    # Current Values
    current_value = db.Column(Float, default=0.0)
    previous_value = db.Column(Float, default=0.0)
    change_percentage = db.Column(Float, default=0.0)
    
    # Trend Analysis
    trend = db.Column(db.String(20))  # 'up', 'down', 'stable'
    
    # Display Settings
    display_format = db.Column(db.String(20), default='number')  # 'number', 'percentage', 'currency'
    currency_symbol = db.Column(db.String(5), default='$')
    
    # Alert Settings
    alert_on_threshold = db.Column(db.Boolean, default=False)
    alert_recipients = db.Column(JSON)
    
    # Update Settings
    update_frequency = db.Column(db.String(20), default='daily')  # 'hourly', 'daily', 'weekly'
    last_calculated_at = db.Column(db.DateTime)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="kpis")
    user = relationship("User", back_populates="kpis")
    
    def __repr__(self):
        return f'<KPI {self.name}>'
    
    @property
    def status(self):
        """Get KPI status based on thresholds"""
        if self.critical_threshold and self.current_value <= self.critical_threshold:
            return 'critical'
        elif self.warning_threshold and self.current_value <= self.warning_threshold:
            return 'warning'
        elif self.target_value and self.current_value >= self.target_value:
            return 'target_met'
        else:
            return 'normal'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'metric_query': self.metric_query,
            'target_value': self.target_value,
            'warning_threshold': self.warning_threshold,
            'critical_threshold': self.critical_threshold,
            'current_value': self.current_value,
            'previous_value': self.previous_value,
            'change_percentage': self.change_percentage,
            'trend': self.trend,
            'display_format': self.display_format,
            'currency_symbol': self.currency_symbol,
            'alert_on_threshold': self.alert_on_threshold,
            'alert_recipients': self.alert_recipients,
            'update_frequency': self.update_frequency,
            'last_calculated_at': self.last_calculated_at.isoformat() if self.last_calculated_at else None,
            'is_active': self.is_active,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }