import requests
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

USDA_API_KEY = os.getenv('USDA_API_KEY')
USDA_BASE_URL = 'https://api.nal.usda.gov/fdc/v1'

@lru_cache(maxsize=1000)
def search_food(query, page_size=10):
    """
    Search for food items in USDA database
    
    Args:
        query: Food name to search for
        page_size: Number of results to return
    
    Returns:
        List of food items with FDC IDs
    """
    try:
        url = f"{USDA_BASE_URL}/foods/search"
        
        # Add 'raw' to query to prefer fresh ingredients
        search_query = f"{query} raw"
        
        params = {
            'api_key': USDA_API_KEY,
            'query': search_query,
            'pageSize': page_size,
            'dataType': ['Foundation', 'SR Legacy']  # Most accurate data
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        foods = data.get('foods', [])
        
        # Filter out dehydrated, dried, concentrated, or canned versions
        # These have much higher calorie density and skew results
        filtered_foods = []
        skip_keywords = ['dehydrated', 'dried', 'powder', 'concentrated', 'freeze-dried', 'canned']
        
        for food in foods:
            description = food.get('description', '').lower()
            # Skip if description contains unwanted keywords
            if not any(keyword in description for keyword in skip_keywords):
                filtered_foods.append({
                    'fdc_id': food.get('fdcId'),
                    'description': food.get('description'),
                    'data_type': food.get('dataType')
                })
        
        # If filtering removed all results, return original results
        if not filtered_foods and foods:
            filtered_foods = [{
                'fdc_id': food.get('fdcId'),
                'description': food.get('description'),
                'data_type': food.get('dataType')
            } for food in foods[:5]]
        
        return filtered_foods[:5]  # Return top 5 results
        
    except Exception as e:
        print(f"Error searching food '{query}': {e}")
        return []

@lru_cache(maxsize=500)
def get_nutrition(fdc_id):
    """
    Get nutrition data for a specific food item
    
    Args:
        fdc_id: FDC ID of the food item
    
    Returns:
        Dictionary with nutrition per 100g
    """
    try:
        url = f"{USDA_BASE_URL}/food/{fdc_id}"
        params = {'api_key': USDA_API_KEY}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        nutrients = data.get('foodNutrients', [])
        
        # Extract key nutrients (per 100g)
        nutrition = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0
        }
        
        energy_found = False  # Track if we've found calories already
        
        for nutrient in nutrients:
            nutrient_name = nutrient.get('nutrient', {}).get('name', '').lower()
            amount = nutrient.get('amount', 0)
            
            # Get calories (first Energy value is in kcal, second is in kJ)
            if 'energy' in nutrient_name and not energy_found:
                nutrition['calories'] = round(amount, 1)
                energy_found = True
            elif 'protein' in nutrient_name:
                nutrition['protein'] = round(amount, 1)
            elif 'carbohydrate' in nutrient_name:
                nutrition['carbs'] = round(amount, 1)
            elif 'total lipid' in nutrient_name or 'fat, total' in nutrient_name:
                nutrition['fat'] = round(amount, 1)
        
        return nutrition
        
    except Exception as e:
        print(f"Error getting nutrition for FDC ID {fdc_id}: {e}")
        return None

