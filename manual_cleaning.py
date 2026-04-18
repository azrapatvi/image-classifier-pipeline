import streamlit as st
import os
import shutil
import random

# FOLDERS
base_dir = 'downloads_temp/'
safe_dir = 'current_batch/SAFE'
hard_negative_dir = 'current_batch/HARD_NEG'
violence_dir = 'current_batch/VIOLENCE'


valid_ext = (".jpg", ".jpeg", ".png")

# LOAD IMAGES
images = [img for img in os.listdir(base_dir) if img.lower().endswith(valid_ext)]

# SHUFFLE ONCE
if "shuffled" not in st.session_state:
    random.shuffle(images)
    st.session_state.shuffled = True

# SESSION STATE
if "index" not in st.session_state:
    st.session_state.index = 0

if "accepted_count" not in st.session_state:
    st.session_state.accepted_count = 0

if "safe_count" not in st.session_state:
    st.session_state.safe_count = 0

if "hard_negative_count" not in st.session_state:
    st.session_state.hard_negative_count = 0

if "violence_count" not in st.session_state:
    st.session_state.violence_count = 0

# STOP CONDITIONS
if st.session_state.accepted_count >= 75:
    st.success("100 images collected!")
    st.stop()

if st.session_state.index >= len(images):
    st.warning("All images reviewed!")
    st.stop()

# CURRENT IMAGE
current_img = images[st.session_state.index]
img_path = os.path.join(base_dir, current_img)

# DISPLAY COUNTS
st.write(f"Total Accepted: {st.session_state.accepted_count}/75")
st.write(f"SAFE: {st.session_state.safe_count}")
st.write(f"HARD NEGATIVE: {st.session_state.hard_negative_count}")
st.write(f"VIOLENCE: {st.session_state.violence_count}")

# SHOW IMAGE
st.write("Image:", current_img)
st.image(img_path)

# -------- BUTTONS -------- #

# SAFE
if st.button("KEEP SAFE"):
    new_name = f"safe_{st.session_state.safe_count + 1}.jpg"

    shutil.copy(img_path, os.path.join(safe_dir, new_name))

    st.session_state.safe_count += 1
    st.session_state.accepted_count += 1
    st.session_state.index += 1
    st.rerun()

# HARD NEGATIVE
if st.button("KEEP HARD NEGATIVE"):
    new_name = f"hard_{st.session_state.hard_negative_count + 1}.jpg"

    shutil.copy(img_path, os.path.join(hard_negative_dir, new_name))

    st.session_state.hard_negative_count += 1
    st.session_state.accepted_count += 1
    st.session_state.index += 1
    st.rerun()

# VIOLENCE
if st.button("KEEP VIOLENCE"):
    new_name = f"violence_{st.session_state.violence_count + 1}.jpg"

    shutil.copy(img_path, os.path.join(violence_dir, new_name))

    st.session_state.violence_count += 1
    st.session_state.accepted_count += 1
    st.session_state.index += 1
    st.rerun()

# -------- REJECT -------- #

if "reason_select" not in st.session_state:
    st.session_state.reason_select = "-- Select reason --"

reason = st.selectbox(
    "Select reason",
    ["-- Select reason --", "Blurry", "Duplicate", "Low Quality", "Irrelevant", "Meme"],
    key="reason_select"
)

if st.button("REJECT"):

    if reason == "-- Select reason --":
        st.warning("Please select a reason first!")

    else:
        with open("logs/rejection_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{current_img} -> {reason}\n")

        st.session_state.index += 1

        del st.session_state["reason_select"]

        st.rerun()