from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
import uuid

automation_bp = Blueprint('automation', __name__)

# Sample workflow templates for different industries
WORKFLOW_TEMPLATES = {
    'lead_nurturing': {
        'name': 'Lead Nurturing Campaign',
        'description': 'Automated lead nurturing with cultural adaptation',
        'triggers': ['form_submission', 'website_visit', 'content_download'],
        'actions': [
            {'type': 'send_email', 'delay': 0, 'template': 'welcome_email'},
            {'type': 'send_whatsapp', 'delay': 24, 'template': 'follow_up_message'},
            {'type': 'assign_sales_rep', 'delay': 72, 'criteria': 'geography_culture'},
            {'type': 'schedule_call', 'delay': 120, 'template': 'demo_invitation'}
        ]
    },
    'customer_onboarding': {
        'name': 'Customer Onboarding Flow',
        'description': 'Comprehensive onboarding with regional customization',
        'triggers': ['purchase_completed', 'subscription_activated'],
        'actions': [
            {'type': 'send_welcome_kit', 'delay': 0, 'language': 'customer_preferred'},
            {'type': 'schedule_onboarding_call', 'delay': 24, 'timezone': 'customer_local'},
            {'type': 'send_tutorial_videos', 'delay': 48, 'content': 'industry_specific'},
            {'type': 'check_progress', 'delay': 168, 'trigger': 'usage_analytics'}
        ]
    },
    'churn_prevention': {
        'name': 'Churn Prevention Automation',
        'description': 'Proactive customer retention with cultural sensitivity',
        'triggers': ['low_engagement', 'support_tickets', 'usage_decline'],
        'actions': [
            {'type': 'analyze_behavior', 'delay': 0, 'model': 'churn_prediction'},
            {'type': 'personalized_outreach', 'delay': 12, 'channel': 'preferred'},
            {'type': 'offer_assistance', 'delay': 48, 'type': 'cultural_appropriate'},
            {'type': 'escalate_to_manager', 'delay': 120, 'criteria': 'high_value_customer'}
        ]
    }
}

# AI Decision Engine Rules
DECISION_RULES = {
    'lead_scoring': {
        'factors': [
            {'name': 'company_size', 'weight': 0.3, 'values': {'enterprise': 100, 'medium': 70, 'small': 40}},
            {'name': 'industry', 'weight': 0.2, 'values': {'technology': 90, 'healthcare': 85, 'finance': 80}},
            {'name': 'geography', 'weight': 0.2, 'values': {'sri_lanka': 95, 'india': 90, 'pakistan': 85}},
            {'name': 'engagement', 'weight': 0.3, 'values': {'high': 100, 'medium': 60, 'low': 20}}
        ],
        'thresholds': {'hot': 80, 'warm': 60, 'cold': 40}
    },
    'channel_selection': {
        'preferences': {
            'sri_lanka': ['whatsapp', 'email', 'voice', 'sms'],
            'india': ['whatsapp', 'email', 'sms', 'voice'],
            'pakistan': ['whatsapp', 'voice', 'sms', 'email'],
            'bangladesh': ['whatsapp', 'voice', 'email', 'sms'],
            'nepal': ['whatsapp', 'email', 'voice', 'sms']
        },
        'cultural_factors': {
            'business_hours': {'start': 9, 'end': 18},
            'religious_considerations': ['friday_prayers', 'ramadan_timing'],
            'festival_awareness': ['diwali', 'vesak', 'eid', 'poya_days']
        }
    }
}

