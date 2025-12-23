import json
from .matcher import match_ingredients

def load_recipes():
    with open("recipes/sample_recipes.json", "r") as f:
        return json.load(f)

def recommend_recipes(user_ingredients, threshold=0.3):
    recipes = load_recipes()
    recommendations = []

    for recipe in recipes:
        result = match_ingredients(
            user_ingredients,
            recipe["ingredients"]
        )

        if result["match_score"] >= threshold:
            recommendations.append({
                "recipe_name": recipe["name"],
                "match_score": result["match_score"],
                "matched_ingredients": result["matched_ingredients"],
                "cook_time": recipe["cook_time"],
                "difficulty": recipe["difficulty"],
                "cuisine": recipe["cuisine"]
            })

    return sorted(
        recommendations,
        key=lambda x: x["match_score"],
        reverse=True
    )
