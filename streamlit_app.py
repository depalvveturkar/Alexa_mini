#!/usr/bin/env python3
"""
🤖 ALEXA MINI - Streamlit Cloud Compatible Version
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import re
import random
import datetime
import tempfile
from io import BytesIO

# Audio Recording (Browser-based)
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr

# ML
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier

# TTS
from gtts import gTTS
import base64

# ========================================
# 🎨 PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="Alexa Mini - Voice Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# 🎨 CUSTOM CSS (Same as before)
# ========================================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .command-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .response-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-size: 1.1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .open-btn {
        display: inline-block;
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        color: white !important;
        padding: 15px 30px;
        text-decoration: none !important;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: all 0.3s;
        text-align: center;
        margin: 10px 0;
    }
    
    .open-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ========================================
# 🌐 WEBSITE OPENER
# ========================================
def open_website_button(url, label="🌐 Click Here to Open Website"):
    """Creates a button to open website"""
    button_html = f'''
    <a href="{url}" target="_blank" class="open-btn">
        {label}
    </a>
    '''
    st.markdown(button_html, unsafe_allow_html=True)


def open_website_auto(url):
    """Auto-opens URL using JavaScript"""
    js = f'''
    <script>
        window.open("{url}", "_blank");
    </script>
    '''
    components.html(js, height=0, width=0)


# ========================================
# 🧠 INTENT CLASSIFIER
# ========================================
@st.cache_resource
def load_classifier():
    """Load and train the intent classifier"""
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
    model = MLPClassifier(hidden_layer_sizes=(50, 25), max_iter=500, random_state=42)
    
    training_data = [
        ("play music", "play_music"), ("play song", "play_music"),
        ("open youtube", "open_website"), ("open google", "open_website"),
        ("tell me a joke", "jokes_fun"), ("joke", "jokes_fun"),
        ("news", "news"), ("show news", "news"),
        ("cricket", "cricket"), ("cricket score", "cricket"),
        ("movie", "movies"), ("netflix", "movies"),
        ("weather", "weather"), ("temperature", "weather"),
        ("time", "date_time"), ("date", "date_time"),
        ("calculate", "calculator"), ("plus", "calculator"),
        ("fact", "facts"), ("hello", "personality"),
        ("search", "general_qa"), ("who is", "general_qa"),
    ]
    
    X = vectorizer.fit_transform([d[0] for d in training_data])
    y = [d[1] for d in training_data]
    model.fit(X, y)
    
    return vectorizer, model


# ========================================
# 🎤 AUDIO HANDLER (Browser-based)
# ========================================
def speech_to_text_from_bytes(audio_bytes):
    """Convert audio bytes to text using Google Speech Recognition"""
    try:
        recognizer = sr.Recognizer()
        
        # Convert bytes to AudioFile
        audio_file = BytesIO(audio_bytes)
        
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        
        # Recognize using Google
        text = recognizer.recognize_google(audio, language="en-US")
        return text
        
    except sr.UnknownValueError:
        return None
    except Exception as e:
        st.error(f"Recognition error: {e}")
        return None


# ========================================
# 🔊 TEXT TO SPEECH
# ========================================
def text_to_speech(text):
    """Generate speech audio"""
    try:
        clean_text = re.sub(r'[^\w\s.,!?]', '', text)
        tts = gTTS(text=clean_text, lang='en', slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode()
        
        audio_html = f'''
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        '''
        return audio_html
    except:
        return None


# ========================================
# ⚡ ACTION HANDLER (Same as before)
# ========================================
def perform_action(intent, text):
    """Execute action based on intent"""
    text_lower = text.lower()
    
    # PLAY MUSIC
    if intent == "play_music":
        if "spotify" in text_lower:
            return "🎵 Opening Spotify!", "https://open.spotify.com", "Spotify"
        elif "youtube" in text_lower:
            return "🎵 Playing on YouTube!", "https://www.youtube.com/results?search_query=music", "YouTube Music"
        else:
            return "🎵 Opening YouTube Music!", "https://www.youtube.com/results?search_query=music", "YouTube"
    
    # OPEN WEBSITE
    elif intent == "open_website":
        sites = {
            "youtube": ("https://www.youtube.com", "YouTube"),
            "google": ("https://www.google.com", "Google"),
            "netflix": ("https://www.netflix.com", "Netflix"),
            "amazon": ("https://www.amazon.in", "Amazon"),
            "github": ("https://www.github.com", "GitHub"),
            "instagram": ("https://www.instagram.com", "Instagram"),
        }
        for name, (url, display) in sites.items():
            if name in text_lower:
                return f"🌐 Opening {display}!", url, display
        return "Which website?", None, None
    
    # JOKES
    elif intent == "jokes_fun":
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
            "Why did the computer get cold? It left its Windows open! 🪟",
            "Why do Java developers wear glasses? Because they can't C#! 👓",
        ]
        return random.choice(jokes), None, None
    
    # NEWS
    elif intent == "news":
        return "📰 Opening Google News!", "https://news.google.com", "Google News"
    
    # CRICKET
    elif intent == "cricket":
        return "🏏 Cricket Scores!", "https://www.google.com/search?q=live+cricket+score", "Cricket"
    
    # MOVIES
    elif intent == "movies":
        return "🎬 Opening Netflix!", "https://www.netflix.com", "Netflix"
    
    # WEATHER
    elif intent == "weather":
        return "🌦️ Weather Info!", "https://www.google.com/search?q=weather", "Weather"
    
    # DATE TIME
    elif intent == "date_time":
        now = datetime.datetime.now()
        return f"🕐 It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}", None, None
    
    # CALCULATOR
    elif intent == "calculator":
        nums = list(map(float, re.findall(r'\d+\.?\d*', text)))
        if len(nums) >= 2:
            if "plus" in text_lower or "add" in text_lower:
                return f"🧮 {int(nums[0])} + {int(nums[1])} = **{int(nums[0] + nums[1])}**", None, None
            elif "times" in text_lower or "multiply" in text_lower:
                return f"🧮 {int(nums[0])} × {int(nums[1])} = **{int(nums[0] * nums[1])}**", None, None
        return "🧮 Try '5 plus 3'", None, None
    
    # FACTS
    elif intent == "facts":
        facts = [
            "🍯 Honey never spoils! 3000-year-old honey was found in Egyptian tombs.",
            "🐙 Octopuses have three hearts!",
            "🍌 Bananas are berries, but strawberries are not!",
        ]
        return random.choice(facts), None, None
    
    # PERSONALITY
    elif intent == "personality":
        return "👋 Hello! I'm Alexa Mini, your AI assistant!", None, None
    
    # GENERAL QA
    elif intent == "general_qa":
        query = text.replace(" ", "+")
        return f"🔍 Searching...", f"https://www.google.com/search?q={query}", "Google"
    
    return "❓ Try: 'open youtube', 'play music', 'tell joke'", None, None


# ========================================
# 🎯 MAIN APP
# ========================================
def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Alexa Mini</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your Personal AI Voice Assistant</p>', unsafe_allow_html=True)
    
    # Initialize
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'vectorizer' not in st.session_state:
        st.session_state.vectorizer, st.session_state.model = load_classifier()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        enable_tts = st.checkbox("🔊 Text-to-Speech", value=True)
        
        st.markdown("---")
        st.markdown("### 📋 Quick Commands")
        
        quick_cmds = [
            "open youtube",
            "play music",
            "tell me a joke",
            "show news",
            "cricket score",
            "what time is it",
        ]
        
        for idx, cmd in enumerate(quick_cmds):
            if st.button(cmd, key=f"qc_{idx}"):
                st.session_state.pending = cmd
        
        st.markdown("---")
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    
    # Main
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Voice Input
        st.markdown("### 🎤 Voice Input")
        
        audio_bytes = audio_recorder(
            text="🎙️ Click to Record",
            recording_color="#e74c3c",
            neutral_color="#3498db",
            icon_name="microphone",
            icon_size="3x"
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            with st.spinner("🔄 Processing speech..."):
                text = speech_to_text_from_bytes(audio_bytes)
            
            if text:
                process_command(text, enable_tts)
            else:
                st.error("⚠️ Couldn't understand. Try again!")
        
        st.markdown("---")
        
        # Text Input
        st.markdown("### ⌨️ Or Type Command")
        
        default = st.session_state.pop('pending', '')
        text_input = st.text_input("Command:", value=default, placeholder="e.g., open youtube")
        
        if st.button("📤 Submit", use_container_width=True):
            if text_input:
                process_command(text_input, enable_tts)
        
        if default:
            process_command(default, enable_tts)
    
    with col2:
        st.markdown("### 📜 History")
        
        if st.session_state.history:
            for i, item in enumerate(reversed(st.session_state.history[-5:])):
                with st.expander(f"⏰ {item['time']}", expanded=(i == 0)):
                    st.write(f"**You:** {item['cmd']}")
                    st.write(f"**Alexa:** {item['resp']}")
                    if item.get('url'):
                        st.markdown(f"[🔗 Open]({item['url']})")
        else:
            st.info("No commands yet!")
    
    st.markdown("---")
    st.markdown("<div style='text-align:center;'>Made with ❤️ | Alexa Mini</div>", unsafe_allow_html=True)


def process_command(text, tts):
    """Process command"""
    st.markdown(f'<div class="command-box">📝 "{text}"</div>', unsafe_allow_html=True)
    
    X = st.session_state.vectorizer.transform([text.lower()])
    intent = st.session_state.model.predict(X)[0]
    confidence = max(st.session_state.model.predict_proba(X)[0])
    
    st.info(f"🎯 **{intent}** ({confidence:.0%})")
    
    response, url, site = perform_action(intent, text)
    
    st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
    
    if url:
        st.success(f"🌐 Ready: **{site}**")
        open_website_button(url, f"🚀 Open {site}")
        open_website_auto(url)
    
    if tts:
        audio = text_to_speech(response)
        if audio:
            st.markdown(audio, unsafe_allow_html=True)
    
    st.session_state.history.append({
        'time': datetime.datetime.now().strftime('%I:%M %p'),
        'cmd': text,
        'resp': response,
        'url': url
    })


if __name__ == "__main__":
    main()