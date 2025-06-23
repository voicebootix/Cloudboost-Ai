from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
import json
from src.models.user import db, User, BusinessProfile, APIKey

business_bp = Blueprint('business', __name__)

@business_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_business_profile():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        profile = BusinessProfile.query.filter_by(tenant_id=tenant_id).first()
        
        if not profile:
            return jsonify({'profile': None}), 200
        
        return jsonify({'profile': profile.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@business_bp.route('/profile', methods=['POST'])
@jwt_required()
def create_business_profile():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Check if profile already exists
        existing_profile = BusinessProfile.query.filter_by(tenant_id=tenant_id).first()
        if existing_profile:
            return jsonify({'error': 'Business profile already exists. Use PUT to update.'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('business_name'):
            return jsonify({'error': 'Business name is required'}), 400
        
        # Create business profile
        profile = BusinessProfile(
            tenant_id=tenant_id,
            business_name=data['business_name'],
            industry=data.get('industry'),
            description=data.get('description'),
            website_url=data.get('website_url'),
            country=data.get('country'),
            city=data.get('city'),
            target_audience=data.get('target_audience'),
            brand_voice=data.get('brand_voice'),
            unique_selling_proposition=data.get('unique_selling_proposition'),
            primary_language=data.get('primary_language', 'en'),
            secondary_languages=json.dumps(data.get('secondary_languages', [])),
            logo_url=data.get('logo_url'),
            brand_colors=json.dumps(data.get('brand_colors', {}))
        )
        
        db.session.add(profile)
        db.session.commit()
        
        return jsonify({
            'message': 'Business profile created successfully',
            'profile': profile.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_business_profile():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        profile = BusinessProfile.query.filter_by(tenant_id=tenant_id).first()
        if not profile:
            return jsonify({'error': 'Business profile not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'business_name' in data:
            profile.business_name = data['business_name']
        if 'industry' in data:
            profile.industry = data['industry']
        if 'description' in data:
            profile.description = data['description']
        if 'website_url' in data:
            profile.website_url = data['website_url']
        if 'country' in data:
            profile.country = data['country']
        if 'city' in data:
            profile.city = data['city']
        if 'target_audience' in data:
            profile.target_audience = data['target_audience']
        if 'brand_voice' in data:
            profile.brand_voice = data['brand_voice']
        if 'unique_selling_proposition' in data:
            profile.unique_selling_proposition = data['unique_selling_proposition']
        if 'primary_language' in data:
            profile.primary_language = data['primary_language']
        if 'secondary_languages' in data:
            profile.secondary_languages = json.dumps(data['secondary_languages'])
        if 'logo_url' in data:
            profile.logo_url = data['logo_url']
        if 'brand_colors' in data:
            profile.brand_colors = json.dumps(data['brand_colors'])
        
        profile.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Business profile updated successfully',
            'profile': profile.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_bp.route('/api-keys', methods=['GET'])
@jwt_required()
def get_api_keys():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        api_keys = APIKey.query.filter_by(tenant_id=tenant_id).all()
        
        return jsonify({
            'api_keys': [key.to_dict() for key in api_keys]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@business_bp.route('/api-keys', methods=['POST'])
@jwt_required()
def create_api_key():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['platform', 'key_name', 'key_value']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if API key already exists for this platform
        existing_key = APIKey.query.filter_by(
            tenant_id=tenant_id,
            platform=data['platform'],
            key_name=data['key_name']
        ).first()
        
        if existing_key:
            return jsonify({'error': 'API key already exists for this platform and name'}), 400
        
        # In production, encrypt the key value
        # For now, we'll store it as-is (this should be encrypted)
        api_key = APIKey(
            tenant_id=tenant_id,
            platform=data['platform'],
            key_name=data['key_name'],
            encrypted_key=data['key_value'],  # Should be encrypted
            expires_at=datetime.fromisoformat(data['expires_at']) if data.get('expires_at') else None
        )
        
        db.session.add(api_key)
        db.session.commit()
        
        return jsonify({
            'message': 'API key created successfully',
            'api_key': api_key.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_bp.route('/api-keys/<key_id>', methods=['PUT'])
@jwt_required()
def update_api_key(key_id):
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        api_key = APIKey.query.filter_by(id=key_id, tenant_id=tenant_id).first()
        if not api_key:
            return jsonify({'error': 'API key not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'key_name' in data:
            api_key.key_name = data['key_name']
        if 'key_value' in data:
            api_key.encrypted_key = data['key_value']  # Should be encrypted
        if 'status' in data:
            api_key.status = data['status']
        if 'expires_at' in data:
            api_key.expires_at = datetime.fromisoformat(data['expires_at']) if data['expires_at'] else None
        
        api_key.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'API key updated successfully',
            'api_key': api_key.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_bp.route('/api-keys/<key_id>', methods=['DELETE'])
@jwt_required()
def delete_api_key(key_id):
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        api_key = APIKey.query.filter_by(id=key_id, tenant_id=tenant_id).first()
        if not api_key:
            return jsonify({'error': 'API key not found'}), 404
        
        db.session.delete(api_key)
        db.session.commit()
        
        return jsonify({'message': 'API key deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_bp.route('/analyze-website', methods=['POST'])
@jwt_required()
def analyze_website():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        website_url = data.get('website_url')
        
        if not website_url:
            return jsonify({'error': 'Website URL is required'}), 400
        
        # This is a placeholder for website analysis functionality
        # In production, this would scrape and analyze the website
        analysis_result = {
            'business_name': 'Extracted Business Name',
            'industry': 'Technology',
            'description': 'AI-powered business automation platform',
            'target_audience': 'Small to medium businesses in South Asia',
            'brand_voice': 'Professional, innovative, customer-focused',
            'unique_selling_proposition': 'Complete automation from content creation to sales',
            'primary_language': 'en',
            'extracted_at': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'message': 'Website analysis completed',
            'analysis': analysis_result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@business_bp.route('/competitor-analysis', methods=['POST'])
@jwt_required()
def competitor_analysis():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        industry = data.get('industry')
        location = data.get('location')
        
        if not industry:
            return jsonify({'error': 'Industry is required'}), 400
        
        # This is a placeholder for competitor analysis functionality
        # In production, this would analyze competitors in the industry
        competitors = [
            {
                'name': 'Competitor 1',
                'website': 'https://competitor1.com',
                'strengths': ['Strong social media presence', 'Good customer reviews'],
                'weaknesses': ['Limited automation features', 'High pricing'],
                'pricing': 'Premium',
                'target_audience': 'Enterprise clients'
            },
            {
                'name': 'Competitor 2',
                'website': 'https://competitor2.com',
                'strengths': ['Affordable pricing', 'Easy to use'],
                'weaknesses': ['Limited features', 'Poor customer support'],
                'pricing': 'Budget',
                'target_audience': 'Small businesses'
            }
        ]
        
        return jsonify({
            'message': 'Competitor analysis completed',
            'competitors': competitors,
            'analysis_date': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

