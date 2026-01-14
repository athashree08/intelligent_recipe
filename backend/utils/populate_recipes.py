import requests
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import RecipeDB

def fetch_recipes_from_api(api_key=None, num_recipes=50):
    """
    Fetch recipes from public API (e.g., Spoonacular)
    
    Args:
        api_key: API key for recipe service
        num_recipes: Number of recipes to fetch
    
    Returns:
        List of recipe dictionaries
    """
    if not api_key:
        print("No API key provided, using static data instead")
        return get_static_recipes()
    
    try:
        # Example using Spoonacular API
        url = f"https://api.spoonacular.com/recipes/random?number={num_recipes}&apiKey={api_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            recipes = parse_spoonacular_recipes(data.get('recipes', []))
            return recipes
        else:
            print(f"API request failed: {response.status_code}")
            return get_static_recipes()
            
    except Exception as e:
        print(f"Error fetching from API: {e}")
        return get_static_recipes()

def parse_spoonacular_recipes(api_recipes):
    """
    Parse Spoonacular API response into our schema
    
    Args:
        api_recipes: List of recipes from API
    
    Returns:
        List of formatted recipe dictionaries
    """
    recipes = []
    
    for api_recipe in api_recipes:
        recipe = {
            'name': api_recipe.get('title', ''),
            'cuisine': api_recipe.get('cuisines', ['General'])[0] if api_recipe.get('cuisines') else 'General',
            'dietary_type': get_dietary_type(api_recipe),
            'cooking_time': api_recipe.get('readyInMinutes', 30),
            'ingredients': parse_ingredients(api_recipe.get('extendedIngredients', [])),
            'instructions': parse_instructions(api_recipe.get('instructions', '')),
            'nutrition': {
                'calories': api_recipe.get('nutrition', {}).get('nutrients', [{}])[0].get('amount', 0),
                'protein': get_nutrient(api_recipe, 'Protein'),
                'carbs': get_nutrient(api_recipe, 'Carbohydrates'),
                'fats': get_nutrient(api_recipe, 'Fat')
            }
        }
        recipes.append(recipe)
    
    return recipes

def get_dietary_type(api_recipe):
    """Extract dietary type from API recipe"""
    if api_recipe.get('vegan'):
        return 'Vegan'
    elif api_recipe.get('vegetarian'):
        return 'Vegetarian'
    elif api_recipe.get('glutenFree'):
        return 'Gluten-Free'
    elif api_recipe.get('ketogenic'):
        return 'Keto'
    return 'Regular'

def parse_ingredients(api_ingredients):
    """Parse ingredients from API format"""
    ingredients = []
    for ing in api_ingredients:
        ingredients.append({
            'name': ing.get('name', ''),
            'quantity': ing.get('amount', 0),
            'unit': ing.get('unit', '')
        })
    return ingredients

def parse_instructions(instructions_text):
    """Parse instructions into list"""
    if isinstance(instructions_text, list):
        return instructions_text
    
    # Simple parsing
    steps = instructions_text.split('.')
    return [step.strip() for step in steps if step.strip()]

def get_nutrient(api_recipe, nutrient_name):
    """Extract specific nutrient value"""
    nutrients = api_recipe.get('nutrition', {}).get('nutrients', [])
    for nutrient in nutrients:
        if nutrient.get('name') == nutrient_name:
            return nutrient.get('amount', 0)
    return 0

def get_static_recipes():
    """
    Return static recipe data as fallback
    
    Returns:
        List of recipe dictionaries
    """
    return [
        {
            'name': 'Spaghetti Carbonara',
            'cuisine': 'Italian',
            'dietary_type': 'Regular',
            'cooking_time': 25,
            'ingredients': [
                {'name': 'spaghetti', 'quantity': 400, 'unit': 'g'},
                {'name': 'eggs', 'quantity': 4, 'unit': 'whole'},
                {'name': 'bacon', 'quantity': 200, 'unit': 'g'},
                {'name': 'parmesan cheese', 'quantity': 100, 'unit': 'g'},
                {'name': 'black pepper', 'quantity': 1, 'unit': 'tsp'}
            ],
            'instructions': [
                'Cook spaghetti according to package directions',
                'Fry bacon until crispy',
                'Beat eggs with grated parmesan',
                'Drain pasta and mix with bacon',
                'Remove from heat and stir in egg mixture',
                'Season with black pepper and serve'
            ],
            'nutrition': {'calories': 650, 'protein': 28, 'carbs': 75, 'fats': 25}
        },
        {
            'name': 'Vegetable Stir Fry',
            'cuisine': 'Chinese',
            'dietary_type': 'Vegetarian',
            'cooking_time': 15,
            'ingredients': [
                {'name': 'broccoli', 'quantity': 200, 'unit': 'g'},
                {'name': 'bell peppers', 'quantity': 2, 'unit': 'whole'},
                {'name': 'carrots', 'quantity': 2, 'unit': 'whole'},
                {'name': 'soy sauce', 'quantity': 3, 'unit': 'tbsp'},
                {'name': 'ginger', 'quantity': 1, 'unit': 'tbsp'},
                {'name': 'garlic', 'quantity': 3, 'unit': 'cloves'}
            ],
            'instructions': [
                'Chop all vegetables into bite-sized pieces',
                'Heat oil in a wok over high heat',
                'Add ginger and garlic, stir for 30 seconds',
                'Add vegetables and stir fry for 5-7 minutes',
                'Add soy sauce and toss to coat',
                'Serve hot over rice'
            ],
            'nutrition': {'calories': 180, 'protein': 8, 'carbs': 32, 'fats': 4}
        },
        {
            'name': 'Chicken Tacos',
            'cuisine': 'Mexican',
            'dietary_type': 'Regular',
            'cooking_time': 20,
            'ingredients': [
                {'name': 'chicken breast', 'quantity': 500, 'unit': 'g'},
                {'name': 'taco shells', 'quantity': 8, 'unit': 'whole'},
                {'name': 'lettuce', 'quantity': 1, 'unit': 'head'},
                {'name': 'tomatoes', 'quantity': 2, 'unit': 'whole'},
                {'name': 'cheese', 'quantity': 100, 'unit': 'g'},
                {'name': 'taco seasoning', 'quantity': 2, 'unit': 'tbsp'}
            ],
            'instructions': [
                'Cook chicken with taco seasoning',
                'Shred the cooked chicken',
                'Chop lettuce and tomatoes',
                'Warm taco shells',
                'Fill shells with chicken and toppings',
                'Serve with salsa and sour cream'
            ],
            'nutrition': {'calories': 420, 'protein': 35, 'carbs': 38, 'fats': 15}
        }
    ]

def populate_database():
    """
    Populate MongoDB with recipe data
    """
    print("Populating recipe database...")
    
    # Try to fetch from API (will fallback to static data)
    recipes = fetch_recipes_from_api()
    
    # Add static recipes to ensure we have data
    recipes.extend(get_static_recipes())
    
    # Insert into database
    count = 0
    for recipe in recipes:
        try:
            RecipeDB.create_recipe(recipe)
            count += 1
            print(f"Added: {recipe['name']}")
        except Exception as e:
            print(f"Error adding {recipe.get('name', 'unknown')}: {e}")
    
    print(f"\nSuccessfully added {count} recipes to database")

if __name__ == '__main__':
    populate_database()
