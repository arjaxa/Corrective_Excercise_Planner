import numpy as np
import tensorflow as tf
from pathlib import Path
from sklearn.metrics import confusion_matrix, classification_report


ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data" / "posture_images" / "validation"
MODEL_PATH = ROOT_DIR / "models" / "posture_classifier.keras"

IMAGE_SIZE = (160, 160)
BATCH_SIZE = 4
SEED = 42


print("=" * 60)
print("POSTURE CLASSIFIER - MODEL EVALUATION")
print("=" * 60)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

class_names = val_ds.class_names

print("\nClasses:")
for i, name in enumerate(class_names):
    print(f"{i}: {name}")


print("\nLoading model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")


print("\nGenerating predictions...")

y_true = []
y_pred = []

for images, labels in val_ds:

    predictions = model.predict(
        images,
        verbose=0
    )

    predicted_classes = np.argmax(
        predictions,
        axis=1
    )

    y_true.extend(labels.numpy())
    y_pred.extend(predicted_classes)

y_true = np.array(y_true)
y_pred = np.array(y_pred)


print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        zero_division=0
    )
)



cm = confusion_matrix(
    y_true,
    y_pred
)

print("\n" + "=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

print("\nRows = Actual")
print("Columns = Predicted\n")

print("                 " + "  ".join(
    f"{name[:8]:>8}" for name in class_names
))

for i, row in enumerate(cm):

    print(
        f"{class_names[i][:15]:<15}"
        + "  "
        + "  ".join(f"{value:8}" for value in row)
    )


accuracy = np.mean(
    y_true == y_pred
)

print("\n" + "=" * 60)
print(f"Overall validation accuracy: {accuracy:.2%}")
print("=" * 60)