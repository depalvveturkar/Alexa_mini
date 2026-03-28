import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
import pickle
import os
from config import DATASET_PATH, MODEL_SAVE_PATH, VECTORIZER_SAVE_PATH, MLP_HIDDEN_LAYERS, MLP_MAX_ITER, DEBUG_MODE

class IntentClassifier:
    def __init__(self):
        """Initialize intent classifier"""
        self.vectorizer = None
        self.model = None
        self.load_or_train()
    
    def load_or_train(self):
        """Load existing model or train new one"""
        # Try to load existing model
        if os.path.exists(MODEL_SAVE_PATH) and os.path.exists(VECTORIZER_SAVE_PATH):
            print("🔄 Loading existing model...")
            try:
                with open(MODEL_SAVE_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                with open(VECTORIZER_SAVE_PATH, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                print("✅ Model loaded successfully")
                return
            except Exception as e:
                print(f"⚠️ Error loading model: {e}")
                print("🔄 Training new model...")
        
        # Train new model
        self.train_model()
    
    def train_model(self):
        """Train intent classification model"""
        try:
            print("🔄 Loading training data...")
            
            if not os.path.exists(DATASET_PATH):
                print(f"❌ Dataset not found: {DATASET_PATH}")
                print("📝 Creating sample dataset...")
                self.create_sample_dataset()
            
            alexa_df = pd.read_csv(DATASET_PATH)
            
            if DEBUG_MODE:
                print(f"📊 Dataset shape: {alexa_df.shape}")
                print(f"📊 Intents: {alexa_df['intent'].unique()}")
            
            # Vectorization
            print("🔄 Vectorizing text...")
            self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
            X = self.vectorizer.fit_transform(alexa_df['prompt'])
            y = alexa_df['intent']
            
            # Training
            print("🔄 Training model...")
            self.model = MLPClassifier(
                hidden_layer_sizes=MLP_HIDDEN_LAYERS,
                max_iter=MLP_MAX_ITER,
                random_state=42,
                early_stopping=True,
                validation_fraction=0.1
            )
            self.model.fit(X, y)
            
            print(f"✅ Model trained successfully (accuracy: {self.model.score(X, y):.2%})")
            
            # Save model
            self.save_model()
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
    
    def save_model(self):
        """Save model and vectorizer"""
        try:
            os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
            
            with open(MODEL_SAVE_PATH, 'wb') as f:
                pickle.dump(self.model, f)
            with open(VECTORIZER_SAVE_PATH, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            
            print("✅ Model saved successfully")
        except Exception as e:
            print(f"❌ Error saving model: {e}")
    
    def predict_intent(self, text):
        """Predict intent from text"""
        if not self.model or not self.vectorizer:
            print("❌ Model not loaded")
            return "unknown"
        
        try:
            X_test = self.vectorizer.transform([text])
            intent = self.model.predict(X_test)[0]
            
            if DEBUG_MODE:
                # Get confidence scores
                probabilities = self.model.predict_proba(X_test)[0]
                confidence = max(probabilities)
                print(f'🎯 Detected Intent: {intent} (confidence: {confidence:.2%})')
            
            return intent
        except Exception as e:
            print(f"❌ Error predicting intent: {e}")
            return "unknown"
    
    def create_sample_dataset(self):
        """Create a sample dataset if none exists"""
        sample_data = {
            'prompt': [
                # Play music
                'play music', 'play a song', 'play some music', 'start music',
                'play my favorite song', 'play spotify', 'play on youtube',
                
                # Open website
                'open youtube', 'open google', 'open github', 'go to youtube',
                'launch spotify', 'open netflix', 'go to amazon',
                
                # Jokes
                'tell me a joke', 'make me laugh', 'say something funny',
                'tell a joke', 'joke please',
                
                # News
                'news', 'tell me the news', 'what\'s happening', 'latest headlines',
                'show me news', 'national news', 'international news',
                
                # Cricket
                'cricket score', 'cricket match', 'ipl live', 'show cricket',
                'cricket on hotstar', 'live cricket score',
                
                # Movies
                'movie', 'watch a movie', 'show movies', 'netflix movies',
                'prime video', 'hotstar shows',
                
                # Shopping
                'shop on amazon', 'buy something', 'flipkart', 'myntra',
                'i want to shop', 'order online',
                
                # Weather
                'weather', 'temperature', 'how\'s the weather', 'forecast',
                'weather in delhi', 'temperature today',
                
                # Time/Date
                'what time is it', 'tell me the time', 'what\'s the date',
                'what day is it', 'current time',
                
                # Timer
                'set a timer', 'timer for 5 minutes', 'countdown timer',
                
                # Alarm
                'set an alarm', 'alarm for 7 am', 'wake me up at 6',
                
                # Reminder
                'remind me', 'set a reminder', 'reminder to call',
                
                # Calculator
                'calculate 5 plus 3', '10 times 2', 'what is 15 divided by 3',
                'multiply 7 by 8', '100 minus 45',
                
                # Facts
                'tell me a fact', 'interesting fact', 'did you know',
                
                # Personality
                'how are you', 'who are you', 'what\'s your name',
                
                # General QA
                'who is elon musk', 'what is python', 'search for recipes',
                'tell me about india'
            ],
            'intent': [
                # Corresponding intents
                'play_music', 'play_music', 'play_music', 'play_music',
                'play_music', 'play_music', 'play_music',
                
                'open_website', 'open_website', 'open_website', 'open_website',
                'open_website', 'open_website', 'open_website',
                
                'jokes_fun', 'jokes_fun', 'jokes_fun', 'jokes_fun', 'jokes_fun',
                
                'news', 'news', 'news', 'news', 'news', 'news', 'news',
                
                'cricket', 'cricket', 'cricket', 'cricket', 'cricket', 'cricket',
                
                'movies', 'movies', 'movies', 'movies', 'movies', 'movies',
                
                'shopping', 'shopping', 'shopping', 'shopping', 'shopping', 'shopping',
                
                'weather', 'weather', 'weather', 'weather', 'weather', 'weather',
                
                'date_time', 'date_time', 'date_time', 'date_time', 'date_time',
                
                'set_timer', 'set_timer', 'set_timer',
                
                'alarm', 'alarm', 'alarm',
                
                'reminder', 'reminder', 'reminder',
                
                'calculator', 'calculator', 'calculator', 'calculator', 'calculator',
                
                'facts', 'facts', 'facts',
                
                'personality', 'personality', 'personality',
                
                'general_qa', 'general_qa', 'general_qa', 'general_qa'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        df.to_csv(DATASET_PATH, index=False)
        print(f"✅ Sample dataset created at {DATASET_PATH}")