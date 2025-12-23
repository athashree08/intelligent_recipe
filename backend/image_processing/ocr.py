import pytesseract

def extract_text(image):
    try:
        text = pytesseract.image_to_string(image)
        return text.strip()
    except:
        return ""
