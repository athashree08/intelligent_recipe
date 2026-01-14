import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.ingredient_recognition import IngredientRecognitionModel

def train_subset_model(data_dir='data/ingredients_subset', epochs=40, batch_size=32):
    """
    Train on ingredient subset for high accuracy in short time
    
    Target: 85-90% accuracy in 1-2 hours
    """
    
    print("=" * 60)
    print("FAST TRAINING: Ingredient Subset")
    print("=" * 60)
    
    # Count classes
    class_names = sorted([d for d in os.listdir(data_dir) 
                         if os.path.isdir(os.path.join(data_dir, d))])
    num_classes = len(class_names)
    
    print(f"\nTraining on {num_classes} ingredients:")
    total_images = 0
    for i, name in enumerate(class_names):
        num_images = len([f for f in os.listdir(os.path.join(data_dir, name))
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        total_images += num_images
        print(f"  {i+1:2}. {name:15} : {num_images:4} images")
    
    print(f"\nTotal images: {total_images}")
    print(f"Average per class: {total_images // num_classes}")
    
    # Enhanced data augmentation for better generalization
    train_datagen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,
        rotation_range=40,
        width_shift_range=0.3,
        height_shift_range=0.3,
        shear_range=0.2,
        zoom_range=0.3,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest',
        validation_split=0.2
    )
    
    # Generators
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    validation_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    # Create model
    print("\nBuilding MobileNetV2 model...")
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
        monitor='val_accuracy',
        patience=7,  # More patience for subset
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )
    
    # Phase 1: Train top layers (15 epochs)
    print("\n" + "=" * 60)
    print("PHASE 1: Training top layers (base frozen)")
    print("=" * 60)
    
    history1 = model.model.fit(
        train_generator,
        epochs=15,
        validation_data=validation_generator,
        callbacks=[checkpoint, early_stopping, reduce_lr]
    )
    
    # Phase 2: Fine-tune (25 more epochs)
    print("\n" + "=" * 60)
    print("PHASE 2: Fine-tuning (unfreezing last 30 layers)")
    print("=" * 60)
    
    model.unfreeze_base_layers(num_layers=30)  # More layers for subset
    
    # Reset early stopping for phase 2
    early_stopping_phase2 = EarlyStopping(
        monitor='val_accuracy',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    history2 = model.model.fit(
        train_generator,
        epochs=epochs - 15,
        validation_data=validation_generator,
        callbacks=[checkpoint, early_stopping_phase2, reduce_lr]
    )
    
    # Save final model
    model.save_model('models/ingredient_model.h5')
    
    # Save class names
    with open('models/class_names.txt', 'w') as f:
        for name in class_names:
            f.write(f"{name}\n")
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    print(f"Model saved to: models/ingredient_model.h5")
    print(f"Best model saved to: models/ingredient_model_best.h5")
    print(f"Class names saved to: models/class_names.txt")
    
    # Final evaluation
    print("\nFinal evaluation on validation set:")
    val_loss, val_accuracy = model.model.evaluate(validation_generator)
    print(f"Validation Loss: {val_loss:.4f}")
    print(f"Validation Accuracy: {val_accuracy*100:.2f}%")
    
    if val_accuracy >= 0.85:
        print("\n🎉 SUCCESS! Achieved 85%+ accuracy!")
        print("Your model is ready for deployment!")
    elif val_accuracy >= 0.80:
        print("\n✅ Good! Achieved 80%+ accuracy!")
        print("Consider training a bit longer for even better results.")
    else:
        print(f"\n⚠️  Accuracy: {val_accuracy*100:.1f}%")
        print("Consider training for more epochs.")
    
    return model, val_accuracy

if __name__ == '__main__':
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Check if subset exists
    if not os.path.exists('data/ingredients_subset'):
        print("Error: Subset not found!")
        print("Run: python create_subset.py first")
        sys.exit(1)
    
    # Train on subset
    print("\nStarting training...")
    print("This will take approximately 1-2 hours")
    print("Press Ctrl+C to stop\n")
    
    model, accuracy = train_subset_model(epochs=40, batch_size=32)
    
    print("\n" + "=" * 60)
    print(f"Final Model Accuracy: {accuracy*100:.2f}%")
    print("=" * 60)
