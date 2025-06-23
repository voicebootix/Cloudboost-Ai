from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timedelta
import json
import uuid
from src.models.user import db, User, BusinessProfile

social_bp = Blueprint('social', __name__)

# Supported social media platforms
SOCIAL_PLATFORMS = {
    'facebook': {
        'name': 'Facebook',
        'api_version': 'v18.0',
        'post_types': ['text', 'image', 'video', 'link', 'carousel'],
        'max_text_length': 2200,
        'hashtag_limit': 30
    },
    'instagram': {
        'name': 'Instagram',
        'api_version': 'v18.0',
        'post_types': ['image', 'video', 'carousel', 'story', 'reel'],
        'max_text_length': 2200,
        'hashtag_limit': 30
    },
    'linkedin': {
        'name': 'LinkedIn',
        'api_version': 'v2',
        'post_types': ['text', 'image', 'video', 'article', 'document'],
        'max_text_length': 3000,
        'hashtag_limit': 10
    },
    'twitter': {
        'name': 'Twitter/X',
        'api_version': 'v2',
        'post_types': ['text', 'image', 'video', 'thread'],
        'max_text_length': 280,
        'hashtag_limit': 10
    },
    'tiktok': {
        'name': 'TikTok',
        'api_version': 'v1',
        'post_types': ['video'],
        'max_text_length': 150,
        'hashtag_limit': 20
    },
    'youtube': {
        'name': 'YouTube',
        'api_version': 'v3',
        'post_types': ['video', 'short', 'live'],
        'max_text_length': 5000,
        'hashtag_limit': 15
    },
    'pinterest': {
        'name': 'Pinterest',
        'api_version': 'v5',
        'post_types': ['pin', 'story'],
        'max_text_length': 500,
        'hashtag_limit': 20
    }
}

# Content scheduling status
SCHEDULE_STATUS = {
    'draft': 'Draft',
    'scheduled': 'Scheduled',
    'published': 'Published',
    'failed': 'Failed',
    'cancelled': 'Cancelled'
}

def simulate_platform_api_call(platform, action, data):
    """
    Simulate API calls to social media platforms
    In production, this would make actual API calls to each platform
    """
    
    # Simulate different response scenarios
    if platform == 'facebook':
        if action == 'post':
            return {
                'success': True,
                'post_id': f"fb_{uuid.uuid4().hex[:10]}",
                'url': f"https://facebook.com/posts/{uuid.uuid4().hex[:10]}",
                'platform': 'facebook'
            }
        elif action == 'get_insights':
            return {
                'success': True,
                'insights': {
                    'reach': 1250,
                    'impressions': 2100,
                    'engagement': 89,
                    'clicks': 45,
                    'shares': 12
                }
            }
    
    elif platform == 'instagram':
        if action == 'post':
            return {
                'success': True,
                'post_id': f"ig_{uuid.uuid4().hex[:10]}",
                'url': f"https://instagram.com/p/{uuid.uuid4().hex[:10]}",
                'platform': 'instagram'
            }
        elif action == 'get_insights':
            return {
                'success': True,
                'insights': {
                    'reach': 980,
                    'impressions': 1650,
                    'engagement': 156,
                    'likes': 134,
                    'comments': 22
                }
            }
    
    elif platform == 'linkedin':
        if action == 'post':
            return {
                'success': True,
                'post_id': f"li_{uuid.uuid4().hex[:10]}",
                'url': f"https://linkedin.com/posts/{uuid.uuid4().hex[:10]}",
                'platform': 'linkedin'
            }
        elif action == 'get_insights':
            return {
                'success': True,
                'insights': {
                    'impressions': 850,
                    'clicks': 67,
                    'engagement': 45,
                    'shares': 8,
                    'comments': 15
                }
            }
    
    # Default response for other platforms
    return {
        'success': True,
        'post_id': f"{platform}_{uuid.uuid4().hex[:10]}",
        'url': f"https://{platform}.com/posts/{uuid.uuid4().hex[:10]}",
        'platform': platform
    }

