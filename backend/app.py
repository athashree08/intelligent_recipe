from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io
import os

from image_processing.preprocess import preprocess_image
from model.ingredient_model import predict_ingredients
from image_processing.ocr import extract_text
from database.db import SessionLocal
from recommender.matcher import match_recipes

app = FastAPI(title="Intelligent Recipe Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    processed = preprocess_image(image)
    cnn_results = predict_ingredients(processed)
    ocr_results = extract_text(image)

    return {
        "cnn_ingredients": cnn_results,
        "ocr_ingredients": ocr_results
    }

@app.post("/recommend")
def recommend_endpoint(ingredients: list[str]):
    db = SessionLocal()
    results = match_recipes(db, ingredients)
    db.close()
    return results
