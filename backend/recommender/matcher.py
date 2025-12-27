from rapidfuzz import fuzz
from database.models import Recipe

def match_recipes(db, user_ingredients, threshold=80):
    results = []

    recipes = db.query(Recipe).all()

    for recipe in recipes:
        if not recipe.ingredients:
            continue

        recipe_ings = [ri.ingredient.name.lower() for ri in recipe.ingredients]
        user_ings = [ui.lower() for ui in user_ingredients]

        matched = 0

        for ui in user_ings:
            for ri in recipe_ings:
                if fuzz.partial_ratio(ui, ri) >= threshold:
                    matched += 1
                    break

        # Penalize recipes with very few ingredients
        score = (matched / max(len(recipe_ings), 3)) * 100

        if matched > 0:
            results.append({
                "recipe": recipe.name,
                "matched_ingredients": matched,
                "total_ingredients": len(recipe_ings),
                "match_percentage": round(min(score, 100), 2)
            })

    return sorted(results, key=lambda x: x["match_percentage"], reverse=True)