@social_bp.route('/platforms', methods=['GET'])
@jwt_required()
def get_platforms():
    try:
        return jsonify({
            'platforms': SOCIAL_PLATFORMS
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/connect', methods=['POST'])
@jwt_required()
def connect_platform():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['platform', 'access_token']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        platform = data['platform']
        access_token = data['access_token']
        
        # Validate platform
        if platform not in SOCIAL_PLATFORMS:
            return jsonify({'error': 'Platform not supported'}), 400
        
        # In production, validate the access token with the platform API
        # For now, we'll simulate successful connection
        
        # Store platform connection (in production, encrypt the token)
        connection_record = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'platform': platform,
            'access_token': access_token,  # Should be encrypted
            'connected_at': datetime.utcnow().isoformat(),
            'status': 'active',
            'account_info': {
                'account_id': f"{platform}_account_{uuid.uuid4().hex[:8]}",
                'account_name': f"Business Account on {SOCIAL_PLATFORMS[platform]['name']}",
                'followers': 1250,  # Simulated data
                'verified': False
            }
        }
        
        return jsonify({
            'success': True,
            'message': f'{SOCIAL_PLATFORMS[platform]["name"]} connected successfully',
            'connection': {
                'id': connection_record['id'],
                'platform': platform,
                'status': connection_record['status'],
                'connected_at': connection_record['connected_at'],
                'account_info': connection_record['account_info']
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/post', methods=['POST'])
@jwt_required()
def create_post():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['platforms', 'content', 'post_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        platforms = data['platforms']
        content = data['content']
        post_type = data['post_type']
        media_urls = data.get('media_urls', [])
        scheduled_time = data.get('scheduled_time')
        
        # Validate platforms
        for platform in platforms:
            if platform not in SOCIAL_PLATFORMS:
                return jsonify({'error': f'Platform {platform} not supported'}), 400
        
        # Create post record
        post_record = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'content': content,
            'post_type': post_type,
            'platforms': platforms,
            'media_urls': media_urls,
            'scheduled_time': scheduled_time,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'scheduled' if scheduled_time else 'published',
            'platform_posts': []
        }
        
        # If immediate posting (no scheduled time)
        if not scheduled_time:
            for platform in platforms:
                # Optimize content for each platform
                optimized_content = optimize_content_for_platform(content, platform)
                
                # Simulate API call to platform
                api_response = simulate_platform_api_call(platform, 'post', {
                    'content': optimized_content,
                    'media_urls': media_urls,
                    'post_type': post_type
                })
                
                if api_response['success']:
                    post_record['platform_posts'].append({
                        'platform': platform,
                        'platform_post_id': api_response['post_id'],
                        'url': api_response['url'],
                        'status': 'published',
                        'published_at': datetime.utcnow().isoformat()
                    })
                else:
                    post_record['platform_posts'].append({
                        'platform': platform,
                        'status': 'failed',
                        'error': api_response.get('error', 'Unknown error')
                    })
        
        return jsonify({
            'success': True,
            'message': 'Post created successfully',
            'post': post_record
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def optimize_content_for_platform(content, platform):
    """Optimize content for specific platform requirements"""
    platform_info = SOCIAL_PLATFORMS.get(platform, {})
    max_length = platform_info.get('max_text_length', 1000)
    
    # Truncate if too long
    if len(content) > max_length:
        content = content[:max_length-3] + "..."
    
    # Platform-specific optimizations
    if platform == 'twitter':
        # Add thread indicator if content is long
        if len(content) > 200:
            content += " 🧵"
    elif platform == 'linkedin':
        # Add professional tone
        if not content.startswith(('Excited', 'Pleased', 'Proud')):
            content = f"Excited to share: {content}"
    elif platform == 'instagram':
        # Ensure hashtags are included
        if '#' not in content:
            content += " #business #southasia #cloudboostai"
    
    return content

@social_bp.route('/schedule', methods=['POST'])
@jwt_required()
def schedule_post():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['platforms', 'content', 'scheduled_time']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        platforms = data['platforms']
        content = data['content']
        scheduled_time = data['scheduled_time']
        
        # Parse scheduled time
        try:
            schedule_dt = datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid scheduled_time format'}), 400
        
        # Validate future time
        if schedule_dt <= datetime.utcnow():
            return jsonify({'error': 'Scheduled time must be in the future'}), 400
        
        # Create scheduled post
        scheduled_post = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'content': content,
            'platforms': platforms,
            'scheduled_time': scheduled_time,
            'status': 'scheduled',
            'created_at': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'success': True,
            'message': 'Post scheduled successfully',
            'scheduled_post': scheduled_post
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        platform = request.args.get('platform')
        
        # Simulate post data (in production, query from database)
        posts = []
        for i in range(per_page):
            post = {
                'id': str(uuid.uuid4()),
                'tenant_id': tenant_id,
                'content': f"Sample post content {i+1}",
                'platforms': ['facebook', 'instagram'],
                'status': 'published',
                'created_at': (datetime.utcnow() - timedelta(days=i)).isoformat(),
                'engagement': {
                    'likes': 45 + i*5,
                    'comments': 8 + i*2,
                    'shares': 3 + i
                }
            }
            posts.append(post)
        
        return jsonify({
            'posts': posts,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': 100,  # Simulated total
                'pages': 10
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Query parameters
        platform = request.args.get('platform')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Simulate analytics data
        analytics = {
            'overview': {
                'total_posts': 45,
                'total_reach': 15750,
                'total_engagement': 892,
                'engagement_rate': 5.67,
                'follower_growth': 127
            },
            'platform_breakdown': {
                'facebook': {
                    'posts': 18,
                    'reach': 8500,
                    'engagement': 456,
                    'engagement_rate': 5.36
                },
                'instagram': {
                    'posts': 15,
                    'reach': 4200,
                    'engagement': 298,
                    'engagement_rate': 7.09
                },
                'linkedin': {
                    'posts': 12,
                    'reach': 3050,
                    'engagement': 138,
                    'engagement_rate': 4.52
                }
            },
            'top_performing_posts': [
                {
                    'id': str(uuid.uuid4()),
                    'content': 'Exciting news about our latest AI features...',
                    'platform': 'instagram',
                    'engagement': 156,
                    'reach': 2100
                },
                {
                    'id': str(uuid.uuid4()),
                    'content': 'How CloudBoost AI is transforming South Asian businesses...',
                    'platform': 'linkedin',
                    'engagement': 89,
                    'reach': 1850
                }
            ],
            'engagement_trends': [
                {'date': '2025-06-15', 'engagement': 45},
                {'date': '2025-06-16', 'engagement': 67},
                {'date': '2025-06-17', 'engagement': 89},
                {'date': '2025-06-18', 'engagement': 76},
                {'date': '2025-06-19', 'engagement': 92},
                {'date': '2025-06-20', 'engagement': 108},
                {'date': '2025-06-21', 'engagement': 134}
            ]
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

@social_bp.route('/content-calendar', methods=['GET'])
@jwt_required()
def get_content_calendar():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Query parameters
        month = request.args.get('month', datetime.utcnow().month, type=int)
        year = request.args.get('year', datetime.utcnow().year, type=int)
        
        # Simulate calendar data
        calendar_events = []
        for day in range(1, 31):
            if day % 3 == 0:  # Simulate posts every 3 days
                event = {
                    'date': f"{year}-{month:02d}-{day:02d}",
                    'posts': [
                        {
                            'id': str(uuid.uuid4()),
                            'content': f"Scheduled post for {day}/{month}",
                            'platforms': ['facebook', 'instagram'],
                            'time': '10:00',
                            'status': 'scheduled'
                        }
                    ]
                }
                calendar_events.append(event)
        
        return jsonify({
            'calendar': calendar_events,
            'month': month,
            'year': year
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/bulk-schedule', methods=['POST'])
@jwt_required()
def bulk_schedule_posts():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('posts') or not isinstance(data['posts'], list):
            return jsonify({'error': 'posts array is required'}), 400
        
        scheduled_posts = []
        failed_posts = []
        
        for post_data in data['posts']:
            try:
                # Validate individual post
                required_fields = ['content', 'platforms', 'scheduled_time']
                for field in required_fields:
                    if not post_data.get(field):
                        raise ValueError(f'{field} is required')
                
                # Create scheduled post
                scheduled_post = {
                    'id': str(uuid.uuid4()),
                    'tenant_id': tenant_id,
                    'content': post_data['content'],
                    'platforms': post_data['platforms'],
                    'scheduled_time': post_data['scheduled_time'],
                    'status': 'scheduled',
                    'created_at': datetime.utcnow().isoformat()
                }
                
                scheduled_posts.append(scheduled_post)
                
            except Exception as e:
                failed_posts.append({
                    'content': post_data.get('content', 'Unknown'),
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'scheduled_posts': scheduled_posts,
            'failed_posts': failed_posts,
            'total_scheduled': len(scheduled_posts),
            'total_failed': len(failed_posts)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/disconnect/<platform>', methods=['DELETE'])
@jwt_required()
def disconnect_platform(platform):
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Validate platform
        if platform not in SOCIAL_PLATFORMS:
            return jsonify({'error': 'Platform not supported'}), 400
        
        # In production, remove stored credentials and revoke access tokens
        
        return jsonify({
            'success': True,
            'message': f'{SOCIAL_PLATFORMS[platform]["name"]} disconnected successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

