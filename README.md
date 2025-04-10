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


pip install opencv-python numpy pillow pyttsx3 SpeechRecognition sounddevice transformers


▶️ How to Run
Make sure model.pkl and processor.pkl are available in the same folder.

Run the script:

bash
Copy
Edit
python your_script_name.py
Speak your command when prompted:

Say "take a picture" to use your webcam

Say "upload image" to manually upload an image

🧪 Sample Commands
"take a picture"

"upload image"

"click picture"

"upload file"

🖼️ Sample Output
For an image of a dog running on the beach:


🖼 Generating caption from: captured_image.jpg
🧾 Caption: a dog running on the beach
For an uploaded image of a bowl of fruit:


🖼 Generating caption from: C:/Users/User/Desktop/fruit_bowl.jpg
🧾 Caption: a bowl full of assorted fruits
Voice output:

"a bowl full of assorted fruits"

📁 Project Files
your_script_name.py – Main Python script

model.pkl – Pickled vision-language model

processor.pkl – Pickled image processor (e.g., feature extractor or tokenizer)

captured_image.jpg – Temporarily saved image from webcam

📌 Notes
If you face webcam issues, make sure your camera index is correct (cv2.VideoCapture(0) or 1).

Tested with models from Hugging Face (like BLIP/ViT-based captioning models).

Runs fully offline (once the .pkl files are saved locally).

You can find the model here: https://drive.google.com/file/d/1vLjZS1UPvGAIJVgCas_JfwoEVHoIdKzY/view?usp=drive_link
