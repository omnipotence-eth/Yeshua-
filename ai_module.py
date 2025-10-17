"""
AI module for intelligent verse selection using Ollama
"""

import ollama
import logging
import re
from typing import Optional, List, Dict, Any
from config import THEME_VERSE_SUGGESTIONS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIVerseSelector:
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.theme_suggestions = THEME_VERSE_SUGGESTIONS
        
        # Test Ollama connection
        try:
            self._test_ollama_connection()
        except Exception as e:
            logger.warning(f"Ollama connection test failed: {e}")
    
    def _test_ollama_connection(self):
        """Test if Ollama is running and model is available"""
        try:
            # Try to list models to test connection
            models = ollama.list()
            available_models = [model['name'] for model in models['models']]
            
            if self.model_name not in available_models:
                logger.warning(f"Model {self.model_name} not found. Available models: {available_models}")
                # Try to pull the model
                logger.info(f"Attempting to pull model {self.model_name}...")
                ollama.pull(self.model_name)
                logger.info(f"Successfully pulled model {self.model_name}")
            
            logger.info("Ollama connection successful")
            
        except Exception as e:
            logger.error(f"Ollama connection failed: {e}")
            raise
    
    def analyze_post_theme(self, post_text: str) -> str:
        """
        Analyze a social media post to extract relevant themes
        
        Args:
            post_text: Text content of the post
            
        Returns:
            Theme string (e.g., 'hope', 'wisdom', 'perseverance')
        """
        try:
            prompt = f"""
            Analyze this social media post and determine the most relevant biblical theme. 
            Choose from: hope, wisdom, perseverance, faith, love, peace, gratitude, strength, joy, grace, 
            forgiveness, market_crash, crypto, finance.
            
            Post: "{post_text}"
            
            Respond with only the theme name, nothing else.
            """
            
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            theme = response['message']['content'].strip().lower()
            
            # Validate theme
            valid_themes = list(self.theme_suggestions.keys())
            if theme not in valid_themes:
                logger.warning(f"AI returned invalid theme '{theme}', using fallback")
                theme = self._fallback_theme_analysis(post_text)
            
            logger.info(f"Analyzed post theme: {theme}")
            return theme
            
        except Exception as e:
            logger.error(f"Error analyzing post theme: {e}")
            return self._fallback_theme_analysis(post_text)
    
    def analyze_bnb_market_theme(self, bnb_data: dict) -> str:
        """
        Analyze BNB market data to determine relevant biblical theme
        
        Args:
            bnb_data: BNB market data dictionary
            
        Returns:
            Theme string based on market conditions
        """
        if not bnb_data:
            return 'faith'
        
        change_24h = bnb_data.get('price_change_percentage_24h', 0)
        volume_24h = bnb_data.get('total_volume', 0)
        
        # Determine theme based on market conditions
        if change_24h > 10:
            return 'gratitude'  # Very bullish
        elif change_24h > 5:
            return 'joy'  # Bullish
        elif change_24h > 0:
            return 'hope'  # Slightly bullish
        elif change_24h > -5:
            return 'patience'  # Slightly bearish
        elif change_24h > -10:
            return 'perseverance'  # Bearish
        else:
            return 'strength'  # Very bearish
    
    def select_news_relevant_verse(self, news_context: str, bnb_data: dict = None) -> str:
        """
        Select a Bible verse relevant to current news and BNB market conditions
        
        Args:
            news_context: Current news or market context
            bnb_data: BNB market data (optional)
            
        Returns:
            Bible verse reference
        """
        try:
            # Determine theme from news and market data
            if bnb_data:
                theme = self.analyze_bnb_market_theme(bnb_data)
            else:
                theme = self.analyze_post_theme(news_context)
            
            # Get verse for theme
            return self.suggest_verse_for_theme(theme)
            
        except Exception as e:
            logger.error(f"Error selecting news-relevant verse: {e}")
            return self._get_fallback_verse('hope')
    
    def _fallback_theme_analysis(self, post_text: str) -> str:
        """
        Fallback theme analysis using keyword matching
        
        Args:
            post_text: Text content of the post
            
        Returns:
            Theme string
        """
        text_lower = post_text.lower()
        
        # Keyword-based theme detection
        if any(word in text_lower for word in ['crash', 'drop', 'fall', 'bear', 'recession']):
            return 'market_crash'
        elif any(word in text_lower for word in ['bitcoin', 'crypto', 'blockchain', 'ethereum']):
            return 'crypto'
        elif any(word in text_lower for word in ['market', 'trading', 'investment', 'finance']):
            return 'finance'
        elif any(word in text_lower for word in ['hope', 'optimistic', 'bullish', 'recovery']):
            return 'hope'
        elif any(word in text_lower for word in ['wisdom', 'learn', 'insight', 'knowledge']):
            return 'wisdom'
        elif any(word in text_lower for word in ['persevere', 'patience', 'endure', 'difficult']):
            return 'perseverance'
        elif any(word in text_lower for word in ['faith', 'believe', 'trust', 'confidence']):
            return 'faith'
        elif any(word in text_lower for word in ['love', 'care', 'compassion', 'kindness']):
            return 'love'
        elif any(word in text_lower for word in ['peace', 'calm', 'serene', 'tranquil']):
            return 'peace'
        elif any(word in text_lower for word in ['thank', 'grateful', 'blessed', 'appreciate']):
            return 'gratitude'
        else:
            return 'wisdom'  # Default theme
    
    def suggest_verse_for_theme(self, theme: str) -> Optional[str]:
        """
        Use AI to suggest a Bible verse reference for a given theme
        
        Args:
            theme: Theme like 'hope', 'wisdom', 'perseverance'
            
        Returns:
            Bible verse reference (e.g., 'John 3:16') or None if failed
        """
        try:
            prompt = f"""
            Suggest a relevant Bible verse reference for the theme: {theme}
            
            Consider these themes and their meanings:
            - hope: optimism, future expectations, encouragement
            - wisdom: knowledge, understanding, good judgment
            - perseverance: endurance, persistence, overcoming challenges
            - faith: trust, belief, confidence in God
            - love: compassion, care, selflessness
            - peace: calm, tranquility, harmony
            - gratitude: thankfulness, appreciation, blessing
            - market_crash: financial loss, economic hardship, uncertainty
            - crypto: digital assets, technology, innovation
            - finance: money, investment, stewardship
            
            Respond with only the verse reference in format "Book Chapter:Verse" (e.g., "John 3:16").
            Choose a well-known, inspirational verse that fits the theme.
            """
            
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            verse_ref = response['message']['content'].strip()
            
            # Clean up the response
            verse_ref = re.sub(r'[^\w\s:]', '', verse_ref)  # Remove special characters
            verse_ref = re.sub(r'\s+', ' ', verse_ref)  # Normalize whitespace
            
            # Validate format
            if not re.match(r'^[A-Za-z0-9\s]+ \d+:\d+$', verse_ref):
                logger.warning(f"AI returned invalid verse format: {verse_ref}")
                return self._get_fallback_verse(theme)
            
            logger.info(f"AI suggested verse for theme '{theme}': {verse_ref}")
            return verse_ref
            
        except Exception as e:
            logger.error(f"Error getting AI verse suggestion for theme '{theme}': {e}")
            return self._get_fallback_verse(theme)
    
    def _get_fallback_verse(self, theme: str) -> Optional[str]:
        """
        Get fallback verse from predefined suggestions
        
        Args:
            theme: Theme string
            
        Returns:
            Bible verse reference or None
        """
        suggestions = self.theme_suggestions.get(theme.lower(), [])
        if suggestions:
            import random
            return random.choice(suggestions)
        
        # Ultimate fallback
        fallback_verses = ['John 3:16', 'Psalms 23:1', 'Romans 8:28']
        import random
        return random.choice(fallback_verses)
    
    def get_daily_theme(self) -> str:
        """
        Get theme for the current day
        
        Returns:
            Theme string based on day of week
        """
        from datetime import datetime
        from config import DAILY_THEMES
        
        day_name = datetime.now().strftime('%A').lower()
        return DAILY_THEMES.get(day_name, 'wisdom')
    
    def is_relevant_for_interaction(self, post_text: str) -> bool:
        """
        Determine if a post is relevant for Bible verse interaction
        
        Args:
            post_text: Text content of the post
            
        Returns:
            True if post is relevant for interaction
        """
        try:
            prompt = f"""
            Determine if this social media post is appropriate for a respectful Bible verse response.
            Consider if the post is:
            - About finance, crypto, markets, or business
            - Positive or neutral in tone
            - Not offensive or controversial
            - Suitable for inspirational content
            
            Post: "{post_text}"
            
            Respond with only "yes" or "no".
            """
            
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            result = response['message']['content'].strip().lower()
            is_relevant = result in ['yes', 'true', '1']
            
            logger.info(f"Post relevance check: {is_relevant}")
            return is_relevant
            
        except Exception as e:
            logger.error(f"Error checking post relevance: {e}")
            # Fallback: check for basic keywords
            text_lower = post_text.lower()
            relevant_keywords = ['market', 'crypto', 'bitcoin', 'finance', 'trading', 'investment', 'business']
            return any(keyword in text_lower for keyword in relevant_keywords)
