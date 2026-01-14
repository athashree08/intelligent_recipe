import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import recipes_collection

# Get all recipes
recipes = list(recipes_collection.find())
print(f"Total recipes: {len(recipes)}")

# Delete recipes without TheMealDB images
deleted = 0
for recipe in recipes:
    image_url = recipe.get('image_url', '')
    if not image_url or not image_url.startswith('https://www.themealdb.com'):
        recipes_collection.delete_one({'_id': recipe['_id']})
        deleted += 1
        print(f"Deleted: {recipe.get('name')}")

remaining = list(recipes_collection.find())
print(f"\nDeleted {deleted} recipes without TheMealDB images")
print(f"Remaining: {len(remaining)} recipes with real photos")
