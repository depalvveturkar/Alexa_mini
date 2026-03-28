import os

# ========================================
# 📂 PATH CONFIGURATIONS
# ========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(DATA_DIR, 'models')

# Audio settings
AUDIO_FILE = os.path.join(DATA_DIR, 'input.wav')
SAMPLE_RATE = 48000
DURATION = 5  # seconds

# Dataset path
DATASET_PATH = os.path.join(DATA_DIR, 'alexa_data.csv')

# FFmpeg path (update this to your actual path)
FFMPEG_PATH = r'C:\Users\Dipal\Desktop\Machine_Learning_Projects\Alexa\path_ffmpeg\ffmpeg\ffmpeg\ffmpeg-8.1-essentials_build\bin'

# Whisper model size
WHISPER_MODEL = 'base'  # Options: tiny, base, small, medium, large

# ========================================
# 🎤 SPEECH SETTINGS
# ========================================
WAKE_WORDS = ['alexa', 'hey alexa', 'ok alexa']

# ========================================
# 🔊 TEXT-TO-SPEECH SETTINGS
# ========================================
TTS_VOICE_INDEX = 1  # 0 = male, 1 = female (usually)
TTS_RATE = 165  # Speaking speed
TTS_VOLUME = 1.0  # Volume (0.0 to 1.0)

# ========================================
# 🧠 MODEL SETTINGS
# ========================================
MLP_HIDDEN_LAYERS = (50, 25)
MLP_MAX_ITER = 500
MODEL_SAVE_PATH = os.path.join(MODEL_DIR, 'intent_model.pkl')
VECTORIZER_SAVE_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')

# ========================================
# 🌐 API KEYS (for future enhancements)
# ========================================
WEATHER_API_KEY = None  # You can add OpenWeatherMap API key
NEWS_API_KEY = None     # You can add NewsAPI key

# ========================================
# 🎨 UI SETTINGS
# ========================================
ENABLE_COLOR_OUTPUT = True
DEBUG_MODE = True