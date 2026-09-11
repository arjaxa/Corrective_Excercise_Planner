from pathlib import Path

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint



ROOT_DIR = Path(__file__).resolve().parent.parent

TRAIN_DIR = ROOT_DIR / "data" / "binary_posture_images" / "train"
VAL_DIR = ROOT_DIR / "data" / "binary_posture_images" / "validation"
MODEL_PATH = ROOT_DIR / "models" / "binary_posture_classifier.keras"



IMAGE_SIZE = (160, 160)
BATCH_SIZE = 4
EPOCHS = 25
SEED = 42

print("=" * 60)
print("BINARY POSTURE CLASSIFIER - DATASET")
print("=" * 60)



train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=SEED
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

class_names = train_ds.class_names

print("\nClasses:")
for i, name in enumerate(class_names):
    print(f"{i}: {name}")

print(f"\nNumber of classes: {len(class_names)}")


data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.10),
])


base_model = MobileNetV2(
    input_shape=(160, 160, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False


inputs = layers.Input(shape=(160, 160, 3))

x = data_augmentation(inputs)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.25)(x)

outputs = layers.Dense(
    1,
    activation="sigmoid"
)(x)

model = models.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()


early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    MODEL_PATH,
    monitor="val_loss",
    save_best_only=True
)



print("\n" + "=" * 60)
print("TRAINING")
print("=" * 60)

class_weight = {
    0: 56 / (2 * 26),
    1: 26 / (2 * 56)
}

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    class_weight=class_weight,
    callbacks=[
        early_stopping,
        checkpoint
    ]
)



print("\n" + "=" * 60)
print("FINAL EVALUATION")
print("=" * 60)

val_loss, val_accuracy = model.evaluate(val_ds)

print(f"\nValidation loss: {val_loss:.4f}")
print(f"Validation accuracy: {val_accuracy:.4f}")

print("\nModel saved to:")
print(MODEL_PATH)

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)