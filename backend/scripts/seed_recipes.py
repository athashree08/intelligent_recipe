import requests
from database.db import SessionLocal, engine
from database.models import Base, Recipe, Ingredient, RecipeIngredient

Base.metadata.create_all(bind=engine)

db = SessionLocal()

API_URL = "https://www.themealdb.com/api/json/v1/1/search.php?s="

def seed():
    response = requests.get(API_URL)
    meals = response.json()["meals"]

    for meal in meals:
        recipe = Recipe(
            name=meal["strMeal"],
            cuisine=meal["strArea"],
            instructions=meal["strInstructions"],
            cook_time=30,
            difficulty="Medium"
        )
        db.add(recipe)
        db.commit()
        db.refresh(recipe)

        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}")
            qty = meal.get(f"strMeasure{i}")

            if ing and ing.strip():
                ingredient = db.query(Ingredient).filter_by(name=ing.lower()).first()
                if not ingredient:
                    ingredient = Ingredient(name=ing.lower())
                    db.add(ingredient)
                    db.commit()
                    db.refresh(ingredient)

                ri = RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    quantity=qty
                )
                db.add(ri)

        db.commit()

    print("Recipes seeded successfully")

if __name__ == "__main__":
    seed()
