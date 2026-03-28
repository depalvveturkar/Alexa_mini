import webbrowser
import datetime
import random
import re
from modules.conversation_manager import ConversationManager
from config import DEBUG_MODE

class ActionHandler:
    def __init__(self):
        """Initialize action handler"""
        self.conv_manager = ConversationManager()
        self.shopping_list = []
    
    def handle_follow_up(self, user_input):
        """Handle follow-up responses"""
        user_input_lower = user_input.lower().strip()
        context = self.conv_manager.get_context()
        
        if DEBUG_MODE:
            print(f"🔄 Handling follow-up for context: {context}")
        
        # NEWS FOLLOW-UP
        if context == "news_type":
            self.conv_manager.reset_state()
            
            if "national" in user_input_lower or "india" in user_input_lower:
                webbrowser.open("https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hwbEVnSmxiaWdBUAE?hl=en-IN&gl=IN")
                return "Here are today's national headlines from India"
            
            elif "international" in user_input_lower or "world" in user_input_lower or "global" in user_input_lower:
                webbrowser.open("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN")
                return "Here are today's international headlines"
            
            elif "sports" in user_input_lower:
                webbrowser.open("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN")
                return "Here are the latest sports news"
            
            elif "tech" in user_input_lower or "technology" in user_input_lower:
                webbrowser.open("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN")
                return "Here are the latest technology news"
            
            elif "business" in user_input_lower or "finance" in user_input_lower:
                webbrowser.open("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN")
                return "Here are the latest business news"
            
            else:
                webbrowser.open("https://news.google.com")
                return "Here are today's top headlines"
        
        # MUSIC PLATFORM FOLLOW-UP
        elif context == "music_platform":
            song_query = self.conv_manager.get_data("song")
            self.conv_manager.reset_state()
            
            if "spotify" in user_input_lower:
                if song_query:
                    webbrowser.open(f"https://open.spotify.com/search/{song_query.replace(' ', '%20')}")
                    return f"Searching '{song_query}' on Spotify"
                else:
                    webbrowser.open("https://open.spotify.com")
                    return "Opening Spotify"
            
            elif "youtube" in user_input_lower or "yt" in user_input_lower:
                if song_query:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={song_query.replace(' ', '+')}")
                    return f"Playing '{song_query}' on YouTube"
                else:
                    webbrowser.open("https://www.youtube.com/results?search_query=music")
                    return "Playing music on YouTube"
            
            elif "jio" in user_input_lower or "saavn" in user_input_lower:
                if song_query:
                    webbrowser.open(f"https://www.jiosaavn.com/search/{song_query.replace(' ', '%20')}")
                    return f"Searching '{song_query}' on JioSaavn"
                else:
                    webbrowser.open("https://www.jiosaavn.com")
                    return "Opening JioSaavn"
            
            elif "gaana" in user_input_lower:
                if song_query:
                    webbrowser.open(f"https://gaana.com/search/{song_query.replace(' ', '%20')}")
                    return f"Searching '{song_query}' on Gaana"
                else:
                    webbrowser.open("https://gaana.com")
                    return "Opening Gaana"
            
            else:
                # Default to YouTube
                if song_query:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={song_query.replace(' ', '+')}")
                    return f"Playing '{song_query}' on YouTube"
                else:
                    webbrowser.open("https://www.youtube.com/results?search_query=music")
                    return "Playing music on YouTube"
        
        # SPORTS PLATFORM FOLLOW-UP
        elif context == "sports_platform":
            self.conv_manager.reset_state()
            
            if "hotstar" in user_input_lower or "jio" in user_input_lower:
                webbrowser.open("https://www.hotstar.com/in/sports/cricket")
                return "Opening JioHotstar for live cricket"
            
            elif "espn" in user_input_lower or "cricinfo" in user_input_lower:
                webbrowser.open("https://www.espncricinfo.com/live-cricket-score")
                return "Opening ESPNCricinfo for live scores"
            
            elif "cricbuzz" in user_input_lower:
                webbrowser.open("https://www.cricbuzz.com/cricket-match/live-scores")
                return "Opening Cricbuzz for live scores"
            
            else:
                webbrowser.open("https://www.hotstar.com/in/sports/cricket")
                return "Opening JioHotstar for cricket"
        
        # SHOPPING PLATFORM FOLLOW-UP
        elif context == "shopping_platform":
            product_query = self.conv_manager.get_data("product")
            self.conv_manager.reset_state()
            
            if "amazon" in user_input_lower:
                if product_query:
                    webbrowser.open(f"https://www.amazon.in/s?k={product_query.replace(' ', '+')}")
                    return f"Searching '{product_query}' on Amazon"
                else:
                    webbrowser.open("https://www.amazon.in")
                    return "Opening Amazon"
            
            elif "flipkart" in user_input_lower:
                if product_query:
                    webbrowser.open(f"https://www.flipkart.com/search?q={product_query.replace(' ', '+')}")
                    return f"Searching '{product_query}' on Flipkart"
                else:
                    webbrowser.open("https://www.flipkart.com")
                    return "Opening Flipkart"
            
            elif "myntra" in user_input_lower:
                if product_query:
                    webbrowser.open(f"https://www.myntra.com/{product_query.replace(' ', '-')}")
                    return f"Searching '{product_query}' on Myntra"
                else:
                    webbrowser.open("https://www.myntra.com")
                    return "Opening Myntra"
            
            else:
                if product_query:
                    webbrowser.open(f"https://www.amazon.in/s?k={product_query.replace(' ', '+')}")
                    return f"Searching '{product_query}' on Amazon"
                else:
                    webbrowser.open("https://www.amazon.in")
                    return "Opening Amazon"
        
        # VIDEO PLATFORM FOLLOW-UP
        elif context == "video_platform":
            movie_query = self.conv_manager.get_data("movie")
            self.conv_manager.reset_state()
            
            if "netflix" in user_input_lower:
                webbrowser.open("https://www.netflix.com")
                return "Opening Netflix"
            
            elif "prime" in user_input_lower or "amazon" in user_input_lower:
                webbrowser.open("https://www.primevideo.com")
                return "Opening Amazon Prime Video"
            
            elif "hotstar" in user_input_lower or "disney" in user_input_lower:
                webbrowser.open("https://www.hotstar.com")
                return "Opening Disney+ Hotstar"
            
            elif "youtube" in user_input_lower:
                if movie_query:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={movie_query.replace(' ', '+')}")
                    return f"Searching '{movie_query}' on YouTube"
                else:
                    webbrowser.open("https://www.youtube.com")
                    return "Opening YouTube"
            
            else:
                webbrowser.open("https://www.imdb.com/chart/top/")
                return "Here are some popular movies on IMDb"
        
        # No matching context
        self.conv_manager.reset_state()
        return None
    
    def perform_action(self, intent, prompt=""):
        """Execute action based on intent"""
        
        # Check for follow-up
        if self.conv_manager.is_awaiting_response():
            follow_up_result = self.handle_follow_up(prompt)
            if follow_up_result:
                return follow_up_result
        
        # PLAY MUSIC
        if intent == "play_music":
            prompt_lower = prompt.lower()
            
            # Extract song name
            song_match = re.search(r"play\s+(.+?)(?:\s+on|\s+in|\s*$)", prompt_lower)
            song_name = ""
            if song_match:
                song_name = song_match.group(1).strip()
                song_name = re.sub(r'\b(song|music|the)\b', '', song_name).strip()
            
            # Check if platform specified
            if "spotify" in prompt_lower:
                if song_name:
                    webbrowser.open(f"https://open.spotify.com/search/{song_name.replace(' ', '%20')}")
                    return f"Playing '{song_name}' on Spotify"
                else:
                    webbrowser.open("https://open.spotify.com")
                    return "Opening Spotify"
            
            elif "youtube" in prompt_lower:
                if song_name:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}")
                    return f"Playing '{song_name}' on YouTube"
                else:
                    webbrowser.open("https://www.youtube.com/results?search_query=music")
                    return "Playing music on YouTube"
            
            elif "jiosaavn" in prompt_lower or "saavn" in prompt_lower:
                if song_name:
                    webbrowser.open(f"https://www.jiosaavn.com/search/{song_name.replace(' ', '%20')}")
                    return f"Playing '{song_name}' on JioSaavn"
                else:
                    webbrowser.open("https://www.jiosaavn.com")
                    return "Opening JioSaavn"
            
            else:
                # Ask for platform
                self.conv_manager.set_state("music_platform", {"song": song_name})
                return "Which platform would you like? Spotify, YouTube, JioSaavn, or Gaana?"
        
        # OPEN WEBSITE
        elif intent == "open_website":
            prompt_lower = prompt.lower()
            
            websites = {
                "youtube": "https://www.youtube.com",
                "google": "https://www.google.com",
                "github": "https://www.github.com",
                "spotify": "https://open.spotify.com",
                "netflix": "https://www.netflix.com",
                "amazon": "https://www.amazon.in",
                "flipkart": "https://www.flipkart.com",
                "hotstar": "https://www.hotstar.com",
                "instagram": "https://www.instagram.com",
                "twitter": "https://www.twitter.com",
                "linkedin": "https://www.linkedin.com",
                "facebook": "https://www.facebook.com",
                "whatsapp": "https://web.whatsapp.com"
            }
            
            for site, url in websites.items():
                if site in prompt_lower:
                    webbrowser.open(url)
                    return f"Opening {site.title()}"
            
            return "Which website would you like me to open?"
        
        # JOKES
        elif intent == "jokes_fun":
            jokes = [
                "Why did the computer get cold? Because it forgot to close Windows!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "I told my AI assistant a joke… it said, processing humor module.",
                "Why do Java developers wear glasses? Because they can't C#!",
                "A SQL query walks into a bar, walks up to two tables and asks, Can I join you?",
                "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
            ]
            return random.choice(jokes)
        
        # NEWS
        elif intent == "news":
            prompt_lower = prompt.lower()
            
            if "national" in prompt_lower or "india" in prompt_lower:
                webbrowser.open("https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hwbEVnSmxiaWdBUAE?hl=en-IN&gl=IN")
                return "Here are today's national headlines"
            
            elif "international" in prompt_lower or "world" in prompt_lower:
                webbrowser.open("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN")
                return "Here are today's international headlines"
            
            elif "sports" in prompt_lower:
                webbrowser.open("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN")
                return "Here are the latest sports news"
            
            elif "tech" in prompt_lower:
                webbrowser.open("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN")
                return "Here are the latest technology news"
            
            else:
                self.conv_manager.set_state("news_type")
                return "Which news would you like? National, International, Sports, Tech, or Business?"
        
        # CRICKET
        elif intent == "cricket":
            prompt_lower = prompt.lower()
            
            if "hotstar" in prompt_lower or "jio" in prompt_lower:
                webbrowser.open("https://www.hotstar.com/in/sports/cricket")
                return "Opening JioHotstar for live cricket"
            
            elif "cricbuzz" in prompt_lower:
                webbrowser.open("https://www.cricbuzz.com/cricket-match/live-scores")
                return "Opening Cricbuzz for live scores"
            
            elif "score" in prompt_lower:
                webbrowser.open("https://www.google.com/search?q=live+cricket+score")
                return "Here are the live cricket scores"
            
            else:
                self.conv_manager.set_state("sports_platform")
                return "Where would you like to watch? JioHotstar for live match, or Cricbuzz for scores?"
        
        # MOVIES
        elif intent == "movies":
            prompt_lower = prompt.lower()
            
            movie_match = re.search(r"(?:watch|play|show)\s+(.+?)(?:\s+on|\s*$)", prompt_lower)
            movie_name = movie_match.group(1).strip() if movie_match else ""
            
            if "netflix" in prompt_lower:
                webbrowser.open("https://www.netflix.com")
                return "Opening Netflix"
            elif "prime" in prompt_lower:
                webbrowser.open("https://www.primevideo.com")
                return "Opening Amazon Prime Video"
            elif "hotstar" in prompt_lower:
                webbrowser.open("https://www.hotstar.com")
                return "Opening Disney+ Hotstar"
            else:
                self.conv_manager.set_state("video_platform", {"movie": movie_name})
                return "Which platform? Netflix, Prime Video, Disney+ Hotstar, or YouTube?"
        
        # SHOPPING
        elif intent == "shopping":
            prompt_lower = prompt.lower()
            
            product_match = re.search(r"(?:buy|shop|search|find)\s+(.+?)(?:\s+on|\s*$)", prompt_lower)
            product_name = product_match.group(1).strip() if product_match else ""
            
            if "amazon" in prompt_lower:
                if product_name:
                    webbrowser.open(f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}")
                    return f"Searching '{product_name}' on Amazon"
                else:
                    webbrowser.open("https://www.amazon.in")
                    return "Opening Amazon"
            elif "flipkart" in prompt_lower:
                webbrowser.open("https://www.flipkart.com")
                return "Opening Flipkart"
            else:
                self.conv_manager.set_state("shopping_platform", {"product": product_name})
                if product_name:
                    return f"Where would you like to buy '{product_name}'? Amazon, Flipkart, or Myntra?"
                return "Which platform? Amazon, Flipkart, or Myntra?"
        
        # TIMER
        elif intent == "set_timer":
            minutes = re.findall(r'\d+', prompt)
            minutes = int(minutes[0]) if minutes else 1
            return f"Timer set for {minutes} minutes"
        
        # ALARM
        elif intent == "alarm":
            time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', prompt.lower())
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                period = time_match.group(3) if time_match.group(3) else "am"
                return f"Alarm set for {hour}:{str(minute).zfill(2)} {period.upper()}"
            return "Alarm set"
        
        # REMINDER
        elif intent == "reminder":
            return "Reminder saved"
        
        # DATE TIME
        elif intent == "date_time":
            now = datetime.datetime.now()
            return f"It's {now.strftime('%I:%M %p')} on {now.strftime('%B %d, %Y')}"
        
        # WEATHER
        elif intent == "weather":
            prompt_lower = prompt.lower()
            match = re.search(r"(in|of|for)\s+([a-zA-Z\s]+)", prompt_lower)
            
            if match:
                city = match.group(2).strip()
                webbrowser.open(f"https://www.google.com/search?q=weather+in+{city.replace(' ', '+')}")
                return f"Showing weather in {city.title()}"
            else:
                webbrowser.open("https://www.google.com/search?q=weather+today")
                return "Here's the latest weather forecast"
        
        # GENERAL QA
        elif intent == "general_qa":
            query = prompt.replace(" ", "+")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return "Here's what I found"
        
        # FACTS
        elif intent == "facts":
            facts = [
                "Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs!",
                "Bananas are berries, but strawberries are not.",
                "Octopuses have three hearts and blue blood.",
                "A day on Venus is longer than a year on Venus.",
            ]
            return random.choice(facts)
        
        # CALCULATOR
        elif intent == "calculator":
            nums = list(map(float, re.findall(r'\d+\.?\d*', prompt)))
            prompt_lower = prompt.lower()
            
            if len(nums) >= 2:
                if "plus" in prompt_lower or "add" in prompt_lower:
                    result = nums[0] + nums[1]
                    return f"The answer is {int(result) if result.is_integer() else result}"
                elif "minus" in prompt_lower or "subtract" in prompt_lower:
                    result = nums[0] - nums[1]
                    return f"The answer is {int(result) if result.is_integer() else result}"
                elif "times" in prompt_lower or "multiply" in prompt_lower:
                    result = nums[0] * nums[1]
                    return f"The answer is {int(result) if result.is_integer() else result}"
                elif "divide" in prompt_lower:
                    if nums[1] != 0:
                        result = nums[0] / nums[1]
                        return f"The answer is {int(result) if result.is_integer() else round(result, 2)}"
                    else:
                        return "Cannot divide by zero!"
            
            return "Sorry, I couldn't calculate that"
        
        # PERSONALITY
        elif intent == "personality":
            responses = [
                "I'm doing great! Ready to help you.",
                "I'm your friendly AI assistant!",
                "I was created to make your life easier.",
            ]
            return random.choice(responses)
        
        # UNKNOWN
        else:
            return "Sorry, I didn't understand that. Try asking about news, music, weather, or cricket!"