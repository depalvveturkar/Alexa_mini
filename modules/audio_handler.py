# ========================================
# 🎤 AUDIO HANDLER (CREATES INPUT.WAV)
# ========================================
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import speech_recognition as sr
import os

class AudioHandler:
    def __init__(self):
        print("🔄 Initializing Audio System...")
        
        # Configuration
        self.sample_rate = 16000  # 16kHz for better recognition
        self.duration = 5         # 5 seconds recording
        self.audio_file = "input.wav"
        
        try:
            # Test microphone
            print("🎤 Testing microphone...")
            devices = sd.query_devices()
            default_input = sd.query_devices(kind='input')
            print(f"✅ Default Input: {default_input['name']}")
            
            # Initialize speech recognizer
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            
            print("✅ Audio system ready!")
            
        except Exception as e:
            print(f"❌ Audio Error: {e}")
            print("\n💡 Troubleshooting:")
            print("  1. Check if microphone is connected")
            print("  2. Check Windows Sound Settings")
            print("  3. Try: pip install sounddevice --upgrade")
            self.recognizer = None
    
    def record_audio(self):
        """Record audio and save to input.wav"""
        try:
            print(f"\n🎤 Recording for {self.duration} seconds...")
            print("🔴 SPEAK NOW!")
            
            # Record audio
            recording = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='int16'
            )
            
            # Wait for recording to complete
            sd.wait()
            
            # Save to file
            write(self.audio_file, self.sample_rate, recording)
            
            # Verify file created
            if os.path.exists(self.audio_file):
                file_size = os.path.getsize(self.audio_file)
                print(f"✅ Audio saved: {self.audio_file} ({file_size} bytes)")
                return True
            else:
                print("❌ Failed to create audio file")
                return False
                
        except Exception as e:
            print(f"❌ Recording error: {e}")
            return False
    
    def speech_to_text(self):
        """Convert input.wav to text using Google Speech Recognition"""
        if not os.path.exists(self.audio_file):
            print(f"❌ Audio file not found: {self.audio_file}")
            return None
        
        try:
            print("⚡ Converting speech to text...")
            
            # Load audio file
            with sr.AudioFile(self.audio_file) as source:
                audio = self.recognizer.record(source)
            
            # Recognize using Google
            text = self.recognizer.recognize_google(audio, language="en-US")
            
            if text and len(text.strip()) > 0:
                print(f'📝 You said: "{text}"')
                return text.lower()
            else:
                print("⚠️ No speech detected in audio")
                return None
                
        except sr.UnknownValueError:
            print("⚠️ Could not understand the audio")
            print("💡 Tips: Speak louder and more clearly")
            return None
        except sr.RequestError as e:
            print(f"❌ Google API error: {e}")
            print("💡 Check your internet connection")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def listen(self, retries=3):
        """Complete listen cycle: Record → Save → Transcribe"""
        for attempt in range(retries):
            if attempt > 0:
                print(f"\n🔄 Retry {attempt + 1}/{retries}...")
            
            # Step 1: Record audio
            if self.record_audio():
                # Step 2: Convert to text
                text = self.speech_to_text()
                
                if text:
                    return text
                else:
                    print("💡 No speech detected. Try speaking louder.")
            else:
                print("💡 Recording failed. Check microphone.")
        
        print(f"\n❌ Failed after {retries} attempts")
        return None
    
    def cleanup(self):
        """Delete temporary audio file"""
        try:
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)
                print("🗑️ Cleaned up audio file")
        except:
            pass