import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
import numpy as np
import os

class IngredientRecognitionModel:
    def __init__(self, num_classes=20, model_path=None):
        """
        Initialize the ingredient recognition model
        
        Args:
            num_classes: Number of ingredient classes
            model_path: Path to saved model (if loading existing model)
        """
        self.num_classes = num_classes
        self.model_path = model_path
        self.model = None
        self.class_names = []
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self.build_model()
    
    def build_model(self):
        """
        Build MobileNetV2 model with transfer learning
        """
        # Load pre-trained MobileNetV2
        self.base_model = MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model layers
        self.base_model.trainable = False
        
        # Add custom classification layers
        x = self.base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.5)(x)
        predictions = Dense(self.num_classes, activation='softmax')(x)
        
        # Create final model
        self.model = Model(inputs=self.base_model.input, outputs=predictions)
        
        # Compile model
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def unfreeze_base_layers(self, num_layers=20):
        """
        Unfreeze last N layers of base model for fine-tuning
        
        Args:
            num_layers: Number of layers to unfreeze from the end
        """
        if not hasattr(self, 'base_model') or self.base_model is None:
            print("Warning: Base model not found. Cannot perform fine-tuning.")
            return
        
        print(f"Unfreezing last {num_layers} layers of base model...")
        self.base_model.trainable = True
        
        # Freeze all layers except the last num_layers
        for layer in self.base_model.layers[:-num_layers]:
            layer.trainable = False
        
        # Count trainable layers
        trainable_count = sum([1 for layer in self.base_model.layers if layer.trainable])
        print(f"Trainable layers in base model: {trainable_count}/{len(self.base_model.layers)}")
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def predict(self, image_tensor, top_k=3):
        """
        Predict ingredients from image tensor
        
        Args:
            image_tensor: Preprocessed image tensor
            top_k: Number of top predictions to return
        
        Returns:
            List of tuples (class_name, confidence)
        """
        if self.model is None:
            raise ValueError("Model not loaded or built")
        
        predictions = self.model.predict(image_tensor)
        top_indices = np.argsort(predictions[0])[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            class_name = self.class_names[idx] if idx < len(self.class_names) else f"class_{idx}"
            confidence = float(predictions[0][idx])
            results.append({
                'name': class_name,
                'confidence': confidence
            })
        
        return results
    
    def save_model(self, path):
        """Save model to file"""
        if self.model:
            self.model.save(path)
            print(f"Model saved to {path}")
    
    def load_model(self, path):
        """Load model from file"""
        self.model = load_model(path)
        print(f"Model loaded from {path}")
        
        # Try to load class names
        class_names_path = os.path.join(os.path.dirname(path), 'class_names.txt')
        if os.path.exists(class_names_path):
            with open(class_names_path, 'r') as f:
                self.class_names = [line.strip() for line in f if line.strip()]
            print(f"Loaded {len(self.class_names)} class names")

# Global model instance (lazy loading)
_model_instance = None

def get_model(model_path='models/ingredient_model.h5'):
    """
    Get or create model instance (singleton pattern)
    """
    global _model_instance
    if _model_instance is None:
        _model_instance = IngredientRecognitionModel(model_path=model_path)
    return _model_instance

def predict_ingredients(image_tensor, top_k=3):
    """
    Predict ingredients from preprocessed image tensor
    
    Args:
        image_tensor: Preprocessed image tensor
        top_k: Number of top predictions
    
    Returns:
        List of ingredient predictions
    """
    model = get_model()
    return model.predict(image_tensor, top_k=top_k)
