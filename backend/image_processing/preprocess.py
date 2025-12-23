import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

def preprocess_image(image):
    image = image.resize((224, 224))
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array
