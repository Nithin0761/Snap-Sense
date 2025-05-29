import streamlit as st
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import speech_recognition as sr
import pyttsx3
import cv2
import numpy as np

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Text-to-speech engine
engine = pyttsx3.init()

# Image captioning function
def generate_caption(image, processor, model):
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

# Voice recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening for command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            st.success(f"Recognized: {command}")
            return command.lower()
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Request error: {e}")
    return ""

# Speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Capture image using webcam (OpenCV)
def take_picture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Could not access webcam.")
        return None

    # Warm-up frames
    for _ in range(5):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret:
        st.error("Failed to capture image.")
        return None

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(frame_rgb)

# App interface
def main():
    st.title("🖼️ Image Captioning with Voice Control")

    if "caption" not in st.session_state:
        st.session_state.caption = ""
    if "image" not in st.session_state:
        st.session_state.image = None

    # Choose action
    action = st.selectbox("Choose an action:", ["Take Picture", "Upload Image", "Use Voice Command"])

    if action == "Take Picture":
        if st.button("Capture"):
            image = take_picture()
            if image:
                st.image(image, caption="Captured Image", use_container_width=True)
                caption = generate_caption(image, processor, model)
                st.session_state.caption = caption
                st.session_state.image = image
                speak(caption)
                st.success(f"Caption: {caption}")

    elif action == "Upload Image":
        uploaded = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
        if uploaded:
            image = Image.open(uploaded).convert("RGB")
            st.image(image, caption="Uploaded Image", use_container_width=True)
            caption = generate_caption(image, processor, model)
            st.session_state.caption = caption
            st.session_state.image = image
            speak(caption)
            st.success(f"Caption: {caption}")

    elif action == "Use Voice Command":
        if st.button("Start Listening"):
            command = recognize_speech()
            if "take" in command and "picture" in command:
                image = take_picture()
            elif "upload" in command:
                st.warning("Use the Upload Image tab to upload files.")
                return
            else:
                st.warning("Unknown command.")
                return

            if image:
                st.image(image, caption="Captured Image", use_container_width=True)
                caption = generate_caption(image, processor, model)
                st.session_state.caption = caption
                st.session_state.image = image
                speak(caption)
                st.success(f"Caption: {caption}")

if __name__ == "__main__":
    main()
