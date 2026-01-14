from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def exact_match(user_ingredients, recipe_ingredients):
    """
    Check for exact ingredient matches
    
    Args:
        user_ingredients: List of user's ingredients
        recipe_ingredients: List of recipe's ingredients
    
    Returns:
        Boolean indicating if all recipe ingredients are available
    """
    user_set = set([ing.lower().strip() for ing in user_ingredients])
    recipe_set = set([ing.lower().strip() for ing in recipe_ingredients])
    
    return recipe_set.issubset(user_set)

def partial_match(user_ingredients, recipe_ingredients):
    """
    Calculate partial match score
    
    Args:
        user_ingredients: List of user's ingredients
        recipe_ingredients: List of recipe's ingredients
    
    Returns:
        Float score between 0 and 1
    """
    if not recipe_ingredients:
        return 0.0
    
    user_set = set([ing.lower().strip() for ing in user_ingredients])
    recipe_set = set([ing.lower().strip() for ing in recipe_ingredients])
    
    # Count matches
    matches = len(user_set.intersection(recipe_set))
    
    # Calculate score
    score = matches / len(recipe_set)
    
    return score

def fuzzy_match_ingredient(user_ingredient, recipe_ingredient, threshold=0.6):
    """
    Fuzzy string matching for ingredient names
    
    Args:
        user_ingredient: User's ingredient name
        recipe_ingredient: Recipe's ingredient name
        threshold: Similarity threshold
    
    Returns:
        Boolean indicating if ingredients match
    """
    user_ing = user_ingredient.lower().strip()
    recipe_ing = recipe_ingredient.lower().strip()
    
    # Exact match
    if user_ing == recipe_ing:
        return True
    
    # Check if one contains the other
    if user_ing in recipe_ing or recipe_ing in user_ing:
        return True
    
    # Simple word overlap
    user_words = set(user_ing.split())
    recipe_words = set(recipe_ing.split())
    
    if user_words.intersection(recipe_words):
        overlap = len(user_words.intersection(recipe_words))
        total = max(len(user_words), len(recipe_words))
        if overlap / total >= threshold:
            return True
    
    return False

def calculate_match_score(user_ingredients, recipe):
    """
    Calculate match score between user ingredients and recipe
    
    Args:
        user_ingredients: List of user's ingredients (detected from image)
        recipe: Recipe dictionary with ingredients
    
    Returns:
        Float score between 0 and 1
        
    STRICT MATCHING: Recipe must contain at least one user ingredient
    """
    recipe_ingredients = recipe.get('ingredients', [])
    
    if not recipe_ingredients or not user_ingredients:
        return 0.0
    
    # Extract recipe ingredient names
    recipe_ing_names = []
    for ing in recipe_ingredients:
        if isinstance(ing, dict):
            recipe_ing_names.append(ing.get('name', '').lower())
        else:
            recipe_ing_names.append(str(ing).lower())
    
    # Count how many USER ingredients are found in the recipe
    matched_user_ingredients = 0
    
    for user_ing in user_ingredients:
        user_ing_lower = user_ing.lower().strip()
        
        # Check if this user ingredient exists in recipe
        found = False
        for recipe_ing in recipe_ing_names:
            if fuzzy_match_ingredient(user_ing_lower, recipe_ing):
                found = True
                break
        
        if found:
            matched_user_ingredients += 1
    
    # STRICT FILTER: If NO user ingredients found, return 0
    if matched_user_ingredients == 0:
        return 0.0
    
    # Calculate match percentage based on user ingredients found
    match_percentage = matched_user_ingredients / len(user_ingredients)
    
    return match_percentage


def rank_recipes_by_ingredients(user_ingredients, recipes):
    """
    Rank recipes by ingredient match score
    
    Args:
        user_ingredients: List of user's ingredients
        recipes: List of recipe dictionaries
    
    Returns:
        List of recipes sorted by match score (descending)
    """
    scored_recipes = []
    
    for recipe in recipes:
        score = calculate_match_score(user_ingredients, recipe)
        recipe['match_score'] = score
        scored_recipes.append(recipe)
    
    # Sort by score (descending)
    scored_recipes.sort(key=lambda x: x['match_score'], reverse=True)
    
    return scored_recipes
