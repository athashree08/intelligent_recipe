import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

base_model = MobileNetV2(weights="imagenet", include_top=False)

x = base_model.output
x = GlobalAveragePooling2D()(x)
predictions = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base_model.input, outputs=predictions)

LABELS = ["Tomato"]

def predict_ingredient(img):
    pred = model.predict(img)[0][0]
    ingredient = LABELS[0] if pred > 0.5 else "Unknown"
    confidence = pred if pred > 0.5 else 1 - pred
    return ingredient, float(confidence)
