from pathlib import Path
import random
import shutil

ROOT_DIR = Path(__file__).resolve().parent.parent

SOURCE_DIR = ROOT_DIR / "data" / "posture_images"
TRAIN_DIR = SOURCE_DIR / "train"
VAL_DIR = SOURCE_DIR / "validation"

CLASSES = [
    "normal",
    "forward_head",
    "upper_crossed_syndrome",
    "lower_crossed_syndrome",
]

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


if TRAIN_DIR.exists() or VAL_DIR.exists():
    existing_files = list(TRAIN_DIR.rglob("*")) if TRAIN_DIR.exists() else []
    existing_files += list(VAL_DIR.rglob("*")) if VAL_DIR.exists() else []

    if any(f.is_file() for f in existing_files):
        print("ERROR: train/validation folders already contain files.")
        print("Nothing was changed.")
        raise SystemExit

random.seed(42)

print("=" * 60)
print("POSTURE DATASET SPLIT")
print("=" * 60)

for class_name in CLASSES:
    source_class = SOURCE_DIR / class_name
    train_class = TRAIN_DIR / class_name
    val_class = VAL_DIR / class_name

    files = [
        f for f in source_class.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]

    random.shuffle(files)

    val_count = max(1, round(len(files) * 0.2))

    val_files = files[:val_count]
    train_files = files[val_count:]

    train_class.mkdir(parents=True, exist_ok=True)
    val_class.mkdir(parents=True, exist_ok=True)

    for file in train_files:
        shutil.copy2(file, train_class / file.name)

    for file in val_files:
        shutil.copy2(file, val_class / file.name)

    print(
        f"{class_name}: "
        f"{len(train_files)} train / {len(val_files)} validation"
    )

print("=" * 60)
print("DONE")
print("Original images were NOT moved or deleted.")
print("=" * 60)