@automation_bp.route('/workflows', methods=['GET'])
def get_workflows():
    """Get all available workflow templates"""
    try:
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return jsonify({'error': 'Tenant ID required'}), 400
        
        return jsonify({
            'success': True,
            'workflows': WORKFLOW_TEMPLATES,
            'total': len(WORKFLOW_TEMPLATES)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@automation_bp.route('/workflows', methods=['POST'])
def create_workflow():
    """Create a new automation workflow"""
    try:
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return jsonify({'error': 'Tenant ID required'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'triggers', 'actions']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create workflow
        workflow = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'name': data['name'],
            'description': data.get('description', ''),
            'triggers': data['triggers'],
            'actions': data['actions'],
            'status': 'active',
            'created_at': datetime.utcnow().isoformat(),
            'cultural_settings': data.get('cultural_settings', {}),
            'performance_metrics': {
                'executions': 0,
                'success_rate': 0,
                'avg_conversion': 0
            }
        }
        
        return jsonify({
            'success': True,
            'workflow': workflow,
            'message': 'Workflow created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@automation_bp.route('/workflows/<workflow_id>/execute', methods=['POST'])
def execute_workflow(workflow_id):
    """Execute a specific workflow"""
    try:
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return jsonify({'error': 'Tenant ID required'}), 400
        
        data = request.get_json()
        customer_data = data.get('customer_data', {})
        trigger_event = data.get('trigger_event', '')
        
        # Simulate workflow execution
        execution = {
            'id': str(uuid.uuid4()),
            'workflow_id': workflow_id,
            'tenant_id': tenant_id,
            'customer_id': customer_data.get('id'),
            'trigger_event': trigger_event,
            'status': 'running',
            'started_at': datetime.utcnow().isoformat(),
            'steps_completed': 0,
            'total_steps': 4,
            'cultural_adaptations': {
                'language': customer_data.get('preferred_language', 'english'),
                'timezone': customer_data.get('timezone', 'Asia/Colombo'),
                'communication_style': customer_data.get('communication_style', 'formal')
            }
        }
        
        return jsonify({
            'success': True,
            'execution': execution,
            'message': 'Workflow execution started'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@automation_bp.route('/decision-engine/score-lead', methods=['POST'])
def score_lead():
    """AI-powered lead scoring"""
    try:
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return jsonify({'error': 'Tenant ID required'}), 400
        
        data = request.get_json()
        lead_data = data.get('lead_data', {})
        
        # Calculate lead score using AI decision rules
        total_score = 0
        scoring_details = []
        
        for factor in DECISION_RULES['lead_scoring']['factors']:
            factor_value = lead_data.get(factor['name'], '')
            factor_score = factor['values'].get(factor_value, 0)
            weighted_score = factor_score * factor['weight']
            total_score += weighted_score
            
            scoring_details.append({
                'factor': factor['name'],
                'value': factor_value,
                'score': factor_score,
                'weight': factor['weight'],
                'weighted_score': weighted_score
            })
        
        # Determine lead category
        thresholds = DECISION_RULES['lead_scoring']['thresholds']
        if total_score >= thresholds['hot']:
            category = 'hot'
        elif total_score >= thresholds['warm']:
            category = 'warm'
        else:
            category = 'cold'
        
        # Cultural recommendations
        geography = lead_data.get('geography', 'sri_lanka')
        cultural_recommendations = {
            'preferred_channels': DECISION_RULES['channel_selection']['preferences'].get(geography, []),
            'cultural_factors': DECISION_RULES['channel_selection']['cultural_factors'],
            'recommended_approach': 'relationship_building' if geography in ['sri_lanka', 'india'] else 'direct_business'
        }
        
        return jsonify({
            'success': True,
            'lead_score': round(total_score, 2),
            'category': category,
            'scoring_details': scoring_details,
            'cultural_recommendations': cultural_recommendations,
            'next_actions': [
                f'Assign to {category} lead queue',
                f'Use {cultural_recommendations["preferred_channels"][0]} for initial contact',
                'Schedule follow-up based on cultural timing preferences'
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@automation_bp.route('/decision-engine/optimize-timing', methods=['POST'])
def optimize_timing():
    """AI-powered communication timing optimization"""
    try:
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return jsonify({'error': 'Tenant ID required'}), 400
        
        data = request.get_json()
        customer_data = data.get('customer_data', {})
        communication_type = data.get('communication_type', 'email')
        
        # Analyze optimal timing based on cultural and behavioral factors
        geography = customer_data.get('geography', 'sri_lanka')
        timezone = customer_data.get('timezone', 'Asia/Colombo')
        
        # Cultural timing considerations
        cultural_factors = DECISION_RULES['channel_selection']['cultural_factors']
        business_hours = cultural_factors['business_hours']
        
        # Calculate optimal send time
        now = datetime.utcnow()
        optimal_time = now.replace(hour=business_hours['start'] + 2, minute=0, second=0)
        
        # Adjust for weekends and cultural considerations
        if optimal_time.weekday() == 4:  # Friday
            optimal_time += timedelta(hours=2)  # Avoid Friday prayers
        elif optimal_time.weekday() >= 5:  # Weekend
            optimal_time += timedelta(days=7-optimal_time.weekday())  # Move to Monday
        
        return jsonify({
            'success': True,
            'optimal_time': optimal_time.isoformat(),
            'timezone': timezone,
            'cultural_considerations': {
                'geography': geography,
                'business_hours': f"{business_hours['start']}:00 - {business_hours['end']}:00",
                'religious_factors': cultural_factors['religious_considerations'],
                'festival_awareness': cultural_factors['festival_awareness']
            },
            'recommendations': [
                f'Send {communication_type} at {optimal_time.strftime("%H:%M")} local time',
                'Avoid religious observance times',
                'Consider local festivals and holidays',
                'Respect weekend preferences'
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@automation_bp.route('/analytics/workflow-performance', methods=['GET'])
def get_workflow_performance():
    """Get workflow performance analytics"""
    try:
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return jsonify({'error': 'Tenant ID required'}), 400
        
        # Sample performance data
        performance_data = {
            'total_workflows': 15,
            'active_workflows': 12,
            'total_executions': 2847,
            'success_rate': 87.3,
            'avg_conversion_rate': 12.8,
            'top_performing_workflows': [
                {
                    'name': 'Lead Nurturing Campaign',
                    'executions': 1250,
                    'success_rate': 92.1,
                    'conversion_rate': 15.6
                },
                {
                    'name': 'Customer Onboarding Flow',
                    'executions': 890,
                    'success_rate': 89.4,
                    'conversion_rate': 18.2
                },
                {
                    'name': 'Churn Prevention Automation',
                    'executions': 456,
                    'success_rate': 78.9,
                    'conversion_rate': 8.7
                }
            ],
            'regional_performance': {
                'sri_lanka': {'success_rate': 91.2, 'conversion_rate': 14.5},
                'india': {'success_rate': 88.7, 'conversion_rate': 13.1},
                'pakistan': {'success_rate': 85.3, 'conversion_rate': 11.8},
                'bangladesh': {'success_rate': 82.1, 'conversion_rate': 10.9},
                'nepal': {'success_rate': 79.6, 'conversion_rate': 9.7}
            },
            'cultural_effectiveness': {
                'language_adaptation': 94.2,
                'timing_optimization': 88.7,
                'channel_preference': 91.5,
                'cultural_sensitivity': 89.3
            }
        }
        
        return jsonify({
            'success': True,
            'performance': performance_data,
            'generated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@automation_bp.route('/triggers', methods=['POST'])
def create_trigger():
    """Create a new automation trigger"""
    try:
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return jsonify({'error': 'Tenant ID required'}), 400
        
        data = request.get_json()
        
        trigger = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'name': data['name'],
            'type': data['type'],  # 'event', 'time', 'condition'
            'conditions': data.get('conditions', {}),
            'workflow_id': data['workflow_id'],
            'status': 'active',
            'created_at': datetime.utcnow().isoformat(),
            'cultural_settings': data.get('cultural_settings', {})
        }
        
        return jsonify({
            'success': True,
            'trigger': trigger,
            'message': 'Trigger created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@automation_bp.route('/predictions/customer-behavior', methods=['POST'])
def predict_customer_behavior():
    """Predict customer behavior using AI models"""
    try:
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return jsonify({'error': 'Tenant ID required'}), 400
        
        data = request.get_json()
        customer_data = data.get('customer_data', {})
        
        # Simulate AI predictions
        predictions = {
            'churn_risk': {
                'probability': 0.23,
                'risk_level': 'low',
                'factors': ['recent_engagement', 'payment_history', 'support_satisfaction'],
                'recommended_actions': [
                    'Continue regular engagement',
                    'Monitor usage patterns',
                    'Proactive check-in in 30 days'
                ]
            },
            'upsell_opportunity': {
                'probability': 0.67,
                'confidence': 'high',
                'recommended_products': ['premium_features', 'additional_users', 'advanced_analytics'],
                'optimal_timing': '2-3 weeks',
                'cultural_approach': 'relationship_building'
            },
            'engagement_likelihood': {
                'email': 0.78,
                'whatsapp': 0.89,
                'sms': 0.65,
                'voice': 0.72,
                'optimal_channel': 'whatsapp',
                'best_time': '10:00-12:00 local time'
            },
            'lifetime_value': {
                'predicted_value': 15750,
                'confidence_interval': [12500, 19000],
                'growth_potential': 'high',
                'retention_probability': 0.84
            }
        }
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'model_version': '2.1.0',
            'generated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

