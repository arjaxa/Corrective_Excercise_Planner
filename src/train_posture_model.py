import tensorflow as tf
from tensorflow.keras import layers, models
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data" / "posture_images"
MODEL_DIR = ROOT_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

IMAGE_SIZE = (160, 160)
BATCH_SIZE = 4
SEED = 42


print("=" * 60)
print("POSTURE CLASSIFIER - DATASET")
print("=" * 60)

TRAIN_DIR = ROOT_DIR / "data" / "posture_images" / "train"
VAL_DIR = ROOT_DIR / "data" / "posture_images" / "validation"

train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=42
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

print("\nNumber of classes:", len(class_names))


AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)



data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.10),
], name="data_augmentation")


base_model = tf.keras.applications.MobileNetV2(
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
    len(class_names),
    activation="softmax"
)(x)

model = models.Model(inputs, outputs)



model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()


print("\n" + "=" * 60)
print("TRAINING")
print("=" * 60)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    MODEL_DIR / "posture_classifier.keras",
    monitor="val_loss",
    save_best_only=True
)

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=25,
    callbacks=[
        early_stopping,
        checkpoint
    ]
)


print("\n" + "=" * 60)
print("FINAL EVALUATION")
print("=" * 60)

loss, accuracy = model.evaluate(val_ds)

print(f"\nValidation loss: {loss:.4f}")
print(f"Validation accuracy: {accuracy:.4f}")

print("\nModel saved to:")
print(MODEL_DIR / "posture_classifier.keras")

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)