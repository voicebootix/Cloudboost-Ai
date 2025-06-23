from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timedelta
import json
import uuid
from src.models.user import db, User, BusinessProfile

crm_bp = Blueprint('crm', __name__)

# Customer status types
CUSTOMER_STATUS = {
    'lead': 'Lead',
    'prospect': 'Prospect', 
    'customer': 'Customer',
    'inactive': 'Inactive',
    'churned': 'Churned'
}

# Lead sources
LEAD_SOURCES = {
    'website': 'Website',
    'social_media': 'Social Media',
    'email_campaign': 'Email Campaign',
    'referral': 'Referral',
    'cold_outreach': 'Cold Outreach',
    'event': 'Event',
    'advertisement': 'Advertisement',
    'whatsapp': 'WhatsApp',
    'phone_call': 'Phone Call'
}

# Deal stages
DEAL_STAGES = {
    'qualification': 'Qualification',
    'needs_analysis': 'Needs Analysis',
    'proposal': 'Proposal',
    'negotiation': 'Negotiation',
    'closed_won': 'Closed Won',
    'closed_lost': 'Closed Lost'
}

# Activity types
ACTIVITY_TYPES = {
    'call': 'Phone Call',
    'email': 'Email',
    'meeting': 'Meeting',
    'whatsapp': 'WhatsApp Message',
    'social_interaction': 'Social Media Interaction',
    'note': 'Note',
    'task': 'Task'
}

def calculate_lead_score(lead_data):
    """Calculate lead score based on various factors"""
    score = 0
    
    # Demographic scoring
    if lead_data.get('company_size'):
        company_size = lead_data['company_size']
        if company_size == 'enterprise':
            score += 30
        elif company_size == 'medium':
            score += 20
        elif company_size == 'small':
            score += 10
    
    # Engagement scoring
    if lead_data.get('email_opened'):
        score += 5
    if lead_data.get('website_visits', 0) > 3:
        score += 10
    if lead_data.get('social_engagement'):
        score += 8
    
    # Source scoring
    source = lead_data.get('source', '')
    if source == 'referral':
        score += 25
    elif source == 'website':
        score += 15
    elif source == 'social_media':
        score += 12
    
    # Geographic scoring (South Asian markets)
    country = lead_data.get('country', '')
    if country in ['IN', 'LK', 'PK', 'BD']:
        score += 15
    
    # Budget indication
    if lead_data.get('budget_range'):
        budget = lead_data['budget_range']
        if budget == 'high':
            score += 20
        elif budget == 'medium':
            score += 10
        elif budget == 'low':
            score += 5
    
    return min(score, 100)  # Cap at 100

