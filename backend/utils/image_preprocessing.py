import numpy as np
from PIL import Image
import io

def resize_image(image, target_size=(224, 224)):
    """
    Resize image to target size
    
    Args:
        image: PIL Image object
        target_size: Tuple of (width, height)
    
    Returns:
        Resized PIL Image
    """
    return image.resize(target_size, Image.Resampling.LANCZOS)

def convert_to_rgb(image):
    """
    Convert image to RGB format
    
    Args:
        image: PIL Image object
    
    Returns:
        RGB PIL Image
    """
    if image.mode != 'RGB':
        return image.convert('RGB')
    return image

def normalize_for_mobilenet(image_array):
    """
    Normalize image array for MobileNet preprocessing
    Uses MobileNetV2 preprocessing: scale to [-1, 1]
    
    Args:
        image_array: numpy array of image
    
    Returns:
        Normalized numpy array
    """
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    return preprocess_input(image_array)

def prepare_image_tensor(image_file, target_size=(224, 224)):
    """
    Complete preprocessing pipeline: resize, convert to RGB, normalize
    
    Args:
        image_file: File object or path to image
        target_size: Target size for resizing
    
    Returns:
        Model-ready numpy array tensor
    """
    # Load image
    if isinstance(image_file, str):
        image = Image.open(image_file)
    else:
        image = Image.open(io.BytesIO(image_file.read()))
    
    # Preprocessing steps
    image = convert_to_rgb(image)
    image = resize_image(image, target_size)
    
    # Convert to array
    image_array = np.array(image)
    
    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    
    # Normalize
    image_array = normalize_for_mobilenet(image_array)
    
    return image_array

def preprocess_image_for_display(image_file):
    """
    Preprocess image for display purposes (without normalization)
    
    Args:
        image_file: File object or path to image
    
    Returns:
        PIL Image object
    """
    if isinstance(image_file, str):
        image = Image.open(image_file)
    else:
        image = Image.open(io.BytesIO(image_file.read()))
    
    image = convert_to_rgb(image)
    return image
