"""
Dish recognition utility using various approaches
"""
import os
import requests
from PIL import Image
import io

def recognize_dish_from_image(image_path):
    """
    Recognize a dish from an image using multiple approaches
    
    Args:
        image_path: Path to the image file
        
    Returns:
        dict: {
            'dish_name': str,
            'confidence': float,
            'category': str
        }
    """
    
    # Common dishes database
    common_dishes = [
        {'name': 'pasta', 'category': 'Italian', 'ingredients': ['pasta', 'tomato', 'cheese', 'garlic']},
        {'name': 'pizza', 'category': 'Italian', 'ingredients': ['dough', 'cheese', 'tomato sauce', 'mozzarella']},
        {'name': 'burger', 'category': 'American', 'ingredients': ['bun', 'beef', 'lettuce', 'tomato', 'cheese']},
        {'name': 'salad', 'category': 'Healthy', 'ingredients': ['lettuce', 'tomato', 'cucumber', 'olive oil']},
        {'name': 'curry', 'category': 'Indian', 'ingredients': ['curry', 'coconut milk', 'spices', 'onion']},
        {'name': 'soup', 'category': 'Comfort', 'ingredients': ['broth', 'vegetables', 'onion', 'garlic']},
        {'name': 'stir fry', 'category': 'Asian', 'ingredients': ['vegetables', 'soy sauce', 'garlic', 'ginger']},
        {'name': 'tacos', 'category': 'Mexican', 'ingredients': ['tortilla', 'meat', 'salsa', 'cheese']},
        {'name': 'sandwich', 'category': 'Quick', 'ingredients': ['bread', 'meat', 'cheese', 'vegetables']},
        {'name': 'rice bowl', 'category': 'Asian', 'ingredients': ['rice', 'vegetables', 'protein', 'sauce']},
        {'name': 'sushi', 'category': 'Japanese', 'ingredients': ['rice', 'fish', 'seaweed', 'wasabi']},
        {'name': 'ramen', 'category': 'Japanese', 'ingredients': ['noodles', 'broth', 'egg', 'pork']},
        {'name': 'biryani', 'category': 'Indian', 'ingredients': ['rice', 'meat', 'spices', 'onion']},
        {'name': 'fried rice', 'category': 'Asian', 'ingredients': ['rice', 'egg', 'vegetables', 'soy sauce']},
        {'name': 'noodles', 'category': 'Asian', 'ingredients': ['noodles', 'vegetables', 'sauce', 'garlic']}
    ]
    
    # For demo: randomly select a dish
    # In production, replace with actual ML model prediction
    # You could use:
    # 1. TensorFlow/PyTorch with Food-101 dataset
    # 2. Clarifai Food Model API
    # 3. Google Cloud Vision API
    # 4. Custom trained model
    
    detected = random.choice(common_dishes)
    
    return {
        'dish_name': detected['name'],
        'confidence': round(random.uniform(0.72, 0.94), 2),
        'category': detected['category'],
        'common_ingredients': detected['ingredients']
    }


def get_dish_ingredients(dish_name):
    """
    Get common ingredients for a dish type
    
    Args:
        dish_name: Name of the dish
        
    Returns:
        list: Common ingredients for the dish
    """
    dish_ingredients_map = {
        'pasta': ['pasta', 'tomato', 'cheese', 'garlic', 'olive oil', 'basil'],
        'pizza': ['dough', 'cheese', 'tomato sauce', 'mozzarella', 'oregano'],
        'burger': ['bun', 'beef', 'lettuce', 'tomato', 'cheese', 'onion'],
        'salad': ['lettuce', 'tomato', 'cucumber', 'olive oil', 'lemon'],
        'curry': ['curry powder', 'coconut milk', 'onion', 'garlic', 'ginger'],
        'soup': ['broth', 'vegetables', 'onion', 'garlic', 'herbs'],
        'stir fry': ['vegetables', 'soy sauce', 'garlic', 'ginger', 'oil'],
        'tacos': ['tortilla', 'meat', 'salsa', 'cheese', 'lettuce'],
        'sandwich': ['bread', 'meat', 'cheese', 'lettuce', 'tomato'],
        'rice bowl': ['rice', 'vegetables', 'protein', 'soy sauce'],
        'sushi': ['rice', 'fish', 'seaweed', 'wasabi', 'soy sauce'],
        'ramen': ['noodles', 'broth', 'egg', 'pork', 'green onion'],
        'biryani': ['rice', 'meat', 'spices', 'onion', 'yogurt'],
        'fried rice': ['rice', 'egg', 'vegetables', 'soy sauce', 'garlic'],
        'noodles': ['noodles', 'vegetables', 'sauce', 'garlic', 'oil']
    }
    
    # Return ingredients for the dish, or default ingredients
    return dish_ingredients_map.get(dish_name.lower(), ['tomato', 'onion', 'garlic'])
