from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

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

class Analytics(Base):
    __tablename__ = 'analytics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    
    # Metric Information
    metric_name = Column(String(200), nullable=False)
    metric_type = Column(Enum(MetricType), nullable=False)
    category = Column(String(100), nullable=False)
    
    # Metric Value
    value = Column(Float, nullable=False)
    
    # Context and Dimensions
    dimensions = Column(JSON)  # Additional context like platform, campaign_id, etc.
    
    # Time-based tracking
    timestamp = Column(DateTime, default=datetime.utcnow)
    date = Column(DateTime, nullable=False)  # Date for aggregation
    
    # Tags for filtering
    tags = Column(JSON)
    
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

class Report(Base):
    __tablename__ = 'report'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Report Information
    name = Column(String(200), nullable=False)
    description = Column(Text)
    report_type = Column(Enum(ReportType), nullable=False)
    
    # Report Configuration
    config = Column(JSON)  # Chart types, filters, etc.
    filters = Column(JSON)  # Date ranges, dimensions, etc.
    
    # Scheduling
    is_scheduled = Column(Boolean, default=False)
    frequency = Column(Enum(ReportFrequency))
    next_run_at = Column(DateTime)
    last_run_at = Column(DateTime)
    
    # Report Recipients
    recipients = Column(JSON)  # Email addresses for scheduled reports
    
    # Report Data
    data = Column(JSON)  # Cached report data
    chart_config = Column(JSON)  # Chart configuration
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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

class KPI(Base):
    __tablename__ = 'kpi'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # KPI Information
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False)
    
    # KPI Configuration
    metric_query = Column(JSON)  # Query configuration to calculate KPI
    target_value = Column(Float)
    warning_threshold = Column(Float)
    critical_threshold = Column(Float)
    
    # Current Values
    current_value = Column(Float, default=0.0)
    previous_value = Column(Float, default=0.0)
    change_percentage = Column(Float, default=0.0)
    
    # Trend Analysis
    trend = Column(String(20))  # 'up', 'down', 'stable'
    
    # Display Settings
    display_format = Column(String(20), default='number')  # 'number', 'percentage', 'currency'
    currency_symbol = Column(String(5), default='$')
    
    # Alert Settings
    alert_on_threshold = Column(Boolean, default=False)
    alert_recipients = Column(JSON)
    
    # Update Settings
    update_frequency = Column(String(20), default='daily')  # 'hourly', 'daily', 'weekly'
    last_calculated_at = Column(DateTime)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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