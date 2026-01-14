import pytesseract
from PIL import Image
import re
import io

# Configure Tesseract path (update based on installation)
# Windows: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def extract_text_from_image(image_file):
    """
    Extract text from image using Tesseract OCR
    
    Args:
        image_file: File object or path to image
    
    Returns:
        Extracted text string
    """
    try:
        # Load image
        if isinstance(image_file, str):
            image = Image.open(image_file)
        else:
            image = Image.open(io.BytesIO(image_file.read()))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract text
        text = pytesseract.image_to_string(image)
        
        return text
    except pytesseract.TesseractNotFoundError:
        raise Exception("Tesseract OCR is not installed. Please install Tesseract to use OCR features.")
    except Exception as e:
        raise Exception(f"OCR processing error: {str(e)}")

def clean_text(text):
    """
    Clean and normalize extracted text
    
    Args:
        text: Raw text from OCR
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep commas and periods
    text = re.sub(r'[^\w\s,.]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def parse_ingredients(text):
    """
    Parse ingredient list from text
    
    Args:
        text: Cleaned text from OCR
    
    Returns:
        List of ingredient names
    """
    # Common ingredient keywords
    ingredient_keywords = [
        'ingredients:', 'contains:', 'made with:',
        'allergens:', 'nutrition facts'
    ]
    
    # Find ingredient section
    text_lower = text.lower()
    start_idx = -1
    
    for keyword in ingredient_keywords:
        idx = text_lower.find(keyword)
        if idx != -1:
            start_idx = idx + len(keyword)
            break
    
    if start_idx == -1:
        # No keyword found, use entire text
        ingredient_text = text
    else:
        # Find end of ingredient list (usually at nutrition facts or allergens)
        end_keywords = ['nutrition facts', 'allergens', 'net weight', 'serving size']
        end_idx = len(text)
        
        for keyword in end_keywords:
            idx = text_lower.find(keyword, start_idx)
            if idx != -1 and idx < end_idx:
                end_idx = idx
        
        ingredient_text = text[start_idx:end_idx]
    
    # Split by common separators
    ingredients = re.split(r'[,;]', ingredient_text)
    
    # Clean each ingredient
    cleaned_ingredients = []
    for ingredient in ingredients:
        ingredient = ingredient.strip()
        
        # Remove parenthetical information
        ingredient = re.sub(r'\([^)]*\)', '', ingredient)
        
        # Remove percentages
        ingredient = re.sub(r'\d+%', '', ingredient)
        
        # Remove numbers and periods at start
        ingredient = re.sub(r'^[\d.]+\s*', '', ingredient)
        
        ingredient = ingredient.strip()
        
        # Only keep non-empty ingredients with at least 2 characters
        if len(ingredient) >= 2:
            cleaned_ingredients.append(ingredient)
    
    return cleaned_ingredients

def process_packaged_food_image(image_file):
    """
    Complete OCR pipeline for packaged food images
    
    Args:
        image_file: File object or path to image
    
    Returns:
        Dictionary with extracted text and parsed ingredients
    """
    # Extract text
    raw_text = extract_text_from_image(image_file)
    
    # Clean text
    cleaned_text = clean_text(raw_text)
    
    # Parse ingredients
    ingredients = parse_ingredients(cleaned_text)
    
    return {
        'raw_text': raw_text,
        'cleaned_text': cleaned_text,
        'ingredients': ingredients
    }
