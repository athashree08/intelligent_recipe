import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-secret-key-change-in-production')

def hash_password(password):
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """
    Verify a password against its hash
    
    Args:
        password: Plain text password
        hashed_password: Hashed password
    
    Returns:
        Boolean indicating if password matches
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(user_id, username):
    """
    Generate JWT token for user
    
    Args:
        user_id: User ID
        username: Username
    
    Returns:
        JWT token string
    """
    payload = {
        'user_id': str(user_id),
        'username': username,
        'exp': datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    """
    Decode and verify JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """
    Decorator to protect routes with JWT authentication
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({'message': 'Success', 'user': current_user})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        # Decode token
        payload = decode_token(token)
        
        if not payload:
            return jsonify({'message': 'Token is invalid or expired'}), 401
        
        # Pass user info to route
        current_user = {
            'user_id': payload['user_id'],
            'username': payload['username']
        }
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def optional_token(f):
    """
    Decorator for routes where authentication is optional
    
    Usage:
        @app.route('/public')
        @optional_token
        def public_route(current_user):
            if current_user:
                return jsonify({'message': 'Authenticated', 'user': current_user})
            return jsonify({'message': 'Anonymous'})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
                payload = decode_token(token)
                if payload:
                    current_user = {
                        'user_id': payload['user_id'],
                        'username': payload['username']
                    }
            except:
                pass
        
        return f(current_user, *args, **kwargs)
    
    return decorated
