import os
import shutil
import random

source_dir = "cleaned_batch"
split_dir = "dataset_split"

categories = ["SAFE", "HARD_NEG", "VIOLENCE"]

train_ratio = 0.8

for cat in categories:

    imgs = os.listdir(os.path.join(source_dir, cat))
    random.shuffle(imgs)

    train_size = int(len(imgs) * train_ratio)

    train_imgs = imgs[:train_size]
    val_imgs = imgs[train_size:]

    # Create folders
    os.makedirs(f"{split_dir}/train/{cat}", exist_ok=True)
    os.makedirs(f"{split_dir}/val/{cat}", exist_ok=True)

    # Copy train
    for img in train_imgs:
        shutil.copy(
            os.path.join(source_dir, cat, img),
            f"{split_dir}/train/{cat}/{img}"
        )

    # Copy val
    for img in val_imgs:
        shutil.copy(
            os.path.join(source_dir, cat, img),
            f"{split_dir}/val/{cat}/{img}"
        )

print(" Train/Val split done")