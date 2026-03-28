from gtts import gTTS
import pygame
import os
import tempfile

# ========================================
# 🔊 TEXT TO SPEECH (GOOGLE - NATURAL VOICE)
# ========================================
class TextToSpeech:
    def __init__(self):
        try:
            # Initialize pygame for audio playback
            pygame.mixer.init()
            self.temp_dir = tempfile.gettempdir()
            print("✅ Google TTS initialized (Natural Voice)")
        except Exception as e:
            print(f"❌ TTS error: {e}")
            self.temp_dir = None
    
    def speak(self, text):
        """Convert text to speech using Google TTS"""
        print(f"\n🔊 Alexa: {text}")
        
        if not self.temp_dir:
            return
        
        try:
            # Create temporary audio file
            audio_file = os.path.join(self.temp_dir, "alexa_speech.mp3")
            
            # Generate speech using Google TTS
            tts = gTTS(
                text=text,
                lang='en',
                slow=False,
                tld='com'  # Use .com for US accent (or 'co.uk' for British)
            )
            
            # Save to file
            tts.save(audio_file)
            
            # Play audio
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up
            try:
                os.remove(audio_file)
            except:
                pass
                
        except Exception as e:
            print(f"❌ TTS playback error: {e}")