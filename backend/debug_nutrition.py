import sys
sys.path.insert(0, '.')

from models.database import RecipeDB
from utils.nutrition_api import search_food, get_nutrition

recipe = RecipeDB.get_recipe_by_id('69664e0e56641ab02148813c')

with open('debug_output.txt', 'w', encoding='utf-8') as f:
    f.write(f"Recipe: {recipe['name']}\n")
    f.write(f"\nIngredient breakdown:\n")
    f.write("=" * 80 + "\n")

    total_calories = 0

    for ing in recipe['ingredients']:
        name = ing['name']
        quantity_str = ing.get('quantity', '1')
        unit = ing.get('unit', 'unit')
        
        # Search for ingredient
        foods = search_food(name)
        if not foods:
            f.write(f"\n❌ {name}: No match found\n")
            continue
        
        # Get nutrition
        nutrition = get_nutrition(foods[0]['fdc_id'])
        if not nutrition:
            f.write(f"\n❌ {name}: No nutrition data\n")
            continue
        
        # Get quantity string and stored unit
        quantity_str_raw = str(ing.get('quantity', '1')).lower()
        stored_unit = str(ing.get('unit', '')).lower()
        
        # Extract numeric value
        import re
        match = re.search(r'(\d+(?:\.\d+)?)', quantity_str_raw)
        if match:
            quantity = float(match.group(1))
        else:
            quantity = 1.0
        
        # Determine effective unit
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
            elif 'clove' in quantity_str_raw or 'cloves' in quantity_str_raw:
                grams = quantity * 5.0
            elif 'slice' in quantity_str_raw:
                grams = quantity * 25.0
            else:
                grams = quantity * 100.0
        
        calories = (nutrition['calories'] * grams) / 100.0
        total_calories += calories
        
        f.write(f"\n{name}:\n")
        f.write(f"  Quantity: {quantity_str_raw} {unit}\n")
        f.write(f"  Matched: {foods[0]['description']}\n")
        f.write(f"  Estimated grams: {grams}g\n")
        f.write(f"  Calories/100g: {nutrition['calories']}\n")
        f.write(f"  Total calories: {calories:.0f}\n")

    f.write(f"\n{'=' * 80}\n")
    f.write(f"TOTAL CALORIES: {total_calories:.0f}\n")
