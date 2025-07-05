from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class WorkflowStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    INACTIVE = "inactive"

class WorkflowTrigger(enum.Enum):
    MANUAL = "manual"
    SCHEDULE = "schedule"
    WEBHOOK = "webhook"
    EMAIL_RECEIVED = "email_received"
    FORM_SUBMITTED = "form_submitted"
    CUSTOMER_CREATED = "customer_created"
    DEAL_CREATED = "deal_created"
    DEAL_STAGE_CHANGED = "deal_stage_changed"
    CONTENT_PUBLISHED = "content_published"

class StepType(enum.Enum):
    SEND_EMAIL = "send_email"
    SEND_SMS = "send_sms"
    SEND_WHATSAPP = "send_whatsapp"
    CREATE_TASK = "create_task"
    UPDATE_DEAL = "update_deal"
    ADD_TAG = "add_tag"
    REMOVE_TAG = "remove_tag"
    WAIT = "wait"
    CONDITION = "condition"
    WEBHOOK = "webhook"
    AI_GENERATE_CONTENT = "ai_generate_content"

class ExecutionStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Workflow(Base):
    __tablename__ = 'workflow'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Workflow Information
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Workflow Configuration
    trigger_type = Column(Enum(WorkflowTrigger), nullable=False)
    trigger_config = Column(JSON)
    
    # Status
    status = Column(Enum(WorkflowStatus), default=WorkflowStatus.DRAFT)
    
    # Execution Settings
    is_active = Column(Boolean, default=False)
    max_executions = Column(Integer, default=0)  # 0 = unlimited
    execution_count = Column(Integer, default=0)
    
    # Scheduling (for scheduled workflows)
    schedule_pattern = Column(String(100))  # cron pattern
    next_run_at = Column(DateTime)
    last_run_at = Column(DateTime)
    
    # Performance Metrics
    success_rate = Column(Float, default=0.0)
    average_execution_time = Column(Integer, default=0)  # in seconds
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="workflows")
    user = relationship("User", back_populates="workflows")
    steps = relationship("WorkflowStep", back_populates="workflow", cascade="all, delete-orphan", order_by="WorkflowStep.order")
    executions = relationship("WorkflowExecution", back_populates="workflow", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Workflow {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'trigger_type': self.trigger_type.value,
            'trigger_config': self.trigger_config,
            'status': self.status.value,
            'is_active': self.is_active,
            'max_executions': self.max_executions,
            'execution_count': self.execution_count,
            'schedule_pattern': self.schedule_pattern,
            'next_run_at': self.next_run_at.isoformat() if self.next_run_at else None,
            'last_run_at': self.last_run_at.isoformat() if self.last_run_at else None,
            'success_rate': self.success_rate,
            'average_execution_time': self.average_execution_time,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class WorkflowStep(Base):
    __tablename__ = 'workflow_step'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    workflow_id = Column(Integer, ForeignKey('workflow.id'), nullable=False)
    
    # Step Information
    name = Column(String(200), nullable=False)
    description = Column(Text)
    step_type = Column(Enum(StepType), nullable=False)
    
    # Step Configuration
    config = Column(JSON)
    
    # Step Order
    order = Column(Integer, nullable=False)
    
    # Conditional Logic
    condition = Column(JSON)  # Conditions for this step to execute
    
    # Timing
    delay_minutes = Column(Integer, default=0)
    
    # Error Handling
    on_error = Column(String(20), default='stop')  # 'stop', 'continue', 'retry'
    max_retries = Column(Integer, default=0)
    
    # Performance Tracking
    execution_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="workflow_steps")
    workflow = relationship("Workflow", back_populates="steps")
    
    def __repr__(self):
        return f'<WorkflowStep {self.name}>'
    
    @property
    def success_rate(self):
        if self.execution_count > 0:
            return (self.success_count / self.execution_count) * 100
        return 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'workflow_id': self.workflow_id,
            'name': self.name,
            'description': self.description,
            'step_type': self.step_type.value,
            'config': self.config,
            'order': self.order,
            'condition': self.condition,
            'delay_minutes': self.delay_minutes,
            'on_error': self.on_error,
            'max_retries': self.max_retries,
            'execution_count': self.execution_count,
            'success_count': self.success_count,
            'success_rate': self.success_rate,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class WorkflowExecution(Base):
    __tablename__ = 'workflow_execution'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    workflow_id = Column(Integer, ForeignKey('workflow.id'), nullable=False)
    
    # Execution Information
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.PENDING)
    
    # Trigger Context
    trigger_data = Column(JSON)
    
    # Execution Progress
    current_step = Column(Integer, default=0)
    completed_steps = Column(Integer, default=0)
    total_steps = Column(Integer, default=0)
    
    # Execution Results
    results = Column(JSON)
    error_message = Column(Text)
    
    # Timing
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    duration_seconds = Column(Integer, default=0)
    
    # Context Data
    context = Column(JSON)  # Data passed between steps
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="workflow_executions")
    workflow = relationship("Workflow", back_populates="executions")
    
    def __repr__(self):
        return f'<WorkflowExecution {self.id}: {self.status.value}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'workflow_id': self.workflow_id,
            'status': self.status.value,
            'trigger_data': self.trigger_data,
            'current_step': self.current_step,
            'completed_steps': self.completed_steps,
            'total_steps': self.total_steps,
            'results': self.results,
            'error_message': self.error_message,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_seconds': self.duration_seconds,
            'context': self.context,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }