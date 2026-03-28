#!/usr/bin/env python3
"""
🤖 ALEXA MINI - Personal Voice Assistant
"""

# ========================================
# 📦 IMPORTS
# ========================================
import os
import sys
import re
import random
import datetime
import webbrowser
import warnings
import tempfile

# Audio
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import speech_recognition as sr

# ML
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier

# TTS
from gtts import gTTS
import pygame

warnings.filterwarnings("ignore")


# ========================================
# 📂 CONFIGURATION
# ========================================
AUDIO_FILE = "input.wav"
SAMPLE_RATE = 16000
DURATION = 5
MAX_RETRIES = 3


# ========================================
# 🎤 AUDIO HANDLER (CREATES INPUT.WAV)
# ========================================
class AudioHandler:
    def __init__(self):
        print("🔄 Initializing Audio System...")
        
        self.sample_rate = SAMPLE_RATE
        self.duration = DURATION
        self.audio_file = AUDIO_FILE
        
        try:
            # List audio devices
            print("\n📋 Available Audio Devices:")
            devices = sd.query_devices()
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    marker = "→" if device['name'] == sd.query_devices(kind='input')['name'] else " "
                    print(f"  {marker} [{i}] {device['name']}")
            
            # Show default
            default_input = sd.query_devices(kind='input')
            print(f"\n✅ Using: {default_input['name']}")
            
            # Initialize recognizer
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            
            print("✅ Audio system ready!")
            
        except Exception as e:
            print(f"❌ Audio Error: {e}")
            self.recognizer = None
    
    def record_audio(self):
        """Record audio from microphone and save to file"""
        try:
            print(f"\n{'='*40}")
            print(f"🎤 RECORDING ({self.duration} seconds)")
            print(f"{'='*40}")
            print("🔴 SPEAK NOW!")
            
            # Record
            recording = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='int16'
            )
            
            # Show countdown
            for i in range(self.duration, 0, -1):
                sd.sleep(1000)
                print(f"⏱️ {i} seconds remaining...")
            
            sd.wait()
            print("🛑 Recording stopped")
            
            # Save file
            write(self.audio_file, self.sample_rate, recording)
            
            # Verify
            if os.path.exists(self.audio_file):
                size = os.path.getsize(self.audio_file)
                print(f"✅ Saved: {self.audio_file} ({size:,} bytes)")
                return True
            else:
                print("❌ File not created!")
                return False
                
        except Exception as e:
            print(f"❌ Recording Error: {e}")
            return False
    
    def speech_to_text(self):
        """Convert audio file to text"""
        if not os.path.exists(self.audio_file):
            print(f"❌ File not found: {self.audio_file}")
            return None
        
        try:
            print("\n⚡ Processing speech...")
            
            with sr.AudioFile(self.audio_file) as source:
                audio = self.recognizer.record(source)
            
            text = self.recognizer.recognize_google(audio, language="en-US")
            
            if text:
                print(f'📝 You said: "{text}"')
                return text.lower()
            return None
            
        except sr.UnknownValueError:
            print("⚠️ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ API Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def listen(self, retries=MAX_RETRIES):
        """Record and transcribe with retries"""
        for attempt in range(retries):
            if attempt > 0:
                print(f"\n🔄 Attempt {attempt + 1}/{retries}")
            
            if self.record_audio():
                text = self.speech_to_text()
                if text:
                    return text
        
        return None
    
    def cleanup(self):
        """Remove audio file"""
        try:
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)
        except:
            pass


