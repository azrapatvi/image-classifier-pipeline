# image-content-moderation

**AI-powered image content moderation pipeline using EfficientNetB0**

---

## Overview

This is a deep learning project aimed at building an automated image content moderation system. This repository contains the work done for a **mini model training pipeline** built to understand the full workflow from raw image scraping all the way through cleaning, preprocessing, model training, and evaluation. The goal of this run was not accuracy but a complete, functional end-to-end understanding of the architecture using a small 3-class dataset.

---

## Repository Structure

```
image-content-moderation/
│
├── downloads_temp/               # Raw scraped images (before cleaning)
│
├── current_batch/
│   ├── SAFE/                     # Accepted SAFE images after manual review
│   ├── HARD_NEG/                 # Accepted HARD_NEG images after manual review
│   └── VIOLENCE/                 # Accepted VIOLENCE images after manual review
│
├── cleaned_batch/
│   ├── SAFE/                     # Preprocessed SAFE images (224x224)
│   ├── HARD_NEG/                 # Preprocessed HARD_NEG images (224x224)
│   └── VIOLENCE/                 # Preprocessed VIOLENCE images (224x224)
│
├── logs/
│   └── rejection_log.txt         # Auto-generated log of all rejected images with reasons
│
├── scrape.ipynb                  # Unsplash API scraping notebook
├── manual_cleaning.py            # Streamlit-based manual image review and cleaning tool
├── image_processing.py           # OpenCV preprocessing script (resize, brightness, sharpen)
├── efficientnet.ipynb            # EfficientNetB0 training and evaluation notebook
├── create_local_structure.py     # Script to create the full folder structure locally
└── README.md
```

---

## Dataset

Images were scraped from the **Unsplash Official REST API** using three keyword groups — one per class. A total of 90 images were downloaded and 25 were rejected during manual cleaning, leaving a final dataset of 65 images.

| Category   | Downloaded | Rejected | Final Count |
|------------|------------|----------|-------------|
| SAFE       | 30         | 11       | 19          |
| HARD_NEG   | 30         | 8        | 22          |
| VIOLENCE   | 30         | 6        | 24          |
| **Total**  | **90**     | **25**   | **65**      |

**Keywords used:**
- SAFE → `people walking`
- HARD_NEG → `holi`
- VIOLENCE → `accident crash`

---

## Pipeline

### 1. Scraping — `scrape.ipynb`

Images are downloaded using the Unsplash REST API with a personal Client-ID key. The script sends GET requests to `https://api.unsplash.com/search/photos` for each keyword with `per_page=30` and saves the binary image content to `downloads_temp/` as `img1.jpg`, `img2.jpg`, etc. Each image is fetched from `img['urls']['small']` and saved with exception handling so one failure does not interrupt the loop.

### 2. Manual Cleaning — `manual_cleaning.py`

A Streamlit-based review tool that displays each image from `downloads_temp/` one at a time. The reviewer either assigns the image to SAFE, HARD_NEG, or VIOLENCE using the corresponding button, or rejects it with a selected reason. The tool automatically renames accepted images in the format `safe_N.jpg`, `hard_N.jpg`, `violence_N.jpg` and copies them to the appropriate `current_batch/` folder. Rejections are logged to `logs/rejection_log.txt` in the format `filename.jpg -> Reason`. The tool stops automatically once 75 images have been accepted.

**Rejection reasons available:** Blurry, Duplicate, Low Quality, Irrelevant, Meme

### 3. Preprocessing — `image_processing.py`

After cleaning, all images in `current_batch/` are processed using OpenCV and saved to `cleaned_batch/`. Three operations are applied in sequence:

- **Resize** to 224×224 pixels using `cv2.resize()` — standard input size for CNNs
- **Brightness and contrast normalization** using `cv2.convertScaleAbs(alpha=1.02, beta=2)` — mild boost without over-saturation
- **Edge sharpening** using a 3×3 kernel via `cv2.filter2D()` — enhances clarity and fine detail

Corrupted or unreadable files are automatically skipped via an `img is None` check.

### 4. Model Training — `efficientnet.ipynb`

The preprocessed dataset in `cleaned_batch/` is organized into `train/` and `val/` splits and fed into an **EfficientNetB0** model built with TensorFlow/Keras. Key configuration:

- **Input size:** 224×224
- **Batch size:** 32
- **Classes:** 3 (SAFE, HARD_NEG, VIOLENCE)
- **Data loading:** `ImageDataGenerator` with `rescale=1./255`
- **Callbacks:** `EarlyStopping(patience=2, restore_best_weights=True)`
- **Evaluation:** Classification report, confusion matrix, accuracy and loss curves

---

## Requirements

```
tensorflow
keras
opencv-python
numpy
streamlit
scikit-learn
matplotlib
requests
Pillow
```

Install all dependencies:

```bash
pip install tensorflow opencv-python numpy streamlit scikit-learn matplotlib requests Pillow
```

---

## How to Run

**Step 1 — Create folder structure:**
```bash
python create_local_structure.py
```

**Step 2 — Scrape images:**

Open `scrape.ipynb` in Jupyter or Google Colab and run all cells. Images will be saved to `downloads_temp/`.

**Step 3 — Manual cleaning:**
```bash
streamlit run manual_cleaning.py
```

Review each image in the browser, assign category or reject with a reason. Stop when 75 images are accepted.

**Step 4 — Preprocess images:**
```bash
python image_processing.py
```

All accepted images will be resized, brightness-adjusted, and sharpened into `cleaned_batch/`.

**Step 5 — Train and evaluate the model:**

Open `efficientnet.ipynb` in Google Colab, upload `cleaned_batch/` as a zip, and run all cells.

---

## Notes

This repository is a **practice run** built for pipeline understanding. Accuracy is not the goal at this stage. The dataset size (65 images) is intentionally small and not representative of production-scale training. EfficientNetB0 is the final architecture planned for the full system — only the dataset size and scope change in the real run.

---

## Categories

| Label      | Description                                                                 |
|------------|-----------------------------------------------------------------------------|
| SAFE       | Clean, non-harmful content — everyday people, activities, nature            |
| HARD_NEG   | Visually intense but not explicitly harmful — crowds, festivals, edge cases |
| VIOLENCE   | Depicts accidents, crashes, or other violent/harmful real-world situations  |

---

