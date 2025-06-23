from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timedelta
import json
import uuid
import re
from src.models.user import db, User, BusinessProfile

communication_bp = Blueprint('communication', __name__)

# Communication channels supported
COMMUNICATION_CHANNELS = {
    'whatsapp': {
        'name': 'WhatsApp Business',
        'message_types': ['text', 'image', 'document', 'template', 'interactive'],
        'max_message_length': 4096,
        'supports_media': True
    },
    'email': {
        'name': 'Email',
        'message_types': ['html', 'text', 'template'],
        'max_message_length': 100000,
        'supports_media': True
    },
    'sms': {
        'name': 'SMS',
        'message_types': ['text'],
        'max_message_length': 160,
        'supports_media': False
    },
    'voice': {
        'name': 'Voice Call',
        'message_types': ['voice_message', 'ivr'],
        'max_message_length': 300,  # seconds
        'supports_media': False
    }
}

# South Asian telecom providers
TELECOM_PROVIDERS = {
    'LK': ['Dialog', 'Mobitel', 'Hutch', 'Airtel'],
    'IN': ['Jio', 'Airtel', 'Vi', 'BSNL'],
    'PK': ['Jazz', 'Telenor', 'Zong', 'Ufone'],
    'BD': ['Grameenphone', 'Robi', 'Banglalink', 'Teletalk'],
    'NP': ['Ncell', 'NTC'],
    'MM': ['MPT', 'Ooredoo', 'Telenor']
}

# Message status types
MESSAGE_STATUS = {
    'queued': 'Queued',
    'sent': 'Sent',
    'delivered': 'Delivered',
    'read': 'Read',
    'failed': 'Failed',
    'cancelled': 'Cancelled'
}

def validate_phone_number(phone_number, country_code=None):
    """Validate phone number format for South Asian countries"""
    # Remove all non-digit characters
    clean_number = re.sub(r'[^\d+]', '', phone_number)
    
    # Basic validation patterns for South Asian countries
    patterns = {
        'LK': r'^\+94[0-9]{9}$',  # Sri Lanka
        'IN': r'^\+91[0-9]{10}$',  # India
        'PK': r'^\+92[0-9]{10}$',  # Pakistan
        'BD': r'^\+880[0-9]{10}$',  # Bangladesh
        'NP': r'^\+977[0-9]{10}$',  # Nepal
        'MM': r'^\+95[0-9]{8,10}$'  # Myanmar
    }
    
    if country_code and country_code in patterns:
        return bool(re.match(patterns[country_code], clean_number))
    
    # General validation if no specific country code
    return bool(re.match(r'^\+[1-9]\d{1,14}$', clean_number))

def validate_email(email):
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def simulate_message_delivery(channel, recipient, message_content):
    """Simulate message delivery across different channels"""
    
    # Simulate delivery success/failure rates based on channel
    success_rates = {
        'whatsapp': 0.95,
        'email': 0.92,
        'sms': 0.98,
        'voice': 0.85
    }
    
    import random
    is_successful = random.random() < success_rates.get(channel, 0.9)
    
    if is_successful:
        return {
            'success': True,
            'message_id': f"{channel}_{uuid.uuid4().hex[:12]}",
            'status': 'sent',
            'delivered_at': datetime.utcnow().isoformat(),
            'cost': calculate_message_cost(channel, recipient, message_content)
        }
    else:
        return {
            'success': False,
            'error': f"Failed to deliver via {channel}",
            'status': 'failed'
        }

def calculate_message_cost(channel, recipient, message_content):
    """Calculate message cost based on channel and destination"""
    
    # Simulated cost structure (in USD)
    base_costs = {
        'whatsapp': 0.005,  # Per message
        'email': 0.001,     # Per email
        'sms': 0.02,        # Per SMS
        'voice': 0.05       # Per minute
    }
    
    # Regional multipliers for South Asian countries
    country_multipliers = {
        'LK': 1.0,   # Sri Lanka (base)
        'IN': 0.8,   # India (lower cost)
        'PK': 0.9,   # Pakistan
        'BD': 0.85,  # Bangladesh
        'NP': 1.1,   # Nepal
        'MM': 1.2    # Myanmar
    }
    
    base_cost = base_costs.get(channel, 0.01)
    
    # Extract country code from recipient (simplified)
    country_code = 'LK'  # Default to Sri Lanka
    if recipient.startswith('+91'):
        country_code = 'IN'
    elif recipient.startswith('+92'):
        country_code = 'PK'
    elif recipient.startswith('+880'):
        country_code = 'BD'
    elif recipient.startswith('+977'):
        country_code = 'NP'
    elif recipient.startswith('+95'):
        country_code = 'MM'
    
    multiplier = country_multipliers.get(country_code, 1.0)
    
    # Calculate final cost
    if channel == 'sms' and len(message_content) > 160:
        # Multi-part SMS
        parts = (len(message_content) + 159) // 160
        return round(base_cost * multiplier * parts, 4)
    elif channel == 'voice':
        # Voice cost per minute (assume 1 minute for simulation)
        return round(base_cost * multiplier, 4)
    else:
        return round(base_cost * multiplier, 4)

