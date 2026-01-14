from flask import Blueprint, request, jsonify
from models.database import UserDB
from utils.auth import hash_password, verify_password, generate_token, token_required
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request body:
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }
    
    Returns:
        {
            "message": "User created successfully",
            "token": "jwt_token",
            "user": {"username": "...", "email": "..."}
        }
    """
    try:
        data = request.get_json()
        
        # Validate input
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Check if user already exists
        existing_user = UserDB.get_user_by_username(username)
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 409
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Create user
        user_data = {
            'username': username,
            'email': email,
            'password_hash': hashed_password,
            'created_at': datetime.utcnow()
        }
        
        user_id = UserDB.create_user(user_data)
        
        # Generate token
        token = generate_token(user_id, username)
        
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {
                'username': username,
                'email': email
            }
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Error creating user: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    
    Request body:
        {
            "username": "string",
            "password": "string"
        }
    
    Returns:
        {
            "message": "Login successful",
            "token": "jwt_token",
            "user": {"username": "...", "email": "..."}
        }
    """
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'message': 'Missing username or password'}), 400
        
        # Get user
        user = UserDB.get_user_by_username(username)
        
        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        # Generate token
        token = generate_token(user['_id'], username)
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'username': user['username'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error logging in: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """
    Get user profile (protected route)
    
    Returns:
        {
            "user": {"username": "...", "email": "..."}
        }
    """
    try:
        user = UserDB.get_user_by_id(current_user['user_id'])
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'username': user['username'],
                'email': user['email'],
                'created_at': user.get('created_at', '')
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching profile: {str(e)}'}), 500
