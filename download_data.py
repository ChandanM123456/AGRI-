import os
import zipfile

datasets = [
    "atharvaingle/crop-recommendation-dataset",
    "vbookshelf/soil-types-image-classification",
    "prasoonkottarathil/indian-agriculture-data"
]

for d in datasets:
    print(f"Downloading {d}...")
    os.system(f"kaggle datasets download -d {d}")

for file in os.listdir():
    if file.endswith(".zip"):
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(file.replace(".zip",""))

print("✅ All datasets downloaded!")