# ========================================
# 🧠 INTENT CLASSIFIER
# ========================================
class IntentClassifier:
    def __init__(self):
        print("\n🔄 Training Intent Classifier...")
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        self.model = MLPClassifier(hidden_layer_sizes=(50, 25), max_iter=500, random_state=42)
        self.train_model()
    
    def train_model(self):
        data = [
            # Music
            ("play music", "play_music"), ("play song", "play_music"),
            ("play spotify", "play_music"), ("music please", "play_music"),
            
            # Website
            ("open youtube", "open_website"), ("open google", "open_website"),
            ("youtube", "open_website"), ("open netflix", "open_website"),
            ("open amazon", "open_website"), ("open instagram", "open_website"),
            
            # Jokes
            ("tell me a joke", "jokes_fun"), ("joke", "jokes_fun"),
            ("make me laugh", "jokes_fun"),
            
            # News
            ("news", "news"), ("show news", "news"),
            ("national news", "news"), ("international news", "news"),
            
            # Cricket
            ("cricket", "cricket"), ("cricket score", "cricket"),
            ("ipl", "cricket"), ("match score", "cricket"),
            
            # Movies
            ("movie", "movies"), ("netflix", "movies"),
            ("watch movie", "movies"),
            
            # Shopping
            ("shopping", "shopping"), ("amazon", "shopping"),
            ("flipkart", "shopping"), ("buy", "shopping"),
            
            # Weather
            ("weather", "weather"), ("temperature", "weather"),
            
            # Time
            ("time", "date_time"), ("date", "date_time"),
            ("what time", "date_time"),
            
            # Calculator
            ("calculate", "calculator"), ("plus", "calculator"),
            ("add", "calculator"), ("multiply", "calculator"),
            
            # Facts
            ("fact", "facts"), ("tell me a fact", "facts"),
            
            # Personality
            ("hello", "personality"), ("hi", "personality"),
            ("how are you", "personality"), ("thank you", "personality"),
            
            # Search
            ("search", "general_qa"), ("who is", "general_qa"),
            ("what is", "general_qa"),
        ]
        
        X = self.vectorizer.fit_transform([d[0] for d in data])
        y = [d[1] for d in data]
        self.model.fit(X, y)
        print(f"✅ Classifier ready ({len(data)} samples)")
    
    def predict(self, text):
        try:
            X = self.vectorizer.transform([text])
            intent = self.model.predict(X)[0]
            conf = max(self.model.predict_proba(X)[0])
            print(f"🎯 Intent: {intent} ({conf:.0%})")
            return intent
        except:
            return "unknown"


# ========================================
# 🔊 TEXT TO SPEECH
# ========================================
class TextToSpeech:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.temp_dir = tempfile.gettempdir()
            print("✅ TTS ready (Google)")
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            self.temp_dir = None
    
    def speak(self, text):
        print(f"\n🔊 Alexa: {text}")
        
        if not self.temp_dir:
            return
        
        try:
            path = os.path.join(self.temp_dir, "speech.mp3")
            gTTS(text=text, lang='en', slow=False).save(path)
            
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            pygame.mixer.music.unload()
            os.remove(path)
        except Exception as e:
            print(f"❌ TTS Error: {e}")


