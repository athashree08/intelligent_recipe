from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import routes
from routes.auth_routes import auth_bp
from routes.image_routes import image_bp
from routes.recipe_routes import recipe_bp

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-secret-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 5 * 1024 * 1024))  # 5MB
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(image_bp, url_prefix='/api/image')
app.register_blueprint(recipe_bp, url_prefix='/api/recipes')

# Root route
@app.route('/')
def index():
    return jsonify({
        'message': 'Intelligent Recipe Generator API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'image': '/api',
            'recipes': '/api/recipes'
        }
    })

# Health check
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'message': 'File too large. Maximum size is 5MB'}), 413

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Run app
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug_mode
    )
