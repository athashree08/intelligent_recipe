import requests
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import RecipeDB

def fetch_from_mealdb():
    """
    Fetch recipes from TheMealDB API (free, no API key needed!)
    
    Returns:
        List of recipe dictionaries
    """
    recipes = []
    
    # TheMealDB endpoints
    base_url = "https://www.themealdb.com/api/json/v1/1"
    
    # Fetch recipes by our trained ingredients
    ingredients = ['apple', 'banana', 'tomato', 'onion', 'potato', 'carrot', 'cucumber', 'orange', 'lemon', 'corn']
    
    print("Fetching recipes from TheMealDB API...")
    print("=" * 70)
    
    for ingredient in ingredients:
        try:
            # Search by ingredient
            url = f"{base_url}/filter.php?i={ingredient}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                meals = data.get('meals', [])
                
                if meals:
                    print(f"\n🔍 Found {len(meals)} recipes with {ingredient}")
                    
                    # Get full details for each meal
                    for meal in meals[:5]:  # Limit to 5 per ingredient
                        meal_id = meal.get('idMeal')
                        detail_url = f"{base_url}/lookup.php?i={meal_id}"
                        detail_response = requests.get(detail_url, timeout=10)
                        
                        if detail_response.status_code == 200:
                            detail_data = detail_response.json()
                            meal_detail = detail_data.get('meals', [{}])[0]
                            
                            if meal_detail:
                                recipe = parse_mealdb_recipe(meal_detail)
                                recipes.append(recipe)
                                print(f"  ✓ {recipe['name']}")
                else:
                    print(f"  ✗ No recipes found for {ingredient}")
        except Exception as e:
            print(f"  ✗ Error fetching {ingredient}: {e}")
    
    return recipes

def parse_mealdb_recipe(meal):
    """
    Parse TheMealDB recipe into our schema
    
    Args:
        meal: Recipe data from TheMealDB
    
    Returns:
        Recipe dictionary in our format
    """
    # Extract ingredients
    ingredients = []
    for i in range(1, 21):  # TheMealDB has up to 20 ingredients
        ingredient_key = f'strIngredient{i}'
        measure_key = f'strMeasure{i}'
        
        ingredient_name = meal.get(ingredient_key, '').strip()
        measure = meal.get(measure_key, '').strip()
        
        if ingredient_name:
            ingredients.append({
                'name': ingredient_name.lower(),
                'quantity': measure if measure else '1',
                'unit': 'unit'
            })
    
    # Parse instructions
    instructions_text = meal.get('strInstructions', '')
    instructions = [step.strip() for step in instructions_text.split('.') if step.strip()]
    
    # Determine dietary type
    dietary_type = 'Regular'
    category = meal.get('strCategory', '').lower()
    if 'vegetarian' in category or 'vegan' in category:
        dietary_type = 'Vegetarian'
    
    # Map area to cuisine
    cuisine_map = {
        'American': 'American',
        'British': 'British',
        'Canadian': 'American',
        'Chinese': 'Chinese',
        'Croatian': 'European',
        'Dutch': 'European',
        'Egyptian': 'Middle Eastern',
        'French': 'French',
        'Greek': 'Greek',
        'Indian': 'Indian',
        'Irish': 'Irish',
        'Italian': 'Italian',
        'Jamaican': 'Caribbean',
        'Japanese': 'Japanese',
        'Kenyan': 'African',
        'Malaysian': 'Asian',
        'Mexican': 'Mexican',
        'Moroccan': 'Middle Eastern',
        'Polish': 'European',
        'Portuguese': 'European',
        'Russian': 'European',
        'Spanish': 'Spanish',
        'Thai': 'Thai',
        'Tunisian': 'Middle Eastern',
        'Turkish': 'Middle Eastern',
        'Vietnamese': 'Vietnamese',
        'Unknown': 'International'
    }
    
    area = meal.get('strArea', 'Unknown')
    cuisine = cuisine_map.get(area, 'International')
    
    recipe = {
        'name': meal.get('strMeal', 'Unknown Recipe'),
        'cuisine': cuisine,
        'dietary_type': dietary_type,
        'cooking_time': 30,  # TheMealDB doesn't provide cooking time
        'ingredients': ingredients,
        'instructions': instructions[:10],  # Limit instructions
        'image_url': meal.get('strMealThumb', ''),  # Recipe image from TheMealDB
        'nutrition': {
            'calories': 0,  # TheMealDB doesn't provide nutrition
            'protein': 0,
            'carbs': 0,
            'fats': 0
        }
    }
    
    return recipe

def populate_from_mealdb():
    """
    Populate database with recipes from TheMealDB
    """
    print("\n" + "=" * 70)
    print("POPULATING DATABASE FROM THEMEALDB API")
    print("=" * 70)
    
    # Fetch recipes
    recipes = fetch_from_mealdb()
    
    print("\n" + "=" * 70)
    print(f"Fetched {len(recipes)} recipes from TheMealDB")
    print("=" * 70)
    
    # Add to database
    count = 0
    duplicates = 0
    
    for recipe in recipes:
        try:
            RecipeDB.create_recipe(recipe)
            count += 1
        except Exception as e:
            if 'duplicate' in str(e).lower():
                duplicates += 1
            else:
                print(f"✗ Error adding {recipe['name']}: {e}")
    
    print("\n" + "=" * 70)
    print("DATABASE UPDATE COMPLETE")
    print("=" * 70)
    print(f"✓ Successfully added: {count} recipes")
    print(f"⊘ Duplicates skipped: {duplicates}")
    print(f"📊 Total new recipes: {count}")
    print("\nYour database now has real recipes from TheMealDB!")
    print("These are professional recipes with proper ingredients and instructions.")

if __name__ == '__main__':
    populate_from_mealdb()