@communication_bp.route('/channels', methods=['GET'])
@jwt_required()
def get_channels():
    try:
        return jsonify({
            'channels': COMMUNICATION_CHANNELS,
            'telecom_providers': TELECOM_PROVIDERS
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/send-message', methods=['POST'])
@jwt_required()
def send_message():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['channel', 'recipient', 'message_content']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        channel = data['channel']
        recipient = data['recipient']
        message_content = data['message_content']
        message_type = data.get('message_type', 'text')
        scheduled_time = data.get('scheduled_time')
        
        # Validate channel
        if channel not in COMMUNICATION_CHANNELS:
            return jsonify({'error': 'Invalid communication channel'}), 400
        
        # Validate recipient based on channel
        if channel in ['whatsapp', 'sms', 'voice']:
            if not validate_phone_number(recipient):
                return jsonify({'error': 'Invalid phone number format'}), 400
        elif channel == 'email':
            if not validate_email(recipient):
                return jsonify({'error': 'Invalid email address format'}), 400
        
        # Validate message length
        max_length = COMMUNICATION_CHANNELS[channel]['max_message_length']
        if len(message_content) > max_length:
            return jsonify({'error': f'Message too long. Maximum {max_length} characters for {channel}'}), 400
        
        # Create message record
        message_record = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'channel': channel,
            'recipient': recipient,
            'message_content': message_content,
            'message_type': message_type,
            'scheduled_time': scheduled_time,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'queued'
        }
        
        # If immediate sending (no scheduled time)
        if not scheduled_time:
            delivery_result = simulate_message_delivery(channel, recipient, message_content)
            
            if delivery_result['success']:
                message_record.update({
                    'status': delivery_result['status'],
                    'message_id': delivery_result['message_id'],
                    'delivered_at': delivery_result['delivered_at'],
                    'cost': delivery_result['cost']
                })
            else:
                message_record.update({
                    'status': 'failed',
                    'error': delivery_result['error']
                })
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully' if not scheduled_time else 'Message scheduled successfully',
            'message_record': message_record
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/bulk-send', methods=['POST'])
@jwt_required()
def bulk_send_messages():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('messages') or not isinstance(data['messages'], list):
            return jsonify({'error': 'messages array is required'}), 400
        
        sent_messages = []
        failed_messages = []
        
        for msg_data in data['messages']:
            try:
                # Validate individual message
                required_fields = ['channel', 'recipient', 'message_content']
                for field in required_fields:
                    if not msg_data.get(field):
                        raise ValueError(f'{field} is required')
                
                channel = msg_data['channel']
                recipient = msg_data['recipient']
                message_content = msg_data['message_content']
                
                # Validate channel
                if channel not in COMMUNICATION_CHANNELS:
                    raise ValueError('Invalid communication channel')
                
                # Validate recipient
                if channel in ['whatsapp', 'sms', 'voice']:
                    if not validate_phone_number(recipient):
                        raise ValueError('Invalid phone number format')
                elif channel == 'email':
                    if not validate_email(recipient):
                        raise ValueError('Invalid email address format')
                
                # Create and send message
                message_record = {
                    'id': str(uuid.uuid4()),
                    'tenant_id': tenant_id,
                    'channel': channel,
                    'recipient': recipient,
                    'message_content': message_content,
                    'created_at': datetime.utcnow().isoformat()
                }
                
                delivery_result = simulate_message_delivery(channel, recipient, message_content)
                
                if delivery_result['success']:
                    message_record.update({
                        'status': delivery_result['status'],
                        'message_id': delivery_result['message_id'],
                        'delivered_at': delivery_result['delivered_at'],
                        'cost': delivery_result['cost']
                    })
                    sent_messages.append(message_record)
                else:
                    message_record.update({
                        'status': 'failed',
                        'error': delivery_result['error']
                    })
                    failed_messages.append(message_record)
                
            except Exception as e:
                failed_messages.append({
                    'recipient': msg_data.get('recipient', 'Unknown'),
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'sent_messages': sent_messages,
            'failed_messages': failed_messages,
            'total_sent': len(sent_messages),
            'total_failed': len(failed_messages),
            'total_cost': sum(msg.get('cost', 0) for msg in sent_messages)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/whatsapp/templates', methods=['GET'])
@jwt_required()
def get_whatsapp_templates():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Simulate WhatsApp message templates
        templates = [
            {
                'id': 'welcome_message',
                'name': 'Welcome Message',
                'category': 'UTILITY',
                'language': 'en',
                'status': 'APPROVED',
                'content': 'Welcome to {{business_name}}! We\'re excited to serve you. Reply STOP to opt out.',
                'components': [
                    {
                        'type': 'BODY',
                        'text': 'Welcome to {{1}}! We\'re excited to serve you. Reply STOP to opt out.'
                    }
                ]
            },
            {
                'id': 'order_confirmation',
                'name': 'Order Confirmation',
                'category': 'UTILITY',
                'language': 'en',
                'status': 'APPROVED',
                'content': 'Your order #{{order_id}} has been confirmed. Total: {{amount}}. Expected delivery: {{delivery_date}}.',
                'components': [
                    {
                        'type': 'BODY',
                        'text': 'Your order #{{1}} has been confirmed. Total: {{2}}. Expected delivery: {{3}}.'
                    }
                ]
            },
            {
                'id': 'appointment_reminder',
                'name': 'Appointment Reminder',
                'category': 'UTILITY',
                'language': 'en',
                'status': 'APPROVED',
                'content': 'Reminder: You have an appointment with {{business_name}} on {{date}} at {{time}}. Reply CONFIRM to confirm.',
                'components': [
                    {
                        'type': 'BODY',
                        'text': 'Reminder: You have an appointment with {{1}} on {{2}} at {{3}}. Reply CONFIRM to confirm.'
                    }
                ]
            }
        ]
        
        return jsonify({
            'templates': templates
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/whatsapp/send-template', methods=['POST'])
@jwt_required()
def send_whatsapp_template():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['recipient', 'template_id', 'parameters']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        recipient = data['recipient']
        template_id = data['template_id']
        parameters = data['parameters']
        
        # Validate phone number
        if not validate_phone_number(recipient):
            return jsonify({'error': 'Invalid phone number format'}), 400
        
        # Simulate template message sending
        delivery_result = simulate_message_delivery('whatsapp', recipient, f"Template: {template_id}")
        
        message_record = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'channel': 'whatsapp',
            'recipient': recipient,
            'template_id': template_id,
            'parameters': parameters,
            'created_at': datetime.utcnow().isoformat()
        }
        
        if delivery_result['success']:
            message_record.update({
                'status': delivery_result['status'],
                'message_id': delivery_result['message_id'],
                'delivered_at': delivery_result['delivered_at'],
                'cost': delivery_result['cost']
            })
        else:
            message_record.update({
                'status': 'failed',
                'error': delivery_result['error']
            })
        
        return jsonify({
            'success': delivery_result['success'],
            'message': 'WhatsApp template sent successfully' if delivery_result['success'] else 'Failed to send template',
            'message_record': message_record
        }), 201 if delivery_result['success'] else 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/email/send', methods=['POST'])
@jwt_required()
def send_email():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['recipient', 'subject', 'content']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        recipient = data['recipient']
        subject = data['subject']
        content = data['content']
        content_type = data.get('content_type', 'html')
        attachments = data.get('attachments', [])
        
        # Validate email address
        if not validate_email(recipient):
            return jsonify({'error': 'Invalid email address format'}), 400
        
        # Simulate email sending
        delivery_result = simulate_message_delivery('email', recipient, content)
        
        email_record = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'channel': 'email',
            'recipient': recipient,
            'subject': subject,
            'content': content,
            'content_type': content_type,
            'attachments': attachments,
            'created_at': datetime.utcnow().isoformat()
        }
        
        if delivery_result['success']:
            email_record.update({
                'status': delivery_result['status'],
                'message_id': delivery_result['message_id'],
                'delivered_at': delivery_result['delivered_at'],
                'cost': delivery_result['cost']
            })
        else:
            email_record.update({
                'status': 'failed',
                'error': delivery_result['error']
            })
        
        return jsonify({
            'success': delivery_result['success'],
            'message': 'Email sent successfully' if delivery_result['success'] else 'Failed to send email',
            'email_record': email_record
        }), 201 if delivery_result['success'] else 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/voice/call', methods=['POST'])
@jwt_required()
def make_voice_call():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['recipient', 'message_content']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        recipient = data['recipient']
        message_content = data['message_content']
        voice_type = data.get('voice_type', 'text_to_speech')
        language = data.get('language', 'en')
        
        # Validate phone number
        if not validate_phone_number(recipient):
            return jsonify({'error': 'Invalid phone number format'}), 400
        
        # Simulate voice call
        delivery_result = simulate_message_delivery('voice', recipient, message_content)
        
        call_record = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'channel': 'voice',
            'recipient': recipient,
            'message_content': message_content,
            'voice_type': voice_type,
            'language': language,
            'created_at': datetime.utcnow().isoformat()
        }
        
        if delivery_result['success']:
            call_record.update({
                'status': delivery_result['status'],
                'call_id': delivery_result['message_id'],
                'call_duration': 45,  # Simulated duration in seconds
                'answered': True,
                'cost': delivery_result['cost']
            })
        else:
            call_record.update({
                'status': 'failed',
                'answered': False,
                'error': delivery_result['error']
            })
        
        return jsonify({
            'success': delivery_result['success'],
            'message': 'Voice call initiated successfully' if delivery_result['success'] else 'Failed to initiate call',
            'call_record': call_record
        }), 201 if delivery_result['success'] else 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/messages', methods=['GET'])
@jwt_required()
def get_messages():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        channel = request.args.get('channel')
        status = request.args.get('status')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Simulate message history
        messages = []
        for i in range(per_page):
            message = {
                'id': str(uuid.uuid4()),
                'tenant_id': tenant_id,
                'channel': channel or 'whatsapp',
                'recipient': f'+94771234{567 + i}',
                'message_content': f'Sample message content {i+1}',
                'status': status or 'delivered',
                'created_at': (datetime.utcnow() - timedelta(hours=i)).isoformat(),
                'delivered_at': (datetime.utcnow() - timedelta(hours=i, minutes=2)).isoformat(),
                'cost': 0.005
            }
            messages.append(message)
        
        return jsonify({
            'messages': messages,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': 500,  # Simulated total
                'pages': 25
            },
            'filters': {
                'channel': channel,
                'status': status,
                'date_from': date_from,
                'date_to': date_to
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_communication_analytics():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Query parameters
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        channel = request.args.get('channel')
        
        # Simulate analytics data
        analytics = {
            'overview': {
                'total_messages': 1250,
                'delivered_messages': 1187,
                'failed_messages': 63,
                'delivery_rate': 94.96,
                'total_cost': 15.75,
                'average_cost_per_message': 0.0126
            },
            'channel_breakdown': {
                'whatsapp': {
                    'messages': 650,
                    'delivered': 618,
                    'delivery_rate': 95.08,
                    'cost': 3.25
                },
                'email': {
                    'messages': 400,
                    'delivered': 372,
                    'delivery_rate': 93.0,
                    'cost': 0.40
                },
                'sms': {
                    'messages': 150,
                    'delivered': 147,
                    'delivery_rate': 98.0,
                    'cost': 3.00
                },
                'voice': {
                    'messages': 50,
                    'delivered': 50,
                    'delivery_rate': 100.0,
                    'cost': 9.10
                }
            },
            'daily_trends': [
                {'date': '2025-06-15', 'messages': 45, 'delivered': 43},
                {'date': '2025-06-16', 'messages': 67, 'delivered': 64},
                {'date': '2025-06-17', 'messages': 89, 'delivered': 85},
                {'date': '2025-06-18', 'messages': 76, 'delivered': 72},
                {'date': '2025-06-19', 'messages': 92, 'delivered': 88},
                {'date': '2025-06-20', 'messages': 108, 'delivered': 103},
                {'date': '2025-06-21', 'messages': 134, 'delivered': 128}
            ],
            'regional_performance': {
                'LK': {'messages': 450, 'delivery_rate': 96.2},
                'IN': {'messages': 380, 'delivery_rate': 94.5},
                'PK': {'messages': 220, 'delivery_rate': 93.8},
                'BD': {'messages': 150, 'delivery_rate': 95.1},
                'NP': {'messages': 50, 'delivery_rate': 92.0}
            }
        }
        
        return jsonify({
            'analytics': analytics,
            'date_range': {
                'from': date_from or '2025-06-15',
                'to': date_to or '2025-06-22'
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/campaigns', methods=['POST'])
@jwt_required()
def create_campaign():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'channel', 'message_content', 'recipients']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        name = data['name']
        channel = data['channel']
        message_content = data['message_content']
        recipients = data['recipients']
        scheduled_time = data.get('scheduled_time')
        
        # Validate channel
        if channel not in COMMUNICATION_CHANNELS:
            return jsonify({'error': 'Invalid communication channel'}), 400
        
        # Validate recipients
        if not isinstance(recipients, list) or len(recipients) == 0:
            return jsonify({'error': 'Recipients must be a non-empty array'}), 400
        
        # Create campaign
        campaign = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'name': name,
            'channel': channel,
            'message_content': message_content,
            'recipients': recipients,
            'scheduled_time': scheduled_time,
            'status': 'scheduled' if scheduled_time else 'active',
            'created_at': datetime.utcnow().isoformat(),
            'total_recipients': len(recipients),
            'estimated_cost': len(recipients) * calculate_message_cost(channel, recipients[0] if recipients else '+94771234567', message_content)
        }
        
        return jsonify({
            'success': True,
            'message': 'Campaign created successfully',
            'campaign': campaign
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

