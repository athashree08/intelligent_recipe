def match_ingredients(user_ingredients, recipe_ingredients):
    user_set = set(i.lower() for i in user_ingredients)
    recipe_set = set(i.lower() for i in recipe_ingredients)

    matched = user_set.intersection(recipe_set)
    match_score = len(matched) / len(recipe_set)

    return {
        "match_score": round(match_score, 2),
        "matched_ingredients": list(matched)
    }
