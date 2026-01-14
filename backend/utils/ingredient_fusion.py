import re

# Basic ingredient whitelist (can grow later)
KNOWN_INGREDIENTS = {
    "banana", "milk", "egg", "flour", "sugar", "butter",
    "onion", "tomato", "garlic", "cheese", "oil"
}

def extract_ingredients_from_ocr(text: str):
    text = text.lower()
    words = re.findall(r"[a-z]+", text)
    return {w for w in words if w in KNOWN_INGREDIENTS}


def combine_ingredients(cnn_results, ocr_text):
    """
    cnn_results: list of {name, confidence}
    ocr_text: raw OCR string
    """

    ingredients = {}

    # 1️⃣ CNN ingredients (confidence-weighted)
    for item in cnn_results:
        name = item["name"].lower()
        confidence = item["confidence"]

        if confidence > 0.15:  # threshold to reduce wild guesses
            ingredients[name] = confidence

    # 2️⃣ OCR ingredients (boost confidence)
    ocr_ingredients = extract_ingredients_from_ocr(ocr_text)
    for ing in ocr_ingredients:
        ingredients[ing] = max(ingredients.get(ing, 0), 0.9)

    return sorted(
        [{"name": k, "confidence": round(v, 2)} for k, v in ingredients.items()],
        key=lambda x: x["confidence"],
        reverse=True
    )
