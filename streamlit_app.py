import streamlit as st
import cv2
from PIL import Image
import pickle
import pyttsx3
import speech_recognition as sr
import time

# Page configuration
st.set_page_config(
    page_title="SnapSense - Image Captioning",
    page_icon="📸",
    layout="wide"
)

# =========================
# === Style Definitions ===
# =========================
def get_theme_css(theme):
    dark_css = """
        <style>
        body, .main, .stApp {
            background-color: #0f0f0f !important;
            color: #E0E0E0;
        }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-thumb { background: #444; border-radius: 10px; }
        .stButton>button {
            width: 100%;
            background-color: #1f8ef1;
            color: white;
            padding: 10px;
            border-radius: 8px;
            border: none;
            font-size: 16px;
            margin: 10px 0;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #0f7ae5;
        }
        .caption-box, .voice-status, .command-list, .history-box {
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.6);
            color: #E0E0E0;
            font-size: 16px;
            margin-bottom: 15px;
        }
        .stSidebar, .css-6qob1r, .css-1d391kg { background-color: #1e1e1e !important; color: #E0E0E0 !important; }
        </style>
    """
    light_css = """
        <style>
        body, .main, .stApp {
            background-color: #ffffff !important;
            color: #333333;
        }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-thumb { background: #ccc; border-radius: 10px; }
        .stButton>button {
            width: 100%;
            background-color: #1f8ef1;
            color: white;
            padding: 10px;
            border-radius: 8px;
            border: none;
            font-size: 16px;
            margin: 10px 0;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #0f7ae5;
        }
        .caption-box, .voice-status, .command-list, .history-box {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            color: #333333;
            font-size: 16px;
            margin-bottom: 15px;
        }
        .stSidebar, .css-6qob1r, .css-1d391kg { background-color: #ffffff !important; color: #333333 !important; }
        </style>
    """
    return dark_css if theme == "Dark" else light_css

# =========================
# === Utility Functions ===
# =========================
@st.cache_resource
def load_model():
    try:
        with open('processor.pkl', 'rb') as processor_file:
            processor = pickle.load(processor_file)
        with open('model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        return processor, model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}. Using dummy caption mode.")
        speak("Model loading failed. Using dummy caption mode.")
        return None, None

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"TTS error: {str(e)}")

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.markdown('<div class="voice-status">🎤 Listening... Speak now</div>', unsafe_allow_html=True)
        speak("Listening for command")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            st.markdown(f'<div class="voice-status">🎤 Heard: {command}</div>', unsafe_allow_html=True)
            speak(f"Heard command: {command}")
            return command
        except:
            st.markdown('<div class="voice-status">❌ Could not understand audio</div>', unsafe_allow_html=True)
            speak("Could not understand audio")
            return None