def predict_customer_lifetime_value(customer_data):
    """Predict customer lifetime value based on historical data"""
    # Simplified CLV calculation
    base_value = 1000  # Base CLV in USD
    
    # Adjust based on company size
    company_size = customer_data.get('company_size', 'small')
    if company_size == 'enterprise':
        base_value *= 5
    elif company_size == 'medium':
        base_value *= 2.5
    
    # Adjust based on engagement level
    engagement_score = customer_data.get('engagement_score', 50)
    engagement_multiplier = engagement_score / 50
    
    # Adjust based on geographic market
    country = customer_data.get('country', 'LK')
    market_multipliers = {
        'IN': 1.2,  # India - larger market
        'LK': 1.0,  # Sri Lanka - base
        'PK': 0.9,  # Pakistan
        'BD': 0.8,  # Bangladesh
        'NP': 0.7,  # Nepal
        'MM': 0.6   # Myanmar
    }
    
    market_multiplier = market_multipliers.get(country, 1.0)
    
    clv = base_value * engagement_multiplier * market_multiplier
    return round(clv, 2)

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
        
        # Simulate customer data
        customers = []
        for i in range(per_page):
            customer = {
                'id': str(uuid.uuid4()),
                'tenant_id': tenant_id,
                'name': f'Customer {i+1}',
                'email': f'customer{i+1}@example.com',
                'phone': f'+94771234{567+i}',
                'company': f'Company {i+1}',
                'status': status or 'customer',
                'country': country or 'LK',
                'city': 'Colombo',
                'source': 'website',
                'created_at': (datetime.utcnow() - timedelta(days=i*5)).isoformat(),
                'last_contact': (datetime.utcnow() - timedelta(days=i)).isoformat(),
                'lifetime_value': predict_customer_lifetime_value({
                    'company_size': 'medium',
                    'engagement_score': 75,
                    'country': country or 'LK'
                }),
                'total_orders': 3 + i,
                'total_spent': 1500.00 + (i * 250),
                'engagement_score': 75 + (i % 25)
            }
            customers.append(customer)
        
        return jsonify({
            'customers': customers,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': 500,  # Simulated total
                'pages': 25
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
        
        # Create customer record
        customer = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'name': data['name'],
            'email': data['email'],
            'phone': data.get('phone'),
            'company': data.get('company'),
            'status': data.get('status', 'lead'),
            'country': data.get('country', 'LK'),
            'city': data.get('city'),
            'address': data.get('address'),
            'source': data.get('source', 'manual'),
            'notes': data.get('notes'),
            'tags': data.get('tags', []),
            'custom_fields': data.get('custom_fields', {}),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'lead_score': calculate_lead_score(data) if data.get('status') == 'lead' else None,
            'lifetime_value': predict_customer_lifetime_value(data),
            'engagement_score': 50  # Default engagement score
        }
        
        return jsonify({
            'success': True,
            'message': 'Customer created successfully',
            'customer': customer
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/customers/<customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Simulate customer data with detailed information
        customer = {
            'id': customer_id,
            'tenant_id': tenant_id,
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+94771234567',
            'company': 'ABC Company',
            'status': 'customer',
            'country': 'LK',
            'city': 'Colombo',
            'address': '123 Main Street, Colombo 03',
            'source': 'website',
            'created_at': '2025-06-01T10:00:00Z',
            'updated_at': '2025-06-22T08:30:00Z',
            'last_contact': '2025-06-21T14:20:00Z',
            'lifetime_value': 2500.00,
            'total_orders': 5,
            'total_spent': 3750.00,
            'engagement_score': 85,
            'lead_score': None,
            'tags': ['vip', 'enterprise'],
            'custom_fields': {
                'industry': 'Technology',
                'company_size': 'medium',
                'decision_maker': True
            },
            'social_profiles': {
                'linkedin': 'https://linkedin.com/in/johndoe',
                'facebook': 'https://facebook.com/johndoe'
            },
            'communication_preferences': {
                'preferred_channel': 'email',
                'language': 'en',
                'timezone': 'Asia/Colombo'
            }
        }
        
        return jsonify({
            'customer': customer
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/customers/<customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Simulate customer update
        updated_customer = {
            'id': customer_id,
            'tenant_id': tenant_id,
            'updated_at': datetime.utcnow().isoformat(),
            **data  # Merge with provided data
        }
        
        # Recalculate scores if relevant data changed
        if 'status' in data and data['status'] == 'lead':
            updated_customer['lead_score'] = calculate_lead_score(data)
        
        if any(field in data for field in ['company_size', 'engagement_score', 'country']):
            updated_customer['lifetime_value'] = predict_customer_lifetime_value(data)
        
        return jsonify({
            'success': True,
            'message': 'Customer updated successfully',
            'customer': updated_customer
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/leads', methods=['GET'])
@jwt_required()
def get_leads():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        source = request.args.get('source')
        score_min = request.args.get('score_min', type=int)
        
        # Simulate lead data
        leads = []
        for i in range(per_page):
            lead_data = {
                'company_size': ['small', 'medium', 'enterprise'][i % 3],
                'source': source or ['website', 'social_media', 'referral'][i % 3],
                'country': 'LK',
                'email_opened': i % 2 == 0,
                'website_visits': i + 2,
                'social_engagement': i % 3 == 0,
                'budget_range': ['low', 'medium', 'high'][i % 3]
            }
            
            lead = {
                'id': str(uuid.uuid4()),
                'tenant_id': tenant_id,
                'name': f'Lead {i+1}',
                'email': f'lead{i+1}@example.com',
                'phone': f'+94771234{567+i}',
                'company': f'Lead Company {i+1}',
                'status': 'lead',
                'source': lead_data['source'],
                'lead_score': calculate_lead_score(lead_data),
                'created_at': (datetime.utcnow() - timedelta(days=i)).isoformat(),
                'last_activity': (datetime.utcnow() - timedelta(hours=i*2)).isoformat(),
                'assigned_to': f'sales_rep_{(i % 3) + 1}',
                'next_follow_up': (datetime.utcnow() + timedelta(days=i+1)).isoformat()
            }
            
            # Filter by minimum score if specified
            if score_min is None or lead['lead_score'] >= score_min:
                leads.append(lead)
        
        return jsonify({
            'leads': leads,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': 200,  # Simulated total
                'pages': 10
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/deals', methods=['GET'])
@jwt_required()
def get_deals():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        stage = request.args.get('stage')
        
        # Simulate deal data
        deals = []
        for i in range(per_page):
            deal = {
                'id': str(uuid.uuid4()),
                'tenant_id': tenant_id,
                'title': f'Deal {i+1} - Software License',
                'customer_id': str(uuid.uuid4()),
                'customer_name': f'Customer {i+1}',
                'value': 5000 + (i * 1000),
                'currency': 'USD',
                'stage': stage or list(DEAL_STAGES.keys())[i % len(DEAL_STAGES)],
                'probability': [20, 40, 60, 80, 100, 0][i % 6],
                'expected_close_date': (datetime.utcnow() + timedelta(days=30+i*5)).isoformat(),
                'created_at': (datetime.utcnow() - timedelta(days=i*3)).isoformat(),
                'last_activity': (datetime.utcnow() - timedelta(days=i)).isoformat(),
                'assigned_to': f'sales_rep_{(i % 3) + 1}',
                'source': ['website', 'referral', 'cold_outreach'][i % 3],
                'products': [
                    {
                        'name': 'CloudBoost AI Pro',
                        'quantity': 1,
                        'price': 3000 + (i * 500)
                    }
                ]
            }
            deals.append(deal)
        
        return jsonify({
            'deals': deals,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': 150,  # Simulated total
                'pages': 8
            },
            'pipeline_summary': {
                'total_value': sum(deal['value'] for deal in deals),
                'weighted_value': sum(deal['value'] * deal['probability'] / 100 for deal in deals),
                'stage_breakdown': {
                    'qualification': 25,
                    'needs_analysis': 20,
                    'proposal': 15,
                    'negotiation': 10,
                    'closed_won': 5,
                    'closed_lost': 3
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/deals', methods=['POST'])
@jwt_required()
def create_deal():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'customer_id', 'value']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create deal record
        deal = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'title': data['title'],
            'customer_id': data['customer_id'],
            'value': data['value'],
            'currency': data.get('currency', 'USD'),
            'stage': data.get('stage', 'qualification'),
            'probability': data.get('probability', 20),
            'expected_close_date': data.get('expected_close_date'),
            'description': data.get('description'),
            'products': data.get('products', []),
            'assigned_to': data.get('assigned_to'),
            'source': data.get('source', 'manual'),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'success': True,
            'message': 'Deal created successfully',
            'deal': deal
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/activities', methods=['GET'])
@jwt_required()
def get_activities():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Query parameters
        customer_id = request.args.get('customer_id')
        activity_type = request.args.get('type')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Simulate activity data
        activities = []
        for i in range(per_page):
            activity = {
                'id': str(uuid.uuid4()),
                'tenant_id': tenant_id,
                'customer_id': customer_id or str(uuid.uuid4()),
                'type': activity_type or list(ACTIVITY_TYPES.keys())[i % len(ACTIVITY_TYPES)],
                'subject': f'Activity {i+1}',
                'description': f'Description for activity {i+1}',
                'created_by': f'user_{(i % 3) + 1}',
                'created_at': (datetime.utcnow() - timedelta(hours=i*2)).isoformat(),
                'due_date': (datetime.utcnow() + timedelta(days=i+1)).isoformat() if i % 2 == 0 else None,
                'completed': i % 3 == 0,
                'outcome': 'Positive response' if i % 3 == 0 else None
            }
            activities.append(activity)
        
        return jsonify({
            'activities': activities,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': 300,  # Simulated total
                'pages': 15
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/activities', methods=['POST'])
@jwt_required()
def create_activity():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        user_id = get_jwt_identity()
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_id', 'type', 'subject']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create activity record
        activity = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'customer_id': data['customer_id'],
            'type': data['type'],
            'subject': data['subject'],
            'description': data.get('description'),
            'due_date': data.get('due_date'),
            'priority': data.get('priority', 'medium'),
            'assigned_to': data.get('assigned_to', user_id),
            'created_by': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'completed': False
        }
        
        return jsonify({
            'success': True,
            'message': 'Activity created successfully',
            'activity': activity
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/analytics/dashboard', methods=['GET'])
@jwt_required()
def get_crm_dashboard():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Simulate CRM dashboard analytics
        dashboard_data = {
            'overview': {
                'total_customers': 1250,
                'active_leads': 89,
                'open_deals': 45,
                'deals_value': 125000,
                'conversion_rate': 12.5,
                'avg_deal_size': 2777.78
            },
            'sales_pipeline': {
                'qualification': {'count': 25, 'value': 62500},
                'needs_analysis': {'count': 20, 'value': 55000},
                'proposal': {'count': 15, 'value': 41250},
                'negotiation': {'count': 10, 'value': 27500},
                'closed_won': {'count': 5, 'value': 13750}
            },
            'lead_sources': {
                'website': 35,
                'social_media': 28,
                'referral': 20,
                'email_campaign': 15,
                'cold_outreach': 12,
                'events': 8
            },
            'customer_segments': {
                'enterprise': {'count': 125, 'value': 75000},
                'medium': {'count': 450, 'value': 112500},
                'small': {'count': 675, 'value': 67500}
            },
            'regional_performance': {
                'LK': {'customers': 450, 'revenue': 67500},
                'IN': {'customers': 380, 'revenue': 95000},
                'PK': {'customers': 220, 'revenue': 44000},
                'BD': {'customers': 150, 'revenue': 30000},
                'NP': {'customers': 50, 'revenue': 8750}
            },
            'recent_activities': [
                {
                    'type': 'deal_won',
                    'description': 'Deal "Enterprise License" closed for $15,000',
                    'timestamp': '2025-06-22T10:30:00Z'
                },
                {
                    'type': 'new_lead',
                    'description': 'New lead "Tech Startup" from website',
                    'timestamp': '2025-06-22T09:15:00Z'
                },
                {
                    'type': 'meeting_scheduled',
                    'description': 'Demo meeting scheduled with "ABC Corp"',
                    'timestamp': '2025-06-22T08:45:00Z'
                }
            ],
            'performance_trends': {
                'monthly_revenue': [
                    {'month': '2025-01', 'revenue': 45000},
                    {'month': '2025-02', 'revenue': 52000},
                    {'month': '2025-03', 'revenue': 48000},
                    {'month': '2025-04', 'revenue': 61000},
                    {'month': '2025-05', 'revenue': 58000},
                    {'month': '2025-06', 'revenue': 67000}
                ],
                'lead_conversion': [
                    {'month': '2025-01', 'rate': 10.5},
                    {'month': '2025-02', 'rate': 11.2},
                    {'month': '2025-03', 'rate': 9.8},
                    {'month': '2025-04', 'rate': 13.1},
                    {'month': '2025-05', 'rate': 12.7},
                    {'month': '2025-06', 'rate': 14.2}
                ]
            }
        }
        
        return jsonify({
            'dashboard': dashboard_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/reports/sales-forecast', methods=['GET'])
@jwt_required()
def get_sales_forecast():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Query parameters
        months = request.args.get('months', 6, type=int)
        
        # Simulate sales forecast
        forecast = []
        base_revenue = 67000
        
        for i in range(months):
            month_date = datetime.utcnow() + timedelta(days=30*i)
            # Simulate growth with some seasonality
            growth_factor = 1 + (0.05 * i) + (0.1 * (i % 3 == 0))
            
            forecast.append({
                'month': month_date.strftime('%Y-%m'),
                'predicted_revenue': round(base_revenue * growth_factor),
                'confidence': max(95 - (i * 5), 70),  # Decreasing confidence over time
                'deals_expected': 25 + i,
                'new_customers': 15 + (i * 2)
            })
        
        return jsonify({
            'forecast': forecast,
            'summary': {
                'total_predicted_revenue': sum(f['predicted_revenue'] for f in forecast),
                'average_monthly_growth': 8.5,
                'confidence_range': '70-95%'
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

