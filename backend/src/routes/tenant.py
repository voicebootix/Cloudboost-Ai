from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from src.models.user import db, User, Tenant, BusinessProfile

tenant_bp = Blueprint('tenant', __name__)

def require_admin():
    """Decorator to require admin role"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

@tenant_bp.route('/', methods=['GET'])
@jwt_required()
def get_tenant():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            return jsonify({'error': 'Tenant not found'}), 404
        
        return jsonify({'tenant': tenant.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tenant_bp.route('/', methods=['PUT'])
@jwt_required()
@require_admin()
def update_tenant():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            return jsonify({'error': 'Tenant not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            tenant.name = data['name']
        if 'subscription_plan' in data:
            tenant.subscription_plan = data['subscription_plan']
        
        tenant.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Tenant updated successfully',
            'tenant': tenant.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tenant_bp.route('/users', methods=['GET'])
@jwt_required()
@require_admin()
def get_tenant_users():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        users = User.query.filter_by(tenant_id=tenant_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tenant_bp.route('/users', methods=['POST'])
@jwt_required()
@require_admin()
def create_user():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(tenant_id=tenant_id, email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400
        
        # Create user
        user = User(
            tenant_id=tenant_id,
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data.get('role', 'user'),
            language_preference=data.get('language_preference', 'en'),
            timezone=data.get('timezone', 'UTC')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tenant_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
@require_admin()
def update_user(user_id):
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        user = User.query.filter_by(id=user_id, tenant_id=tenant_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'role' in data:
            user.role = data['role']
        if 'status' in data:
            user.status = data['status']
        if 'language_preference' in data:
            user.language_preference = data['language_preference']
        if 'timezone' in data:
            user.timezone = data['timezone']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tenant_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
@require_admin()
def delete_user(user_id):
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        current_user_id = get_jwt_identity()
        
        # Prevent self-deletion
        if user_id == current_user_id:
            return jsonify({'error': 'Cannot delete your own account'}), 400
        
        user = User.query.filter_by(id=user_id, tenant_id=tenant_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tenant_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_tenant_stats():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        # Get basic stats
        total_users = User.query.filter_by(tenant_id=tenant_id).count()
        active_users = User.query.filter_by(tenant_id=tenant_id, status='active').count()
        business_profiles = BusinessProfile.query.filter_by(tenant_id=tenant_id).count()
        
        # Get tenant info
        tenant = Tenant.query.get(tenant_id)
        
        stats = {
            'tenant': tenant.to_dict() if tenant else None,
            'total_users': total_users,
            'active_users': active_users,
            'business_profiles': business_profiles,
            'subscription_plan': tenant.subscription_plan if tenant else None
        }
        
        return jsonify({'stats': stats}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

