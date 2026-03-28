#!/usr/bin/env python3
"""
🤖 ALEXA MINI - Streamlit Web Interface (FIXED - Opens Websites)
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import re
import random
import datetime
import tempfile

# Audio
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr

# ML
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier

# TTS
from gtts import gTTS
import base64
from io import BytesIO

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
# 🎨 CUSTOM CSS
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
# 🌐 WEBSITE OPENER FUNCTIONS
# ========================================
def open_website_button(url, label="🌐 Click Here to Open Website"):
    """
    Creates a prominent button/link to open website
    This is the most reliable method in Streamlit
    """
    button_html = f'''
    <a href="{url}" target="_blank" class="open-btn">
        {label}
    </a>
    '''
    st.markdown(button_html, unsafe_allow_html=True)


def open_website_auto(url):
    """
    Attempts to auto-open using JavaScript
    Note: May be blocked by browser pop-up blockers
    """
    js = f'''
    <script>
        window.open("{url}", "_blank");
    </script>
    '''
    components.html(js, height=0, width=0)


def show_website_iframe(url, height=600):
    """
    Shows website in an iframe (works for some sites)
    Note: Many sites block iframe embedding
    """
    try:
        st.components.v1.iframe(url, height=height, scrolling=True)
    except:
        st.warning("This website cannot be embedded. Please use the link above.")


# ========================================
# 🧠 INTENT CLASSIFIER
# ========================================
@st.cache_resource
def load_classifier():
    """Load and train the intent classifier"""
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
    model = MLPClassifier(hidden_layer_sizes=(50, 25), max_iter=500, random_state=42)
    
    training_data = [
        # Music
        ("play music", "play_music"), ("play song", "play_music"),
        ("play spotify", "play_music"), ("music", "play_music"),
        ("play youtube music", "play_music"),
        
        # Website
        ("open youtube", "open_website"), ("open google", "open_website"),
        ("youtube", "open_website"), ("open netflix", "open_website"),
        ("open amazon", "open_website"), ("open instagram", "open_website"),
        ("open github", "open_website"), ("open facebook", "open_website"),
        
        # Jokes
        ("tell me a joke", "jokes_fun"), ("joke", "jokes_fun"),
        ("make me laugh", "jokes_fun"), ("funny", "jokes_fun"),
        
        # News
        ("news", "news"), ("show news", "news"),
        ("national news", "news"), ("international news", "news"),
        
        # Cricket
        ("cricket", "cricket"), ("cricket score", "cricket"),
        ("ipl", "cricket"), ("live score", "cricket"), ("live cricket", "cricket"),
        
        # Movies
        ("movie", "movies"), ("netflix", "movies"),
        ("watch movie", "movies"), ("prime video", "movies"),
        
        # Shopping
        ("shopping", "shopping"), ("amazon", "shopping"),
        ("flipkart", "shopping"), ("buy", "shopping"),
        
        # Weather
        ("weather", "weather"), ("temperature", "weather"),
        ("forecast", "weather"),
        
        # Time
        ("time", "date_time"), ("date", "date_time"),
        ("what time", "date_time"), ("what day", "date_time"),
        
        # Calculator
        ("calculate", "calculator"), ("plus", "calculator"),
        ("add", "calculator"), ("multiply", "calculator"),
        ("minus", "calculator"), ("divide", "calculator"),
        
        # Facts
        ("fact", "facts"), ("tell me a fact", "facts"),
        
        # Personality
        ("hello", "personality"), ("hi", "personality"),
        ("how are you", "personality"), ("thank you", "personality"),
        
        # Search
        ("search", "general_qa"), ("who is", "general_qa"),
        ("what is", "general_qa"),
    ]
    
    X = vectorizer.fit_transform([d[0] for d in training_data])
    y = [d[1] for d in training_data]
    model.fit(X, y)
    
    return vectorizer, model


# ========================================
# 🎤 AUDIO HANDLER
# ========================================
class AudioHandler:
    def __init__(self, sample_rate=16000, duration=5):
        self.sample_rate = sample_rate
        self.duration = duration
        self.audio_file = "temp_audio.wav"
        self.recognizer = sr.Recognizer()
    
    def record_audio(self, status_placeholder):
        """Record audio from microphone"""
        try:
            status_placeholder.warning(f"🔴 Recording for {self.duration} seconds... SPEAK NOW!")
            
            recording = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='int16'
            )
            sd.wait()
            write(self.audio_file, self.sample_rate, recording)
            
            status_placeholder.success("✅ Recording complete!")
            return True
            
        except Exception as e:
            status_placeholder.error(f"❌ Recording error: {e}")
            return False
    
    def speech_to_text(self):
        """Convert audio to text"""
        try:
            with sr.AudioFile(self.audio_file) as source:
                audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio, language="en-US")
            return text
        except sr.UnknownValueError:
            return None
        except Exception as e:
            return None
    
    def cleanup(self):
        try:
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)
        except:
            pass


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
# ⚡ ACTION HANDLER
# ========================================
def perform_action(intent, text):
    """Execute action based on intent"""
    text_lower = text.lower()
    
    # Website URLs
    websites = {
        "youtube": ("https://www.youtube.com", "YouTube", "🎬"),
        "google": ("https://www.google.com", "Google", "🔍"),
        "netflix": ("https://www.netflix.com", "Netflix", "🎬"),
        "amazon": ("https://www.amazon.in", "Amazon", "🛒"),
        "instagram": ("https://www.instagram.com", "Instagram", "📸"),
        "facebook": ("https://www.facebook.com", "Facebook", "👥"),
        "github": ("https://www.github.com", "GitHub", "💻"),
        "twitter": ("https://www.twitter.com", "Twitter", "🐦"),
        "linkedin": ("https://www.linkedin.com", "LinkedIn", "💼"),
        "spotify": ("https://open.spotify.com", "Spotify", "🎵"),
        "hotstar": ("https://www.hotstar.com", "JioHotstar", "📺"),
        "flipkart": ("https://www.flipkart.com", "Flipkart", "🛒"),
        "myntra": ("https://www.myntra.com", "Myntra", "👗"),
        "prime": ("https://www.primevideo.com", "Prime Video", "🎬"),
        "cricbuzz": ("https://www.cricbuzz.com", "Cricbuzz", "🏏"),
    }
    
    # PLAY MUSIC
    if intent == "play_music":
        if "spotify" in text_lower:
            return "🎵 Opening Spotify for you!", "https://open.spotify.com", "Spotify"
        elif "youtube" in text_lower:
            return "🎵 Playing music on YouTube!", "https://www.youtube.com/results?search_query=music", "YouTube Music"
        elif "jiosaavn" in text_lower or "saavn" in text_lower:
            return "🎵 Opening JioSaavn!", "https://www.jiosaavn.com", "JioSaavn"
        elif "gaana" in text_lower:
            return "🎵 Opening Gaana!", "https://gaana.com", "Gaana"
        else:
            return "🎵 Opening YouTube Music for you!", "https://www.youtube.com/results?search_query=music", "YouTube Music"
    
    # OPEN WEBSITE
    elif intent == "open_website":
        for name, (url, display, emoji) in websites.items():
            if name in text_lower:
                return f"{emoji} Opening {display}!", url, display
        return "🌐 Which website would you like to open?", None, None
    
    # JOKES
    elif intent == "jokes_fun":
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
            "Why did the computer get cold? It left its Windows open! 🪟",
            "Why do Java developers wear glasses? Because they can't C#! 👓",
            "A SQL query walks into a bar, walks up to two tables and asks: Can I join you? 🍺",
            "There are only 10 types of people: those who understand binary and those who don't! 🔢",
        ]
        return random.choice(jokes), None, None
    
    # NEWS
    elif intent == "news":
        if "national" in text_lower or "india" in text_lower:
            return "📰 Opening National News!", "https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hwbEVnSmxiaWdBUAE?hl=en-IN", "National News"
        elif "international" in text_lower or "world" in text_lower:
            return "📰 Opening International News!", "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pKVGlnQVAB", "World News"
        elif "sports" in text_lower:
            return "📰 Opening Sports News!", "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pKVGlnQVAB", "Sports News"
        else:
            return "📰 Opening Google News!", "https://news.google.com", "Google News"
    
    # CRICKET
    elif intent == "cricket":
        if "hotstar" in text_lower:
            return "🏏 Opening JioHotstar for Live Cricket!", "https://www.hotstar.com/in/sports/cricket", "JioHotstar Cricket"
        elif "cricbuzz" in text_lower:
            return "🏏 Opening Cricbuzz!", "https://www.cricbuzz.com/cricket-match/live-scores", "Cricbuzz"
        else:
            return "🏏 Showing Live Cricket Scores!", "https://www.google.com/search?q=live+cricket+score", "Cricket Scores"
    
    # MOVIES
    elif intent == "movies":
        if "netflix" in text_lower:
            return "🎬 Opening Netflix!", "https://www.netflix.com", "Netflix"
        elif "prime" in text_lower:
            return "🎬 Opening Prime Video!", "https://www.primevideo.com", "Prime Video"
        elif "hotstar" in text_lower:
            return "🎬 Opening Disney+ Hotstar!", "https://www.hotstar.com", "Hotstar"
        else:
            return "🎬 Opening Netflix!", "https://www.netflix.com", "Netflix"
    
    # SHOPPING
    elif intent == "shopping":
        if "flipkart" in text_lower:
            return "🛒 Opening Flipkart!", "https://www.flipkart.com", "Flipkart"
        elif "myntra" in text_lower:
            return "🛒 Opening Myntra!", "https://www.myntra.com", "Myntra"
        else:
            return "🛒 Opening Amazon!", "https://www.amazon.in", "Amazon"
    
    # WEATHER
    elif intent == "weather":
        match = re.search(r"(?:in|of|for|at)\s+([a-zA-Z\s]+)", text_lower)
        if match:
            city = match.group(1).strip()
            return f"🌦️ Weather in {city.title()}!", f"https://www.google.com/search?q=weather+in+{city.replace(' ', '+')}", "Weather"
        else:
            return "🌦️ Today's Weather!", "https://www.google.com/search?q=weather+today", "Weather"
    
    # DATE TIME
    elif intent == "date_time":
        now = datetime.datetime.now()
        return f"🕐 It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}", None, None
    
    # CALCULATOR
    elif intent == "calculator":
        nums = list(map(float, re.findall(r'\d+\.?\d*', text)))
        if len(nums) >= 2:
            if any(w in text_lower for w in ["plus", "add", "+"]):
                result = nums[0] + nums[1]
                return f"🧮 {int(nums[0])} + {int(nums[1])} = **{int(result)}**", None, None
            elif any(w in text_lower for w in ["minus", "subtract", "-"]):
                result = nums[0] - nums[1]
                return f"🧮 {int(nums[0])} - {int(nums[1])} = **{int(result)}**", None, None
            elif any(w in text_lower for w in ["times", "multiply", "x", "*", "into"]):
                result = nums[0] * nums[1]
                return f"🧮 {int(nums[0])} × {int(nums[1])} = **{int(result)}**", None, None
            elif any(w in text_lower for w in ["divide", "/"]):
                if nums[1] != 0:
                    result = nums[0] / nums[1]
                    return f"🧮 {int(nums[0])} ÷ {int(nums[1])} = **{result:.2f}**", None, None
        return "🧮 Try saying '5 plus 3' or '10 times 7'", None, None
    
    # FACTS
    elif intent == "facts":
        facts = [
            "🍯 Honey never spoils! 3000-year-old honey was found in Egyptian tombs.",
            "🐙 Octopuses have three hearts and blue blood!",
            "🪐 A day on Venus is longer than a year on Venus.",
            "🍌 Bananas are berries, but strawberries are not!",
            "🦈 Sharks are older than trees - around for 400 million years!",
        ]
        return random.choice(facts), None, None
    
    # PERSONALITY
    elif intent == "personality":
        if any(w in text_lower for w in ["hello", "hi", "hey"]):
            return "👋 Hello! How can I help you today?", None, None
        elif "thank" in text_lower:
            return "😊 You're welcome! Happy to help!", None, None
        elif "how are you" in text_lower:
            return "🤖 I'm doing great! How can I assist you?", None, None
        return "🤖 I'm Alexa Mini, your AI assistant!", None, None
    
    # GENERAL QA
    elif intent == "general_qa":
        query = text.replace(" ", "+")
        return f"🔍 Searching: '{text}'", f"https://www.google.com/search?q={query}", "Google Search"
    
    return "❓ Try: 'open youtube', 'play music', 'tell me a joke'", None, None


# ========================================
# 🎯 MAIN APP
# ========================================
def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Alexa Mini</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your Personal AI Voice Assistant</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'vectorizer' not in st.session_state:
        st.session_state.vectorizer, st.session_state.model = load_classifier()
    if 'last_url' not in st.session_state:
        st.session_state.last_url = None
    if 'last_site_name' not in st.session_state:
        st.session_state.last_site_name = None
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        recording_duration = st.slider("🎤 Recording Duration", 3, 10, 5)
        enable_tts = st.checkbox("🔊 Text-to-Speech", value=True)
        
        st.markdown("---")
        st.markdown("### 📋 Quick Commands")
        
        commands = {
            "🎵 Music": ["play music", "play spotify", "play youtube music"],
            "🌐 Websites": ["open youtube", "open google", "open github"],
            "📰 News": ["show news", "national news", "sports news"],
            "🏏 Cricket": ["cricket score", "cricket on hotstar", "live cricket"],
            "🎬 Movies": ["open netflix", "open prime video", "open hotstar"],
            "🛒 Shopping": ["open amazon", "open flipkart", "open myntra"],
            "🌦️ Weather": ["weather today", "weather in mumbai"],
            "😂 Fun": ["tell me a joke", "tell me a fact"],
            "🧮 Math": ["5 plus 3", "10 times 7"],
        }
        
        for cat_idx, (category, cmds) in enumerate(commands.items()):
            with st.expander(category):
                for cmd_idx, cmd in enumerate(cmds):
                    if st.button(cmd, key=f"qc_{cat_idx}_{cmd_idx}"):
                        st.session_state.pending_command = cmd
        
        st.markdown("---")
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # ========== VOICE INPUT ==========
        st.markdown("### 🎤 Voice Input")
        
        if st.button("🎙️ Click & Speak", use_container_width=True, key="record"):
            status = st.empty()
            audio_handler = AudioHandler(duration=recording_duration)
            
            if audio_handler.record_audio(status):
                with st.spinner("Processing..."):
                    text = audio_handler.speech_to_text()
                
                if text:
                    process_command(text, enable_tts)
                else:
                    st.error("⚠️ Couldn't understand. Please try again!")
                
                audio_handler.cleanup()
        
        st.markdown("---")
        
        # ========== TEXT INPUT ==========
        st.markdown("### ⌨️ Or Type Command")
        
        # Check for pending command from sidebar
        default_val = st.session_state.pop('pending_command', '')
        
        text_input = st.text_input(
            "Enter command:",
            value=default_val,
            placeholder="e.g., open youtube, play music, tell me a joke...",
            key="text_cmd"
        )
        
        if st.button("📤 Submit", use_container_width=True, key="submit"):
            if text_input:
                process_command(text_input, enable_tts)
            else:
                st.warning("Please enter a command!")
        
        # Auto-process if there was a pending command
        if default_val:
            process_command(default_val, enable_tts)
    
    with col2:
        st.markdown("### 📜 History")
        
        if st.session_state.history:
            for i, item in enumerate(reversed(st.session_state.history[-10:])):
                with st.expander(f"⏰ {item['time']}", expanded=(i == 0)):
                    st.write(f"**You:** {item['command']}")
                    st.write(f"**Alexa:** {item['response']}")
                    if item.get('url'):
                        st.markdown(f"[🔗 {item.get('site_name', 'Open Link')}]({item['url']})")
        else:
            st.info("No commands yet!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#666;'>Made with ❤️ | Alexa Mini Voice Assistant</div>",
        unsafe_allow_html=True
    )


def process_command(text, enable_tts):
    """Process a command and show results"""
    
    # Show command
    st.markdown(f'<div class="command-box">📝 <strong>"{text}"</strong></div>', unsafe_allow_html=True)
    
    # Predict intent
    X = st.session_state.vectorizer.transform([text.lower()])
    intent = st.session_state.model.predict(X)[0]
    confidence = max(st.session_state.model.predict_proba(X)[0])
    
    st.info(f"🎯 Intent: **{intent}** ({confidence:.0%})")
    
    # Get response
    response, url, site_name = perform_action(intent, text)
    
    # Show response
    st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
    
    # ========== OPEN WEBSITE ==========
    if url:
        st.success(f"🌐 Ready to open: **{site_name or 'Website'}**")
        
        # Method 1: Big clickable button (MOST RELIABLE)
        open_website_button(url, f"🚀 Click to Open {site_name or 'Website'}")
        
        # Method 2: Try auto-open (may be blocked)
        open_website_auto(url)
        
        # Method 3: Direct link
        st.markdown(f"**Direct Link:** [{url}]({url})")
    
    # Text-to-Speech
    if enable_tts:
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
    
    # Add to history
    st.session_state.history.append({
        'time': datetime.datetime.now().strftime('%I:%M %p'),
        'command': text,
        'intent': intent,
        'response': response,
        'url': url,
        'site_name': site_name
    })


# ========================================
# 🚀 RUN
# ========================================
if __name__ == "__main__":
    main()