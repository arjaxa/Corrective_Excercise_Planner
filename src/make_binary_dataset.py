from pathlib import Path
import shutil

ROOT_DIR = Path(__file__).resolve().parent.parent

SOURCE_DIR = ROOT_DIR / "data" / "posture_images"
BINARY_DIR = ROOT_DIR / "data" / "binary_posture_images"

NORMAL_SOURCE = SOURCE_DIR / "normal"

DEVIATION_CLASSES = [
    "forward_head",
    "upper_crossed_syndrome",
    "lower_crossed_syndrome",
]

if BINARY_DIR.exists() and any(BINARY_DIR.rglob("*")):
    print("ERROR: binary_posture_images already contains files.")
    print("Nothing was changed.")
    raise SystemExit

normal_dest = BINARY_DIR / "normal"
deviation_dest = BINARY_DIR / "postural_deviation"

normal_dest.mkdir(parents=True, exist_ok=True)
deviation_dest.mkdir(parents=True, exist_ok=True)

extensions = {".jpg", ".jpeg", ".png", ".webp"}

normal_files = [
    f for f in NORMAL_SOURCE.iterdir()
    if f.is_file() and f.suffix.lower() in extensions
]

for file in normal_files:
    shutil.copy2(file, normal_dest / file.name)

deviation_count = 0

for class_name in DEVIATION_CLASSES:
    source_class = SOURCE_DIR / class_name

    for file in source_class.iterdir():
        if file.is_file() and file.suffix.lower() in extensions:
            destination = deviation_dest / f"{class_name}_{file.name}"
            shutil.copy2(file, destination)
            deviation_count += 1

print("=" * 60)
print("BINARY POSTURE DATASET CREATED")
print("=" * 60)
print(f"Normal: {len(normal_files)}")
print(f"Postural deviation: {deviation_count}")
print(f"Total: {len(normal_files) + deviation_count}")
print("=" * 60)
print("Original images were NOT changed.")