import cv2
import os
import numpy as np

# INPUT ROOT
input_root = "current_batch"

# OUTPUT ROOT
output_root = "cleaned_batch"

# Classes (folders)
categories = ["SAFE", "HARD_NEG", "VIOLENCE"]

for category in categories:

    input_folder = os.path.join(input_root, category)
    output_folder = os.path.join(output_root, category)

    os.makedirs(output_folder, exist_ok=True)

    print(f"\nProcessing {category}...")

    for img_name in os.listdir(input_folder):

        img_path = os.path.join(input_folder, img_name)
        img = cv2.imread(img_path)

        if img is None:
            print(f"Skipping {img_name}")
            continue

    
        img = cv2.resize(img, (224, 224))

    
        img = cv2.convertScaleAbs(img, alpha=1.02, beta=2)

    
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        img = cv2.filter2D(img, -1, kernel)

        # SAVE
        save_path = os.path.join(output_folder, img_name)
        cv2.imwrite(save_path, img)

        print(f"{category} -> {img_name} processed")

print("\n ALL IMAGES PROCESSED SUCCESSFULLY")