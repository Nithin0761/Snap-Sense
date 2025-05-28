import os
import cv2
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import pickle
from PIL import Image
import pyttsx3

# Load the processor and model
with open('processor.pkl', 'rb') as processor_file:
    processor = pickle.load(processor_file)

with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Function to initialize text-to-speech engine
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()

# Function to take a picture using the camera
def take_picture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Could not open webcam')
        return
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Captured Image', frame)
        cv2.imwrite('captured_image.jpg', frame)
        print('Image saved as captured_image.jpg')
        cv2.waitKey(0)
    else:
        print('Failed to capture image')
    cap.release()
    cv2.destroyAllWindows()

# Function to listen for a single voice command and take a picture
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening for command...')
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f'Command received: {command}')
            if 'take picture' in command or 'click picture' in command or 'take a picture from my webcam' in command:
                take_picture()
                generate_caption_from_file()
                return
        except sr.UnknownValueError:
            print('Sorry, I did not understand that.')
        except sr.RequestError as e:
            print(f'Could not request results; {e}')

# Function to generate caption using the loaded model
def generate_caption_from_file():
    img = cv2.imread('captured_image.jpg')
    if img is not None:
        img_input = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        inputs = processor(img_input, return_tensors='pt')
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        print(f'Generated Caption: {caption}')
        speak(caption)
    else:
        print('No image found!')

# Start listening for a single command
if __name__ == '__main__':
    listen_for_command()