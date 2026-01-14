from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from utils.image_preprocessing import prepare_image_tensor
from utils.ocr_processor import process_packaged_food_image
from models.ingredient_recognition import predict_ingredients

image_bp = Blueprint('image', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    """
    Upload an image file
    
    Form data:
        image: File
    
    Returns:
        {
            "message": "Image uploaded successfully",
            "filename": "..."
        }
    """
    try:
        if 'image' not in request.files:
            return jsonify({'message': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'message': 'Invalid file type. Use JPG, JPEG, or PNG'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        return jsonify({
            'message': 'Image uploaded successfully',
            'filename': filename
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error uploading image: {str(e)}'}), 500

@image_bp.route('/recognize', methods=['POST'])
def recognize_ingredients():
    """
    Recognize ingredients from uploaded image
    - First tries OCR for packaged food labels
    - Falls back to ML model for fresh ingredients
    
    Form data:
        image: File
    
    Returns:
        {
            "ingredients": [
                {"name": "tomato", "confidence": 0.95},
                ...
            ],
            "method": "ocr" | "ml_model"
        }
    """
    try:
        if 'image' not in request.files:
            return jsonify({'message': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'message': 'Invalid file type'}), 400
        
        # Try OCR first (for packaged food labels)
        try:
            print("=" * 50)
            print("Attempting OCR extraction...")
            file.seek(0)  # Reset file pointer
            ocr_result = process_packaged_food_image(file)
            
            print(f"OCR raw text: {ocr_result.get('raw_text', '')[:200]}")
            print(f"OCR cleaned text: {ocr_result.get('cleaned_text', '')[:200]}")
            print(f"OCR ingredients: {ocr_result.get('ingredients', [])}")
            
            # If OCR found ingredients, use them
            if ocr_result['ingredients'] and len(ocr_result['ingredients']) >= 2:
                print(f"✓ OCR SUCCESS: Found {len(ocr_result['ingredients'])} ingredients")
                ingredients = [{'name': ing, 'confidence': 0.90} for ing in ocr_result['ingredients']]
                
                return jsonify({
                    'ingredients': ingredients,
                    'method': 'ocr',
                    'raw_text': ocr_result.get('raw_text', ''),
                    'message': f'Detected {len(ingredients)} ingredients using OCR'
                }), 200
            else:
                print(f"✗ OCR found only {len(ocr_result.get('ingredients', []))} ingredients, trying ML model...")
        
        except Exception as ocr_error:
            import traceback
            print(f"✗ OCR FAILED with error: {ocr_error}")
            print(f"Traceback: {traceback.format_exc()}")
            print("Trying ML model...")
            print("=" * 50)
        
        # If OCR didn't work or found few ingredients, try ML model (for fresh ingredients)
        try:
            file.seek(0)  # Reset file pointer
            image_tensor = prepare_image_tensor(file)
            file.seek(0)
            
            predictions = predict_ingredients(image_tensor, top_k=5)
            
            return jsonify({
                'ingredients': predictions,
                'method': 'ml_model',
                'message': 'Ingredients recognized using ML model'
            }), 200
            
        except Exception as model_error:
            # If both OCR and model fail, return placeholder
            print(f"Model error: {model_error}")
            return jsonify({
                'ingredients': [
                    {'name': 'tomato', 'confidence': 0.85},
                    {'name': 'onion', 'confidence': 0.75},
                    {'name': 'garlic', 'confidence': 0.65}
                ],
                'method': 'placeholder',
                'message': 'Using placeholder data (OCR and model unavailable)'
            }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error recognizing ingredients: {str(e)}'}), 500

@image_bp.route('/recognize-dish', methods=['POST'])
def recognize_dish():
    """
    Recognize a dish from an image and find similar recipes
    
    Form data:
        image: File
    
    Returns:
        {
            "dish_name": "pasta carbonara",
            "confidence": 0.85,
            "similar_recipes": [...]
        }
    """
    try:
        if 'image' not in request.files:
            return jsonify({'message': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'message': 'Invalid file type'}), 400
        
        # Save the file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Use dish recognition utility
        try:
            from models.database import RecipeDB
            from utils.dish_recognition import recognize_dish_from_image, get_dish_ingredients
            
            # Recognize the dish from the image
            dish_result = recognize_dish_from_image(filepath)
            detected_dish = dish_result['dish_name']
            confidence = dish_result['confidence']
            common_ingredients = dish_result.get('common_ingredients', [])
            
            # Search for similar recipes in our database
            all_recipes = RecipeDB.get_all_recipes()
            
            # Filter recipes that match the detected dish
            similar_recipes = []
            search_terms = [detected_dish]
            
            # Add variations of the dish name
            if ' ' in detected_dish:
                search_terms.extend(detected_dish.split())
            
            for recipe in all_recipes:
                recipe_name = recipe.get('name', '').lower()
                recipe_category = recipe.get('category', '').lower()
                
                # Check if any search term matches recipe name or category
                for term in search_terms:
                    if term.lower() in recipe_name or term.lower() in recipe_category:
                        recipe['_id'] = str(recipe['_id'])
                        if recipe not in similar_recipes:
                            similar_recipes.append(recipe)
                        break
            
            # If no exact matches, search by common ingredients
            if len(similar_recipes) < 5:
                # Use recommendation engine with common ingredients
                from utils.recommendation_engine import get_recommendations
                recommended = get_recommendations(
                    common_ingredients,
                    all_recipes,
                    method='hybrid',
                    top_n=15
                )
                
                for recipe in recommended:
                    recipe['_id'] = str(recipe['_id'])
                    if recipe not in similar_recipes:
                        similar_recipes.append(recipe)
            
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
            
            return jsonify({
                'dish_name': detected_dish,
                'confidence': confidence,
                'category': dish_result.get('category', 'Unknown'),
                'similar_recipes': similar_recipes[:12],
                'count': len(similar_recipes[:12]),
                'message': f'Found recipes similar to {detected_dish}'
            }), 200
            
        except Exception as model_error:
            print(f"Dish recognition error: {model_error}")
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # Fallback to general recommendations
            from models.database import RecipeDB
            all_recipes = RecipeDB.get_all_recipes()
            
            # Return random selection
            import random
            random_recipes = random.sample(all_recipes, min(10, len(all_recipes)))
            for recipe in random_recipes:
                recipe['_id'] = str(recipe['_id'])
            
            return jsonify({
                'dish_name': 'various dishes',
                'confidence': 0.50,
                'similar_recipes': random_recipes,
                'count': len(random_recipes),
                'message': 'Showing popular recipes (dish recognition unavailable)'
            }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error recognizing dish: {str(e)}'}), 500

@image_bp.route('/ocr', methods=['POST'])
def ocr_extract():
    """
    Extract ingredients from packaged food label using OCR
    
    Form data:
        image: File
    
    Returns:
        {
            "ingredients": ["flour", "sugar", "eggs", ...],
            "raw_text": "...",
            "cleaned_text": "..."
        }
    """
    try:
        if 'image' not in request.files:
            return jsonify({'message': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'message': 'Invalid file type'}), 400
        
        # Process with OCR
        result = process_packaged_food_image(file)
        
        # Convert ingredient names to simple list
        ingredients = [{'name': ing} for ing in result['ingredients']]
        
        return jsonify({
            'ingredients': ingredients,
            'raw_text': result['raw_text'],
            'cleaned_text': result['cleaned_text'],
            'message': 'OCR processing complete'
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error processing OCR: {str(e)}'}), 500
