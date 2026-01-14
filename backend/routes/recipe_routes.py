from flask import Blueprint, request, jsonify
from bson import ObjectId
from models.database import RecipeDB
from utils.recommendation_engine import get_recommendations
from utils.auth import optional_token

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET'])
@optional_token
def list_recipes(current_user):
    """
    Get all recipes or search with filters
    
    Query parameters:
        cuisine: string (optional)
        dietary_type: string (optional)
        max_time: int (optional)
    
    Returns:
        {
            "recipes": [...]
        }
    """
    try:
        # Check if filters are provided
        filters = {}
        
        if request.args.get('cuisine'):
            filters['cuisine'] = request.args.get('cuisine')
        
        if request.args.get('dietary_type'):
            filters['dietary_type'] = request.args.get('dietary_type')
        
        if request.args.get('max_time'):
            filters['max_cooking_time'] = int(request.args.get('max_time'))
        
        # Get recipes
        if filters:
            recipes = RecipeDB.search_recipes(filters)
        else:
            recipes = RecipeDB.get_all_recipes()
        
        # Convert ObjectId to string
        for recipe in recipes:
            recipe['_id'] = str(recipe['_id'])
        
        return jsonify({
            'recipes': recipes,
            'count': len(recipes)
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching recipes: {str(e)}'}), 500


@recipe_bp.route('/search', methods=['GET'])
@optional_token
def search_recipes(current_user):
    """
    Search recipes with optional filters
    
    Query parameters:
        cuisine: string (optional)
        dietary_type: string (optional)
        max_cooking_time: int (optional)
    
    Returns:
        {
            "recipes": [...]
        }
    """
    try:
        # Get filter parameters
        filters = {}
        
        if request.args.get('cuisine'):
            filters['cuisine'] = request.args.get('cuisine')
        
        if request.args.get('dietary_type'):
            filters['dietary_type'] = request.args.get('dietary_type')
        
        if request.args.get('max_cooking_time'):
            filters['max_cooking_time'] = request.args.get('max_cooking_time')
        
        # Search recipes
        recipes = RecipeDB.search_recipes(filters)
        
        # Convert ObjectId to string
        for recipe in recipes:
            recipe['_id'] = str(recipe['_id'])
        
        return jsonify({
            'recipes': recipes,
            'count': len(recipes)
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error searching recipes: {str(e)}'}), 500

@recipe_bp.route('/recommend', methods=['POST'])
@optional_token
def recommend_recipes(current_user):
    """
    Get recipe recommendations based on ingredients
    
    Request body:
        {
            "ingredients": ["tomato", "onion", ...],
            "method": "hybrid" | "content" | "ingredient" (optional)
        }
    
    Returns:
        {
            "recipes": [...]
        }
    """
    try:
        data = request.get_json()
        
        # Extract ingredients
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({'message': 'No ingredients provided'}), 400
        
        # Extract ingredient names if they're objects
        ingredient_names = []
        for ing in ingredients:
            if isinstance(ing, dict):
                ingredient_names.append(ing.get('name', ''))
            else:
                ingredient_names.append(str(ing))
        
        # Get recommendation method
        method = data.get('method', 'hybrid')
        
        # Get all recipes
        all_recipes = RecipeDB.get_all_recipes()
        
        # Get recommendations
        recommended_recipes = get_recommendations(
            ingredient_names,
            all_recipes,
            method=method,
            top_n=20
        )
        
        # Convert ObjectId to string
        for recipe in recommended_recipes:
            recipe['_id'] = str(recipe['_id'])
        
        return jsonify({
            'recipes': recommended_recipes,
            'count': len(recommended_recipes),
            'method': method
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error getting recommendations: {str(e)}'}), 500

@recipe_bp.route('/<recipe_id>', methods=['GET'])
@optional_token
def get_recipe_details(current_user, recipe_id):
    """
    Get detailed information about a specific recipe
    
    Path parameters:
        recipe_id: MongoDB ObjectId
    
    Returns:
        {
            "recipe": {...}
        }
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(recipe_id):
            return jsonify({'message': 'Invalid recipe ID'}), 400
        
        # Get recipe
        recipe = RecipeDB.get_recipe_by_id(recipe_id)
        
        if not recipe:
            return jsonify({'message': 'Recipe not found'}), 404
        
        # Convert ObjectId to string
        recipe['_id'] = str(recipe['_id'])
        
        # Optionally enhance with generated instructions
        from utils.instruction_generator import enhance_recipe_with_instructions
        
        if not recipe.get('instructions') or len(recipe.get('instructions', [])) == 0:
            recipe = enhance_recipe_with_instructions(recipe)
        
        return jsonify({
            'recipe': recipe
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching recipe: {str(e)}'}), 500

@recipe_bp.route('/search-by-ingredients', methods=['POST'])
@optional_token
def search_by_ingredients(current_user):
    """
    Search recipes by manually entered ingredients
    
    Request body:
        {
            "ingredients": ["tomato", "onion", "garlic"],
            "method": "hybrid" | "content" | "ingredient" (optional)
        }
    
    Returns:
        {
            "recipes": [...],
            "count": int,
            "method": string
        }
    """
    try:
        data = request.get_json()
        
        # Extract ingredients
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({'message': 'No ingredients provided'}), 400
        
        # Clean and normalize ingredient names
        ingredient_names = []
        for ing in ingredients:
            if isinstance(ing, str):
                ingredient_names.append(ing.strip().lower())
            elif isinstance(ing, dict):
                ingredient_names.append(ing.get('name', '').strip().lower())
        
        # Remove empty strings
        ingredient_names = [ing for ing in ingredient_names if ing]
        
        if not ingredient_names:
            return jsonify({'message': 'No valid ingredients provided'}), 400
        
        # Get recommendation method
        method = data.get('method', 'hybrid')
        
        # Get all recipes
        all_recipes = RecipeDB.get_all_recipes()
        
        # Get recommendations
        recommended_recipes = get_recommendations(
            ingredient_names,
            all_recipes,
            method=method,
            top_n=20
        )
        
        # Convert ObjectId to string
        for recipe in recommended_recipes:
            recipe['_id'] = str(recipe['_id'])
        
        return jsonify({
            'recipes': recommended_recipes,
            'count': len(recommended_recipes),
            'method': method,
            'searched_ingredients': ingredient_names
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error searching recipes: {str(e)}'}), 500

@recipe_bp.route('/all', methods=['GET'])
@optional_token
def get_all_recipes(current_user):
    """
    Get all recipes (for testing/debugging)
    
    Returns:
        {
            "recipes": [...]
        }
    """
    try:
        recipes = RecipeDB.get_all_recipes()
        
        # Convert ObjectId to string
        for recipe in recipes:
            recipe['_id'] = str(recipe['_id'])
        
        return jsonify({
            'recipes': recipes,
            'count': len(recipes)
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching recipes: {str(e)}'}), 500

@recipe_bp.route('/filter-options', methods=['GET'])
def get_filter_options():
    """
    Get unique filter options from the database
    
    Returns:
        {
            "cuisines": [...],
            "dietary_types": [...]
        }
    """
    try:
        from models.database import get_db
        db = get_db()
        
        # Get unique cuisines
        cuisines = db.recipes.distinct('cuisine')
        cuisines = [c for c in cuisines if c]  # Remove None/empty values
        cuisines.sort()
        
        # Get unique dietary types
        dietary_types = db.recipes.distinct('dietary_type')
        dietary_types = [d for d in dietary_types if d]  # Remove None/empty values
        dietary_types.sort()
        
        return jsonify({
            'cuisines': cuisines,
            'dietary_types': dietary_types
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching filter options: {str(e)}'}), 500

@recipe_bp.route('/<recipe_id>/nutrition', methods=['GET'])
@optional_token
def calculate_nutrition(current_user, recipe_id):
    """
    Calculate nutrition for a recipe using USDA API
    
    Path parameters:
        recipe_id: MongoDB ObjectId
    
    Returns:
        {
            "nutrition": {
                "calories": int,
                "protein": float,
                "carbs": float,
                "fat": float,
                "calculated": true,
                "ingredients_matched": int,
                "total_ingredients": int
            }
        }
    """
    try:
        from utils.nutrition_api import calculate_recipe_nutrition
        from models.database import get_db
        
        # Validate ObjectId
        if not ObjectId.is_valid(recipe_id):
            return jsonify({'message': 'Invalid recipe ID'}), 400
        
        # Get recipe
        recipe = RecipeDB.get_recipe_by_id(recipe_id)
        
        if not recipe:
            return jsonify({'message': 'Recipe not found'}), 404
        
        # Get ingredients
        ingredients = recipe.get('ingredients', [])
        
        if not ingredients:
            return jsonify({'message': 'Recipe has no ingredients'}), 400
        
        # Calculate nutrition
        nutrition = calculate_recipe_nutrition(ingredients)
        
        # Update recipe in database with calculated nutrition
        db = get_db()
        db.recipes.update_one(
            {'_id': ObjectId(recipe_id)},
            {'$set': {'nutrition': nutrition}}
        )
        
        return jsonify({
            'nutrition': nutrition,
            'message': f'Nutrition calculated successfully ({nutrition["ingredients_matched"]}/{nutrition["total_ingredients"]} ingredients matched)'
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error calculating nutrition: {e}")
        print(traceback.format_exc())
        return jsonify({'message': f'Error calculating nutrition: {str(e)}'}), 500