def generate_caption(image, processor, model):
    if processor is None or model is None:
        return "Dummy caption: A sample image description."
    try:
        inputs = processor(images=image, return_tensors='pt')
        if isinstance(inputs, tuple):
            inputs = inputs[0]
        output_ids = model.generate(**inputs)
        caption = processor.decode(output_ids[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        st.error(f"Caption generation failed: {str(e)}")
        speak("Caption generation failed")
        return None

def take_picture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Could not open webcam")
        speak("Could not open webcam")
        return None
    ret, frame = cap.read()
    cap.release()
    if ret:
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return None

# =========================
# === Main App Layout  ===
# =========================
def main():
    if 'theme' not in st.session_state:
        st.session_state.theme = "Dark"

    st.sidebar.markdown("### 🎨 Theme")
    theme = st.sidebar.selectbox("Choose Theme", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1)
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.experimental_rerun()

    st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)
    st.title("📸 SnapSense - Image Captioning")

    st.session_state.setdefault('image', None)
    st.session_state.setdefault('caption', None)
    st.session_state.setdefault('listening', False)
    st.session_state.setdefault('history', [])

    processor, model = load_model()
    speak("Welcome to SnapSense. Say 'take picture', 'upload image', 'generate caption', or 'speak caption' to begin.")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.markdown("### 🎤 Voice Commands")
        st.markdown('<div class="command-list">*Available Commands:*<br>'
                    "- 'Take picture'<br>"
                    "- 'Upload image'<br>"
                    "- 'Generate caption'<br>"
                    "- 'Speak caption'<br>"
                    "- 'Stop listening'</div>", unsafe_allow_html=True)

        st.session_state.continuous = st.checkbox("🎧 Continuous Listening")

        if st.button("🎤 Start Voice Command"):
            st.session_state.listening = True
            while st.session_state.listening:
                command = listen_for_command()
                if command:
                    if 'take picture' in command:
                        st.session_state.image = take_picture()
                        if st.session_state.image:
                            speak("Picture taken successfully")
                            st.success("Picture taken successfully!")
                    elif 'upload image' in command:
                        speak("Please upload an image using the file uploader")
                        st.info("Please upload an image using the file uploader")
                    elif 'generate caption' in command and st.session_state.image:
                        caption = generate_caption(st.session_state.image, processor, model)
                        if caption:
                            st.session_state.caption = caption
                            st.session_state.history.append({"image": st.session_state.image, "caption": caption})
                            speak(f"Caption generated: {caption}")
                            st.success("Caption generated!")
                    elif 'speak caption' in command and st.session_state.caption:
                        speak(f"Caption: {st.session_state.caption}")
                        st.success("Speaking caption...")
                    elif 'stop listening' in command:
                        st.session_state.listening = False
                        speak("Stopped listening")
                        break
                if not st.session_state.continuous:
                    break
                time.sleep(1)

    with col2:
        st.markdown("### 📷 Image Input")
        if st.button("📸 Take Picture"):
            st.session_state.image = take_picture()
            if st.session_state.image:
                speak("Picture taken successfully")
                st.success("Picture taken successfully!")

        uploaded_file = st.file_uploader("Or upload an image", type=['jpg', 'jpeg', 'png'])
        if uploaded_file:
            st.session_state.image = Image.open(uploaded_file).convert('RGB')
            speak("Image uploaded successfully")
            st.success("Image uploaded successfully!")

        if st.session_state.image:
            st.image(st.session_state.image, use_column_width=True)
            if st.button("🔍 Generate Caption"):
                caption = generate_caption(st.session_state.image, processor, model)
                if caption:
                    st.session_state.caption = caption
                    st.session_state.history.append({"image": st.session_state.image, "caption": caption})
                    speak(f"Caption generated: {caption}")
                    st.success("Caption generated!")
        else:
            st.info("No image selected. Take a picture or upload an image.")

    with col3:
        st.markdown("### 📝 Results")
        if st.session_state.caption:
            st.markdown(f'<div class="caption-box">*Caption:* {st.session_state.caption}</div>', unsafe_allow_html=True)
            if st.button("🔊 Speak Caption"):
                speak(f"Caption: {st.session_state.caption}")
                st.success("Speaking caption...")

        st.markdown("### 📜 Caption History")
        if st.session_state.history:
            st.markdown('<div class="history-box">', unsafe_allow_html=True)
            for idx, item in enumerate(st.session_state.history[::-1]):
                cols = st.columns([1, 4, 1])
                with cols[0]:
                    st.image(item['image'], width=80)
                with cols[1]:
                    st.markdown(f"*{item['caption']}*")
                with cols[2]:
                    if st.button(f"🔄 Load {idx+1}", key=f"load_{idx}"):
                        st.session_state.image = item['image']
                        st.session_state.caption = item['caption']
                        speak(f"Loaded caption {idx+1}: {st.session_state.caption}")
                        st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            if st.button("🗑️ Clear Caption History"):
                st.session_state.history = []
                speak("Caption history cleared")
                st.success("Caption history cleared!")
                st.experimental_rerun()
        else:
            st.info("No caption history available.")

    if st.sidebar.button("🔄 Reset All"):
        st.session_state.image = None
        st.session_state.caption = None
        st.session_state.history = []
        st.session_state.listening = False
        speak("Application reset")
        st.experimental_rerun()

    st.markdown("---")
    st.markdown("Made with ❤ using Streamlit")

if __name__ == "__main__":
    main()
