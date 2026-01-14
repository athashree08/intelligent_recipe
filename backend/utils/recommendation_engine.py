from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def create_recipe_text(recipe):
    """
    Create text representation of recipe for TF-IDF
    
    Args:
        recipe: Recipe dictionary
    
    Returns:
        String representation
    """
    text_parts = []
    
    # Add recipe name
    if recipe.get('name'):
        text_parts.append(recipe['name'])
    
    # Add ingredients
    if isinstance(recipe.get('ingredients'), list):
        for ing in recipe['ingredients']:
            if isinstance(ing, dict):
                text_parts.append(ing.get('name', ''))
            else:
                text_parts.append(str(ing))
    
    # Add cuisine
    if recipe.get('cuisine'):
        text_parts.append(recipe['cuisine'])
    
    # Add dietary type
    if recipe.get('dietary_type'):
        text_parts.append(recipe['dietary_type'])
    
    return ' '.join(text_parts)

def content_based_filtering(user_ingredients, recipes, top_n=10):
    """
    Content-based recommendation using TF-IDF and cosine similarity
    
    Args:
        user_ingredients: List of user's ingredients
        recipes: List of recipe dictionaries
        top_n: Number of top recommendations to return
    
    Returns:
        List of top N recommended recipes
    """
    if not recipes:
        return []
    
    # Create user query
    user_query = ' '.join(user_ingredients)
    
    # Create recipe texts
    recipe_texts = [create_recipe_text(recipe) for recipe in recipes]
    
    # Add user query to corpus
    corpus = [user_query] + recipe_texts
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Calculate cosine similarity
    user_vector = tfidf_matrix[0]
    recipe_vectors = tfidf_matrix[1:]
    
    similarities = cosine_similarity(user_vector, recipe_vectors)[0]
    
    # Add similarity scores to recipes
    for i, recipe in enumerate(recipes):
        recipe['similarity_score'] = float(similarities[i])
    
    # Sort by similarity
    sorted_recipes = sorted(recipes, key=lambda x: x['similarity_score'], reverse=True)
    
    return sorted_recipes[:top_n]

def hybrid_recommendation(user_ingredients, recipes, top_n=10, alpha=0.9):
    """
    Hybrid recommendation combining ingredient matching and content-based filtering
    
    Args:
        user_ingredients: List of user's ingredients
        recipes: List of recipe dictionaries
        top_n: Number of recommendations
        alpha: Weight for ingredient matching (1-alpha for content-based)
               Default 0.9 = 90% ingredient match, 10% content similarity
    
    Returns:
        List of top N recommended recipes (deduplicated)
    """
    from utils.ingredient_matcher import calculate_match_score
    
    if not recipes:
        return []
    
    # Deduplicate recipes by name first
    seen_names = set()
    unique_recipes = []
    for recipe in recipes:
        name = recipe.get('name', '').lower()
        if name not in seen_names:
            seen_names.add(name)
            unique_recipes.append(recipe)
    
    # Calculate ingredient match scores
    for recipe in unique_recipes:
        match_score = calculate_match_score(user_ingredients, recipe)
        recipe['match_score'] = match_score
    
    # Filter out recipes with 0% match (don't contain any detected ingredients)
    relevant_recipes = [r for r in unique_recipes if r.get('match_score', 0) > 0]
    
    # SMART FILTERING: Focus on the PRIMARY ingredient (highest confidence)
    # If user detected banana (100%), carrot (0%), lemon (0%), etc.
    # Only show recipes that contain BANANA
    if relevant_recipes and user_ingredients:
        # The first ingredient in the list has the highest confidence
        primary_ingredient = user_ingredients[0].lower()
        
        # Filter recipes that contain the primary ingredient
        primary_recipes = []
        for recipe in relevant_recipes:
            recipe_ing_names = []
            for ing in recipe.get('ingredients', []):
                if isinstance(ing, dict):
                    recipe_ing_names.append(ing.get('name', '').lower())
                else:
                    recipe_ing_names.append(str(ing).lower())
            
            # Check if primary ingredient is in this recipe
            from utils.ingredient_matcher import fuzzy_match_ingredient
            for recipe_ing in recipe_ing_names:
                if fuzzy_match_ingredient(primary_ingredient, recipe_ing):
                    primary_recipes.append(recipe)
                    break
        
        # Use primary ingredient recipes if found, otherwise use all relevant
        highly_relevant_recipes = primary_recipes if primary_recipes else relevant_recipes
    else:
        highly_relevant_recipes = relevant_recipes
    
    if not highly_relevant_recipes:
        # If no recipes match, return empty list
        return []
    
    # Get content-based scores
    content_recipes = content_based_filtering(user_ingredients, highly_relevant_recipes, top_n=len(highly_relevant_recipes))
    
    # Create similarity score mapping
    similarity_map = {id(r): r.get('similarity_score', 0) for r in content_recipes}
    
    # Calculate hybrid score
    for recipe in highly_relevant_recipes:
        match = recipe.get('match_score', 0)
        similarity = similarity_map.get(id(recipe), 0)
        recipe['hybrid_score'] = alpha * match + (1 - alpha) * similarity
    
    # Sort by hybrid score
    sorted_recipes = sorted(highly_relevant_recipes, key=lambda x: x.get('hybrid_score', 0), reverse=True)
    
    return sorted_recipes[:top_n]

def get_recommendations(user_ingredients, recipes, method='hybrid', top_n=10):
    """
    Get recipe recommendations
    
    Args:
        user_ingredients: List of user's ingredients
        recipes: List of recipe dictionaries
        method: 'hybrid', 'content', or 'ingredient'
        top_n: Number of recommendations
    
    Returns:
        List of recommended recipes
    """
    if method == 'content':
        return content_based_filtering(user_ingredients, recipes, top_n)
    elif method == 'ingredient':
        from utils.ingredient_matcher import rank_recipes_by_ingredients
        return rank_recipes_by_ingredients(user_ingredients, recipes)[:top_n]
    else:  # hybrid
        return hybrid_recommendation(user_ingredients, recipes, top_n)