# ========================================
# ⚡ ACTION HANDLER
# ========================================
class ActionHandler:
    def __init__(self):
        self.state = {"awaiting": False, "context": None, "data": {}}
    
    def reset(self):
        self.state = {"awaiting": False, "context": None, "data": {}}
    
    def set_state(self, context, data=None):
        self.state = {"awaiting": True, "context": context, "data": data or {}}
    
    def handle_follow_up(self, text):
        ctx = self.state["context"]
        text = text.lower()
        self.reset()
        
        if ctx == "news_type":
            if "national" in text:
                webbrowser.open("https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hwbEVnSmxiaWdBUAE")
                return "Opening national news"
            elif "international" in text:
                webbrowser.open("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pKVGlnQVAB")
                return "Opening world news"
            else:
                webbrowser.open("https://news.google.com")
                return "Opening Google News"
        
        elif ctx == "music_platform":
            if "spotify" in text:
                webbrowser.open("https://open.spotify.com")
                return "Opening Spotify"
            elif "youtube" in text:
                webbrowser.open("https://www.youtube.com/results?search_query=music")
                return "Playing on YouTube"
            elif "jio" in text or "saavn" in text:
                webbrowser.open("https://www.jiosaavn.com")
                return "Opening JioSaavn"
            else:
                webbrowser.open("https://www.youtube.com/results?search_query=music")
                return "Playing on YouTube"
        
        elif ctx == "cricket_platform":
            if "hotstar" in text:
                webbrowser.open("https://www.hotstar.com/in/sports/cricket")
                return "Opening Hotstar"
            elif "cricbuzz" in text:
                webbrowser.open("https://www.cricbuzz.com")
                return "Opening Cricbuzz"
            else:
                webbrowser.open("https://www.google.com/search?q=cricket+score")
                return "Showing scores"
        
        return None
    
    def perform(self, intent, text):
        text_lower = text.lower()
        
        if self.state["awaiting"]:
            r = self.handle_follow_up(text)
            if r:
                return r
        
        # Music
        if intent == "play_music":
            if "spotify" in text_lower:
                webbrowser.open("https://open.spotify.com")
                return "Opening Spotify"
            elif "youtube" in text_lower:
                webbrowser.open("https://www.youtube.com/results?search_query=music")
                return "Playing on YouTube"
            else:
                self.set_state("music_platform")
                return "Which platform? Spotify, YouTube, JioSaavn, or Gaana?"
        
        # Website
        elif intent == "open_website":
            sites = {
                "youtube": "https://www.youtube.com",
                "google": "https://www.google.com",
                "netflix": "https://www.netflix.com",
                "amazon": "https://www.amazon.in",
                "instagram": "https://www.instagram.com",
                "facebook": "https://www.facebook.com",
                "github": "https://www.github.com",
            }
            for name, url in sites.items():
                if name in text_lower:
                    webbrowser.open(url)
                    return f"Opening {name.title()}"
            return "Which website?"
        
        # Jokes
        elif intent == "jokes_fun":
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why did the computer get cold? It left its Windows open!",
            ]
            return random.choice(jokes)
        
        # News
        elif intent == "news":
            if "national" in text_lower:
                webbrowser.open("https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hwbEVnSmxiaWdBUAE")
                return "Opening national news"
            else:
                self.set_state("news_type")
                return "Which news? National or International?"
        
        # Cricket
        elif intent == "cricket":
            if "hotstar" in text_lower:
                webbrowser.open("https://www.hotstar.com/in/sports/cricket")
                return "Opening Hotstar"
            else:
                self.set_state("cricket_platform")
                return "Where? Hotstar or Cricbuzz?"
        
        # Movies
        elif intent == "movies":
            webbrowser.open("https://www.netflix.com")
            return "Opening Netflix"
        
        # Shopping
        elif intent == "shopping":
            webbrowser.open("https://www.amazon.in")
            return "Opening Amazon"
        
        # Weather
        elif intent == "weather":
            webbrowser.open("https://www.google.com/search?q=weather")
            return "Showing weather"
        
        # Time
        elif intent == "date_time":
            now = datetime.datetime.now()
            return f"It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d')}"
        
        # Calculator
        elif intent == "calculator":
            nums = list(map(float, re.findall(r'\d+', text)))
            if len(nums) >= 2:
                if "plus" in text_lower or "add" in text_lower:
                    return f"Answer: {int(nums[0] + nums[1])}"
                elif "minus" in text_lower:
                    return f"Answer: {int(nums[0] - nums[1])}"
                elif "times" in text_lower or "multiply" in text_lower:
                    return f"Answer: {int(nums[0] * nums[1])}"
            return "Couldn't calculate"
        
        # Facts
        elif intent == "facts":
            return "Honey never spoils! 3000 year old honey was found in Egyptian tombs."
        
        # Personality
        elif intent == "personality":
            if "hello" in text_lower or "hi" in text_lower:
                return "Hello! How can I help?"
            elif "thank" in text_lower:
                return "You're welcome!"
            return "I'm Alexa Mini, your assistant!"
        
        # Search
        elif intent == "general_qa":
            webbrowser.open(f"https://www.google.com/search?q={text.replace(' ', '+')}")
            return "Here's what I found"
        
        return "I didn't understand. Try again!"


# ========================================
# 🤖 ALEXA MINI
# ========================================
class AlexaMini:
    def __init__(self):
        print("\n" + "=" * 50)
        print("🤖 ALEXA MINI - Voice Assistant")
        print("=" * 50)
        
        self.audio = AudioHandler()
        self.classifier = IntentClassifier()
        self.action = ActionHandler()
        self.tts = TextToSpeech()
        
        print("\n" + "=" * 50)
        print("✅ READY! Speak clearly when recording starts.")
        print("=" * 50)
    
    def run(self):
        self.tts.speak("Hello! How can I help you?")
        
        try:
            # Listen
            text = self.audio.listen()
            
            if not text:
                self.tts.speak("I couldn't hear you. Please try again!")
                return
            
            # Exit check
            if any(w in text for w in ["quit", "exit", "bye", "stop"]):
                self.tts.speak("Goodbye!")
                return
            
            # Process
            intent = self.classifier.predict(text)
            response = self.action.perform(intent, text)
            self.tts.speak(response)
            
            # Follow-up
            if self.action.state["awaiting"]:
                print("\n💬 Waiting for your choice...")
                follow = self.audio.listen(retries=2)
                if follow:
                    result = self.action.handle_follow_up(follow)
                    if result:
                        self.tts.speak(result)
            
            self.tts.speak("Done! Have a great day!")
            
        except KeyboardInterrupt:
            self.tts.speak("Goodbye!")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.audio.cleanup()


# ========================================
# 🚀 RUN
# ========================================
if __name__ == "__main__":
    assistant = AlexaMini()
    assistant.run()
    print("\n👋 Alexa Mini stopped.")