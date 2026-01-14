import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.ingredient_recognition import IngredientRecognitionModel

def train_model(data_dir, epochs=50, batch_size=32, validation_split=0.2):
    """
    Train the ingredient recognition model using transfer learning
    
    Args:
        data_dir: Directory containing training data (folder-based labels)
                  Structure: data_dir/class_name/image.jpg
        epochs: Number of training epochs
        batch_size: Batch size for training
        validation_split: Fraction of data for validation
    """
    
    print("=" * 50)
    print("INGREDIENT RECOGNITION MODEL TRAINING")
    print("=" * 50)
    
    # Count number of classes
    class_names = sorted([d for d in os.listdir(data_dir) 
                         if os.path.isdir(os.path.join(data_dir, d))])
    num_classes = len(class_names)
    
    print(f"\nFound {num_classes} ingredient classes:")
    for i, name in enumerate(class_names):
        num_images = len(os.listdir(os.path.join(data_dir, name)))
        print(f"  {i+1}. {name}: {num_images} images")
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        validation_split=validation_split
    )
    
    # Training data generator
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )
    
    # Validation data generator
    validation_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )
    
    # Create model
    print("\nBuilding model...")
    model = IngredientRecognitionModel(num_classes=num_classes)
    model.class_names = class_names
    
    # Callbacks
    checkpoint = ModelCheckpoint(
        'models/ingredient_model_best.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )
    
    # Phase 1: Train only top layers
    print("\n" + "=" * 50)
    print("PHASE 1: Training top layers (base frozen)")
    print("=" * 50)
    
    history1 = model.model.fit(
        train_generator,
        epochs=10,
        validation_data=validation_generator,
        callbacks=[checkpoint, early_stopping, reduce_lr]
    )
    
    # Phase 2: Fine-tune last layers
    print("\n" + "=" * 50)
    print("PHASE 2: Fine-tuning (unfreezing last 20 layers)")
    print("=" * 50)
    
    model.unfreeze_base_layers(num_layers=20)
    
    history2 = model.model.fit(
        train_generator,
        epochs=epochs - 10,
        validation_data=validation_generator,
        callbacks=[checkpoint, early_stopping, reduce_lr]
    )
    
    # Save final model
    model.save_model('models/ingredient_model.h5')
    
    # Save class names
    with open('models/class_names.txt', 'w') as f:
        for name in class_names:
            f.write(f"{name}\n")
    
    print("\n" + "=" * 50)
    print("TRAINING COMPLETE")
    print("=" * 50)
    print(f"Model saved to: models/ingredient_model.h5")
    print(f"Best model saved to: models/ingredient_model_best.h5")
    print(f"Class names saved to: models/class_names.txt")
    
    # Evaluate on validation set
    print("\nFinal evaluation on validation set:")
    val_loss, val_accuracy = model.model.evaluate(validation_generator)
    print(f"Validation Loss: {val_loss:.4f}")
    print(f"Validation Accuracy: {val_accuracy:.4f}")

if __name__ == '__main__':
    # Default data directory
    data_directory = 'data/ingredients'
    
    if not os.path.exists(data_directory):
        print(f"Error: Data directory '{data_directory}' not found!")
        print("\nPlease organize your training data as follows:")
        print("  data/ingredients/")
        print("    ├── tomato/")
        print("    │   ├── img1.jpg")
        print("    │   └── img2.jpg")
        print("    ├── onion/")
        print("    │   ├── img1.jpg")
        print("    │   └── img2.jpg")
        print("    └── ...")
        sys.exit(1)
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Train model
    train_model(data_directory, epochs=50, batch_size=32)
