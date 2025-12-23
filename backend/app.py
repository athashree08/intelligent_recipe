from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from image_processing.preprocess import preprocess_image
from model.ingredient_model import predict_ingredient
from image_processing.ocr import extract_text
from recipes.recipe_db import recommend_recipes
from PIL import Image
import io

app = FastAPI(title="Intelligent Recipe Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    processed = preprocess_image(image)
    ingredient, confidence = predict_ingredient(processed)
    ocr_text = extract_text(image)

    return {
        "ingredient": ingredient,
        "confidence": round(confidence, 2),
        "ocr_text": ocr_text
    }


@app.post("/recommend")
async def recommend(data: dict):
    user_ingredients = data.get("ingredients", [])
    recommendations = recommend_recipes(user_ingredients)

    return {
        "input_ingredients": user_ingredients,
        "recommendations": recommendations
    }
