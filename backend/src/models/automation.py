from datetime import datetime
from sqlalchemy import Enum, JSON, Float
from sqlalchemy.orm import relationship
import enum

# Import db from database module
from ..database import db

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

class Workflow(db.Model):
    __tablename__ = 'workflow'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Workflow Information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Workflow Configuration
    trigger_type = db.Column(Enum(WorkflowTrigger), nullable=False)
    trigger_config = db.Column(JSON)
    
    # Status
    status = db.Column(Enum(WorkflowStatus), default=WorkflowStatus.DRAFT)
    
    # Execution Settings
    is_active = db.Column(db.Boolean, default=False)
    max_executions = db.Column(db.Integer, default=0)  # 0 = unlimited
    execution_count = db.Column(db.Integer, default=0)
    
    # Scheduling (for scheduled workflows)
    schedule_pattern = db.Column(db.String(100))  # cron pattern
    next_run_at = db.Column(db.DateTime)
    last_run_at = db.Column(db.DateTime)
    
    # Performance Metrics
    success_rate = db.Column(Float, default=0.0)
    average_execution_time = db.Column(db.Integer, default=0)  # in seconds
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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

class WorkflowStep(db.Model):
    __tablename__ = 'workflow_step'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'), nullable=False)
    
    # Step Information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    step_type = db.Column(Enum(StepType), nullable=False)
    
    # Step Configuration
    config = db.Column(JSON)
    
    # Step Order
    order = db.Column(db.Integer, nullable=False)
    
    # Conditional Logic
    condition = db.Column(JSON)  # Conditions for this step to execute
    
    # Timing
    delay_minutes = db.Column(db.Integer, default=0)
    
    # Error Handling
    on_error = db.Column(db.String(20), default='stop')  # 'stop', 'continue', 'retry'
    max_retries = db.Column(db.Integer, default=0)
    
    # Performance Tracking
    execution_count = db.Column(db.Integer, default=0)
    success_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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

class WorkflowExecution(db.Model):
    __tablename__ = 'workflow_execution'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'), nullable=False)
    
    # Execution Information
    status = db.Column(Enum(ExecutionStatus), default=ExecutionStatus.PENDING)
    
    # Trigger Context
    trigger_data = db.Column(JSON)
    
    # Execution Progress
    current_step = db.Column(db.Integer, default=0)
    completed_steps = db.Column(db.Integer, default=0)
    total_steps = db.Column(db.Integer, default=0)
    
    # Execution Results
    results = db.Column(JSON)
    error_message = db.Column(db.Text)
    
    # Timing
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Integer, default=0)
    
    # Context Data
    context = db.Column(JSON)  # Data passed between steps
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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