import cv2
import numpy as np
import streamlit as st
from PIL import Image

# ---------------------------
# Helper Functions
# ---------------------------
def detect_face(image):
    # ✅ Convert RGB → BGR (IMPORTANT FIX)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,   # 🔥 more sensitive
        minNeighbors=4,    # 🔥 detects more faces
        minSize=(30, 30)
    )

    return faces


def get_skin_tone(image, face):
    x, y, w, h = face
    face_region = image[y:y+h, x:x+w]

    avg_color = np.mean(face_region, axis=(0, 1))
    brightness = np.mean(avg_color)

    if brightness > 180:
        return "Fair"
    elif brightness > 130:
        return "Medium"
    else:
        return "Dark"


def get_face_shape(face):
    x, y, w, h = face
    ratio = w / h

    if ratio > 0.9:
        return "Round"
    elif ratio < 0.75:
        return "Oval"
    else:
        return "Square"


def suggest_outfit(skin_tone, face_shape, occasion):
    suggestions = []

    if skin_tone == "Fair":
        suggestions.append("Try bold colors like red, blue, black")
    elif skin_tone == "Medium":
        suggestions.append("Earth tones and pastels suit you well")
    else:
        suggestions.append("Bright colors like yellow, white look great")

    if face_shape == "Round":
        suggestions.append("V-neck outfits and long layers suit you")
    elif face_shape == "Oval":
        suggestions.append("Most styles suit you!")
    else:
        suggestions.append("Structured outfits look great on you")

    if occasion == "Party":
        suggestions.append("Go for stylish and shiny outfits")
    elif occasion == "Casual":
        suggestions.append("Keep it simple and comfortable")
    else:
        suggestions.append("Formal wear like blazers works best")

    return suggestions


# ---------------------------
# Streamlit UI
# ---------------------------

st.title("👗 AI Personal Stylist")

# 👉 Input choice
option = st.radio("Choose Input Method", ["Upload Image", "Use Webcam"])

image = None

# 👉 Upload option
if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload your image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        image = np.array(image)

# 👉 Webcam option
elif option == "Use Webcam":
    camera_image = st.camera_input("Capture your image")
    if camera_image:
        image = Image.open(camera_image)
        image = np.array(image)

# 👉 Occasion selection
occasion = st.selectbox("Select Occasion", ["Casual", "Party", "Formal"])

# ---------------------------
# Processing
# ---------------------------

if image is not None:
    st.image(image, caption="Input Image", use_column_width=True)

    faces = detect_face(image)

    if len(faces) == 0:
        st.error("No face detected!")
    else:
        for face in faces:
            skin_tone = get_skin_tone(image, face)
            face_shape = get_face_shape(face)

            st.subheader("🧠 Analysis")
            st.write(f"Skin Tone: {skin_tone}")
            st.write(f"Face Shape: {face_shape}")

            suggestions = suggest_outfit(skin_tone, face_shape, occasion)

            st.subheader("✨ Style Suggestions")
            for s in suggestions:
                st.write("✔️", s)
