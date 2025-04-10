# 🧠 Voice-Controlled Image Caption Generator

This Python script allows you to **take a picture with your webcam** or **upload an image**, and then it generates a **caption for that image using a pre-trained vision-language model**.

It uses:
- 🖼️ Image inputs (from webcam or file)
- 🎤 Voice recognition to control actions
- 🧠 Hugging Face-compatible image captioning model (via `processor.pkl` and `model.pkl`)
- 🗣️ Text-to-speech to speak the caption aloud

---

## 🔧 Features

- 📸 **Capture Image:** Say **"take a picture"** to snap an image using your webcam.
- 📂 **Upload Image:** Say **"upload image"** or **"upload file"** to input an image path manually.
- 🧠 **Image Captioning:** Uses a fine-tuned image captioning model to describe the image.
- 🗣️ **Voice Feedback:** Speaks the generated caption using `pyttsx3`.

---

## 📦 Requirements

Install required packages:

```bash
pip install opencv-python numpy pillow pyttsx3 SpeechRecognition sounddevice transformers