def calculate_recipe_nutrition(ingredients):
    """
    Calculate total nutrition for a recipe based on ingredients
    
    Args:
        ingredients: List of ingredient dicts with 'name', 'quantity', 'unit'
    
    Returns:
        Dictionary with total nutrition values
    """
    total_nutrition = {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0,
        'calculated': True
    }
    
    successful_matches = 0
    
    for ingredient in ingredients:
        try:
            # Search for the ingredient
            ingredient_name = ingredient.get('name', '')
            if not ingredient_name:
                continue
            
            foods = search_food(ingredient_name)
            if not foods:
                print(f"No match found for: {ingredient_name}")
                continue
            
            # Use the first (best) match
            best_match = foods[0]
            fdc_id = best_match['fdc_id']
            
            # Get nutrition data (per 100g)
            nutrition_per_100g = get_nutrition(fdc_id)
            if not nutrition_per_100g:
                continue
            
            # Get quantity string and stored unit
            quantity_str_raw = str(ingredient.get('quantity', '1')).lower()
            stored_unit = str(ingredient.get('unit', '')).lower()
            
            # Extract numeric value
            import re
            match = re.search(r'(\d+(?:\.\d+)?)', quantity_str_raw)
            if match:
                quantity = float(match.group(1))
            else:
                quantity = 1.0
            
            # Determine effective unit
            # If stored unit is generic, try to find unit in quantity string
            effective_unit = stored_unit
            if stored_unit in ['', 'unit', 'none', 'item']:
                # Helper for word boundary check (matches " g", "200g", "200 g")
                def has_unit(u, text):
                    # Match if unit is standalone word OR follows a digit
                    pattern = r'(?:^|\d|\s)' + re.escape(u) + r'(?:$|\s|\b)'
                    return re.search(pattern, text) is not None
                
                if 'mg' in quantity_str_raw and has_unit('mg', quantity_str_raw):
                    effective_unit = 'mg'
                elif 'kg' in quantity_str_raw and has_unit('kg', quantity_str_raw):
                    effective_unit = 'kg'
                elif (has_unit('g', quantity_str_raw) or 'grams' in quantity_str_raw) and 'mg' not in quantity_str_raw and 'kg' not in quantity_str_raw and 'large' not in quantity_str_raw and 'orange' not in quantity_str_raw and 'egg' not in quantity_str_raw:
                    effective_unit = 'g'
                elif has_unit('ml', quantity_str_raw):
                    effective_unit = 'ml'
                elif has_unit('l', quantity_str_raw) and 'ml' not in quantity_str_raw:
                    effective_unit = 'l'
                elif 'tbsp' in quantity_str_raw or 'tablespoon' in quantity_str_raw:
                    effective_unit = 'tbsp'
                elif 'tsp' in quantity_str_raw or 'teaspoon' in quantity_str_raw:
                    effective_unit = 'tsp'
                elif 'cup' in quantity_str_raw:
                    effective_unit = 'cup'
                elif has_unit('oz', quantity_str_raw) or 'ounce' in quantity_str_raw:
                    effective_unit = 'oz'
                elif has_unit('lb', quantity_str_raw) or 'pound' in quantity_str_raw:
                    effective_unit = 'lb'
                elif 'pinch' in quantity_str_raw:
                    effective_unit = 'pinch'
                elif 'splash' in quantity_str_raw or 'sprinkling' in quantity_str_raw:
                    effective_unit = 'splash'
            
            # Convert to grams based on effective unit
            grams = quantity
            
            if 'mg' in effective_unit:
                grams = quantity / 1000.0
            elif 'kg' in effective_unit or 'kilogram' in effective_unit:
                grams = quantity * 1000.0
            elif effective_unit == 'g' or 'gram' in effective_unit:
                grams = quantity
            elif 'ml' in effective_unit:
                grams = quantity  # Assume density of water
            elif 'l' in effective_unit and 'ml' not in effective_unit:
                grams = quantity * 1000.0
            elif 'cup' in effective_unit:
                grams = quantity * 200.0
            elif 'tbsp' in effective_unit or 'tablespoon' in effective_unit:
                grams = quantity * 15.0
            elif 'tsp' in effective_unit or 'teaspoon' in effective_unit:
                grams = quantity * 5.0
            elif 'oz' in effective_unit or 'ounce' in effective_unit:
                grams = quantity * 28.35
            elif 'lb' in effective_unit or 'pound' in effective_unit:
                grams = quantity * 453.59
            elif 'pinch' in effective_unit:
                grams = 0.5  # Fixed small amount
            elif 'splash' in effective_unit:
                grams = 2.0  # Fixed small amount
            else:
                # Text-based estimation for whole items
                if 'large' in quantity_str_raw:
                    grams = quantity * 150.0
                elif 'medium' in quantity_str_raw:
                    grams = quantity * 100.0
                elif 'small' in quantity_str_raw:
                    grams = quantity * 50.0
                elif 'clove' in quantity_str_raw or 'cloves' in quantity_str_raw: # Garlic
                    grams = quantity * 5.0 
                elif 'slice' in quantity_str_raw:
                    grams = quantity * 25.0
                else:
                    # Fallback default
                    grams = quantity * 100.0

            
            # Calculate nutrition for this ingredient
            multiplier = grams / 100.0
            
            total_nutrition['calories'] += nutrition_per_100g['calories'] * multiplier
            total_nutrition['protein'] += nutrition_per_100g['protein'] * multiplier
            total_nutrition['carbs'] += nutrition_per_100g['carbs'] * multiplier
            total_nutrition['fat'] += nutrition_per_100g['fat'] * multiplier
            
            successful_matches += 1
            
        except Exception as e:
            print(f"Error processing ingredient {ingredient.get('name')}: {e}")
            continue
    
    # Round final values
    total_nutrition['calories'] = round(total_nutrition['calories'])
    total_nutrition['protein'] = round(total_nutrition['protein'], 1)
    total_nutrition['carbs'] = round(total_nutrition['carbs'], 1)
    total_nutrition['fat'] = round(total_nutrition['fat'], 1)
    total_nutrition['ingredients_matched'] = successful_matches
    total_nutrition['total_ingredients'] = len(ingredients)
    
    return total_nutrition
