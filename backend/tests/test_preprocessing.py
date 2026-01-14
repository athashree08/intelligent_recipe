import pytest
import sys
import os
import numpy as np
from PIL import Image

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.image_preprocessing import (
    resize_image,
    convert_to_rgb,
    normalize_for_mobilenet,
    prepare_image_tensor
)

def test_resize_image():
    """Test image resizing"""
    # Create a test image
    img = Image.new('RGB', (500, 500), color='red')
    
    # Resize
    resized = resize_image(img, target_size=(224, 224))
    
    assert resized.size == (224, 224)

def test_convert_to_rgb():
    """Test RGB conversion"""
    # Create grayscale image
    img = Image.new('L', (100, 100), color=128)
    
    # Convert to RGB
    rgb_img = convert_to_rgb(img)
    
    assert rgb_img.mode == 'RGB'

def test_normalize_for_mobilenet():
    """Test MobileNet normalization"""
    # Create random image array
    img_array = np.random.randint(0, 255, (1, 224, 224, 3), dtype=np.uint8)
    
    # Normalize
    normalized = normalize_for_mobilenet(img_array.astype(np.float32))
    
    # Check that values are in expected range [-1, 1]
    assert normalized.min() >= -1.0
    assert normalized.max() <= 1.0

def test_prepare_image_tensor_shape():
    """Test complete preprocessing pipeline output shape"""
    # Create test image
    img = Image.new('RGB', (500, 500), color='blue')
    
    # Save to temporary file
    temp_path = 'test_temp_image.jpg'
    img.save(temp_path)
    
    try:
        # Prepare tensor
        tensor = prepare_image_tensor(temp_path)
        
        # Check shape
        assert tensor.shape == (1, 224, 224, 3)
        
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
