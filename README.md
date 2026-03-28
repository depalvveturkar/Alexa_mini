# 🤖 Alexa Mini - AI-Powered Personal Voice Assistant

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**A smart, responsive voice assistant built with Python that understands natural language and executes commands seamlessly.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Contributing](#-contributing)

</div>

---

## 📖 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Demo](#-demo)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Commands](#-commands)
- [Configuration](#%EF%B8%8F-configuration)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)
- [Contact](#-contact)

---

## 🎯 About

**Alexa Mini** is a lightweight, intelligent voice assistant that brings the power of AI to your desktop. Unlike traditional assistants, it's built with privacy in mind, runs locally, and can be easily customized to fit your needs.

### Why Alexa Mini?

- ✅ **Privacy-First**: Runs entirely on your machine (optional offline mode)
- ✅ **Customizable**: Easy to add new commands and integrations
- ✅ **Smart Conversations**: Understands context and follow-up questions
- ✅ **Natural Voice**: Uses Google TTS for human-like responses
- ✅ **Fast & Efficient**: Optimized for quick response times
- ✅ **Open Source**: Free to use, modify, and distribute

---

## ✨ Features

### 🎤 Voice Interaction
- **Speech Recognition**: Google Speech Recognition for accurate transcription
- **Natural Language Processing**: Intent classification using Machine Learning
- **Text-to-Speech**: Natural-sounding voice responses

### 🎵 Entertainment
- **Music Streaming**: Play music on Spotify, YouTube, JioSaavn, Gaana
- **Movies & Shows**: Open Netflix, Prime Video, Disney+ Hotstar, YouTube
- **Jokes & Facts**: Get programming jokes and interesting facts

### 📰 Information
- **News**: National, International, Sports, Technology, Business news
- **Weather**: Real-time weather updates for any city
- **Cricket Scores**: Live scores on JioHotstar, Cricbuzz, ESPNCricinfo
- **Web Search**: Google search integration

### 🛠️ Utilities
- **Calculator**: Perform mathematical calculations
- **Date & Time**: Get current date and time
- **Timers & Alarms**: Set countdown timers and wake-up alarms
- **Reminders**: Create voice reminders

### 🌐 Web Automation
- **Website Control**: Open YouTube, Google, GitHub, Instagram, etc.
- **Shopping**: Quick access to Amazon, Flipkart, Myntra
- **Social Media**: Instagram, Twitter, Facebook, LinkedIn
- **Email**: Open Gmail with voice command

### 🧠 Smart Features
- **Context Awareness**: Remembers conversation context
- **Follow-up Questions**: "Which platform?" → "Spotify"
- **Multi-turn Dialogues**: Natural conversation flow
- **Platform Selection**: Choose between multiple service providers

---

## 🎥 Demo

🔊 Alexa: Hello! How can I help you?

🎤 You: "Play music"
🎯 Intent: play_music (95%)
🔊 Alexa: "Which platform would you like? Spotify, YouTube, JioSaavn, or Gaana?"

🎤 You: "Spotify"
🔊 Alexa: "Opening Spotify"
✅ Task completed!

🔊 Alexa: "Done! Have a great day!"


### Example Interactions

| Your Command | Alexa's Response |
|--------------|------------------|
| "Open YouTube" | Opens YouTube in your browser |
| "Show me news" | "Which news? National, International, Sports, or Tech?" |
| "Cricket match" | "Where would you like to watch? JioHotstar or Cricbuzz?" |
| "Weather in Mumbai" | Shows current weather forecast |
| "What time is it" | "It's 02:30 PM on Monday, January 15, 2024" |
| "Tell me a joke" | Shares a programming joke |
| "Calculate 25 times 4" | "The answer is 100" |

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+** - Primary programming language
- **Speech Recognition** - Google Speech Recognition API
- **scikit-learn** - Machine Learning for intent classification
- **gTTS** - Google Text-to-Speech for natural voice
- **pyttsx3** - Offline text-to-speech (fallback)

### Libraries Used

ounddevice # Audio recording
scipy # Audio file handling
SpeechRecognition # Speech-to-text conversion
gTTS # Text-to-speech (Google)
pygame # Audio playback
scikit-learn # ML model (TF-IDF + MLP)
pandas # Data processing
numpy # Numerical operations
pyttsx3 # Offline TTS
webbrowser # Web automation


### Machine Learning
- **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Classifier**: Multi-layer Perceptron (Neural Network)
- **Training**: Supervised learning with labeled intent data
- **Accuracy**: ~95% intent prediction accuracy

---

## 📦 Installation

### Prerequisites

Before you begin, ensure you have:
- **Python 3.8 or higher** installed
- **Microphone** connected and working
- **Internet connection** (for Google Speech Recognition & TTS)
- **Speakers/Headphones** for audio output

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/alexa-mini.git
cd alexa-mini

Step 2: Create Virtual Environment

Windows:

python -m venv .venv
.venv\Scripts\activate

Mac/Linux:

python3 -m venv .venv
source .venv/bin/activate

Step 3: Install Dependencies

pip install -r requirements.txt

Step 4: Install PyAudio (Platform-Specific)

Windows:

pip install pipwin
pipwin install pyaudio

Mac:

brew install portaudio
pip install pyaudio

Linux (Ubuntu/Debian):

sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio

Step 5: Test Installation

python main.py

You should see:

🤖 ALEXA MINI - Single Command Mode
============================================================
🔄 Initializing Speech Recognition (Google)...
✅ Google Speech Recognition ready (FAST MODE)
🔄 Training intent classifier...
📊 Training with 144 samples
✅ Intent classifier trained (100.0% accuracy)
✅ Google TTS initialized (Natural Voice)
============================================================
✅ Ready!
============================================================

🚀 Usage

Basic Usage
Run the assistant:

Basic Usage
1. Run the assistant:

2. Wait for the prompt:

🔊 Alexa: Hello! How can I help you?
🎤 Listening...

3. Speak your command clearly
4. Alexa will respond and execute the task

Command Mode
Single Command Mode (Default):

Listens once
Executes command
Exits automatically
Continuous Mode (Optional):

Keeps listening
Say "stop" or "quit" to exit
Good for multiple tasks

📋 Commands

🎵 Music & Entertainment

"Play music"                    → Asks for platform
"Play music on Spotify"         → Opens Spotify
"Play Bohemian Rhapsody"        → Plays on YouTube
"Open Netflix"                  → Opens Netflix
"Watch a movie"                 → Shows platform options
"Tell me a joke"                → Programming jokes
"Tell me a fact"                → Interesting facts

📰 News & Information

"Show me news"                  → Asks for news type
"National news"                 → Indian news headlines
"International news"            → World news
"Sports news"                   → Sports updates
"Tech news"                     → Technology news
"Business news"                 → Financial news

🏏 Sports

"Cricket match"                 → Platform selection
"Live cricket score"            → Google search
"Cricket on Hotstar"            → Opens JioHotstar
"IPL score"                     → Live scores

🌐 Web & Social

"Open YouTube"                  → youtube.com
"Open Google"                   → google.com
"Open Instagram"                → instagram.com
"Open Gmail"                    → Gmail inbox
"Go to GitHub"                  → github.com

🛒 Shopping

"Shop on Amazon"                → amazon.in
"Buy something"                 → Platform selection
"Open Flipkart"                 → flipkart.com
"Myntra shopping"               → myntra.com

🌦️ Weather & Time

"What's the weather"            → Local weather
"Weather in Delhi"              → Delhi weather
"Temperature today"             → Current temp
"What time is it"               → Current time
"What's the date"               → Current date

🧮 Utilities

"Calculate 5 plus 3"            → "Answer: 8"
"10 times 7"                    → "Answer: 70"
"Divide 100 by 5"               → "Answer: 20"
"Set a timer for 5 minutes"     → Timer set
"Set an alarm for 7 AM"         → Alarm set
"Remind me to call"             → Reminder saved

🤖 Assistant Interaction

"Hello"                         → Greeting response
"How are you"                   → Status response
"Who are you"                   → Introduction
"Thank you"                     → "You're welcome!"
"Stop" / "Quit"                 → Exits assistant

⚙️ Configuration
Change Speech Recognition Engine
Edit main.py and replace AudioHandler class:

Option 1: Google Speech (Default - Fast)

# Already implemented - no changes needed

Option 2: Whisper (Offline - Slower)
# Uncomment whisper code in AudioHandler
# Install: pip install openai-whisper

Option 3: Faster-Whisper (Offline - Fast)

# Install: pip install faster-whisper
# Use FasterWhisperModel in AudioHandler

