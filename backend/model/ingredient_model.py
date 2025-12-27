from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    decode_predictions
)

model = MobileNetV2(weights="imagenet")

def predict_ingredients(image_tensor, top_k=5):
    preds = model.predict(image_tensor)
    decoded = decode_predictions(preds, top=top_k)[0]

    return [
        {
            "name": label.lower(),
            "confidence": round(float(confidence), 3)
        }
        for _, label, confidence in decoded
    ]
