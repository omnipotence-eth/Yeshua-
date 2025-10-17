"""
Bible API integration for fetching Chinese verses
"""

import requests
import random
import logging
from typing import Optional, Dict, Any
from config import CHINESE_BOOK_MAP, THEME_VERSE_SUGGESTIONS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BibleAPI:
    def __init__(self):
        self.base_url = "https://bible-api.com"
        self.chinese_book_map = CHINESE_BOOK_MAP
        self.theme_suggestions = THEME_VERSE_SUGGESTIONS
    
    def get_verse_by_reference(self, book: str, chapter: int, verse: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a specific Bible verse
        
        Args:
            book: English book name (e.g., 'john')
            chapter: Chapter number
            verse: Verse number
            
        Returns:
            Dict with verse text and reference, or None if failed
        """
        try:
            # Convert English book name to Chinese
            chinese_book = self.chinese_book_map.get(book.lower())
            if not chinese_book:
                logger.error(f"Unknown book: {book}")
                return None
            
            # Use English format for bible-api.com
            english_reference = f"{book} {chapter}:{verse}"
            url = f"{self.base_url}/{english_reference}"
            
            logger.info(f"Fetching verse: {url}")
            response = requests.get(url, timeout=10)
            
            response.raise_for_status()
            data = response.json()
            
            return {
                'text': data.get('text', '').strip(),
                'reference': data.get('reference', english_reference),
                'book': chinese_book,
                'chapter': chapter,
                'verse': verse
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching verse {book} {chapter}:{verse}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching verse: {e}")
            return None
    
    def get_verse_by_theme(self, theme: str) -> Optional[Dict[str, Any]]:
        """
        Get a random verse based on theme
        
        Args:
            theme: Theme like 'hope', 'wisdom', 'perseverance'
            
        Returns:
            Dict with verse text and reference, or None if failed
        """
        try:
            # Get suggested verses for theme
            suggestions = self.theme_suggestions.get(theme.lower(), [])
            if not suggestions:
                logger.warning(f"No suggestions for theme: {theme}")
                return self.get_random_verse()
            
            # Pick a random suggestion
            verse_ref = random.choice(suggestions)
            logger.info(f"Selected verse for theme '{theme}': {verse_ref}")
            
            # Parse reference (e.g., "John 3:16" -> book="john", chapter=3, verse=16)
            parts = verse_ref.split()
            if len(parts) < 2:
                logger.error(f"Invalid verse reference format: {verse_ref}")
                return self.get_random_verse()
            
            book = parts[0].lower()
            chapter_verse = parts[1].split(':')
            
            if len(chapter_verse) != 2:
                logger.error(f"Invalid chapter:verse format: {parts[1]}")
                return self.get_random_verse()
            
            try:
                chapter = int(chapter_verse[0])
                verse = int(chapter_verse[1])
            except ValueError:
                logger.error(f"Invalid chapter or verse number: {chapter_verse}")
                return self.get_random_verse()
            
            return self.get_verse_by_reference(book, chapter, verse)
            
        except Exception as e:
            logger.error(f"Error getting verse by theme '{theme}': {e}")
            return self.get_random_verse()
    
    def get_random_verse(self) -> Optional[Dict[str, Any]]:
        """
        Get a random popular verse as fallback
        
        Returns:
            Dict with verse text and reference, or None if failed
        """
        popular_verses = [
            ('john', 3, 16),
            ('psalms', 23, 1),
            ('romans', 8, 28),
            ('philippians', 4, 13),
            ('jeremiah', 29, 11),
            ('proverbs', 3, 5),
            ('matthew', 28, 20),
            ('isaiah', 40, 31)
        ]
        
        book, chapter, verse = random.choice(popular_verses)
        logger.info(f"Fetching random verse: {book} {chapter}:{verse}")
        
        return self.get_verse_by_reference(book, chapter, verse)
    
    def format_verse_for_post(self, verse_data: Dict[str, Any]) -> tuple[str, str]:
        """
        Format verse data for X thread (English and Chinese)
        
        Args:
            verse_data: Dict containing verse text and reference
            
        Returns:
            Tuple of (english_post, chinese_post)
        """
        if not verse_data:
            english_post = "The Lord is my shepherd; I shall not want.\n\n— Psalm 23:1"
            chinese_post = "耶和华是我的牧者，我必不致缺乏。\n\n— 诗篇 23:1"
            return english_post, chinese_post
        
        text = verse_data.get('text', '')
        reference = verse_data.get('reference', '')
        chinese_book = verse_data.get('book', '')
        chapter = verse_data.get('chapter', 0)
        verse = verse_data.get('verse', 0)
        
        # English post
        english_post = f"{text}\n\n— {reference}"
        
        # Chinese post - get the Chinese translation of the same verse
        chinese_verse = self.get_chinese_translation(chinese_book, chapter, verse)
        chinese_reference = f"{chinese_book} {chapter}:{verse}"
        chinese_post = f"{chinese_verse}\n\n— {chinese_reference}"
        
        return english_post, chinese_post
    
    def get_chinese_translation(self, chinese_book: str, chapter: int, verse: int) -> str:
        """
        Get Chinese translation for a specific verse
        
        Args:
            chinese_book: Chinese book name
            chapter: Chapter number
            verse: Verse number
            
        Returns:
            Chinese verse text
        """
        # Map of popular verses with their Chinese translations
        chinese_translations = {
            # Mark 11:22
            ('马可福音', 11, 22): '耶稣回答说：你们当信服神。',
            # Hebrews 11:1
            ('希伯来书', 11, 1): '信就是所望之事的实底，是未见之事的确据。',
            # John 3:16
            ('约翰福音', 3, 16): '神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不至灭亡，反得永生。',
            # Psalm 23:1
            ('诗篇', 23, 1): '耶和华是我的牧者，我必不致缺乏。',
            # Romans 8:28
            ('罗马书', 8, 28): '我们晓得万事都互相效力，叫爱神的人得益处。',
            # Philippians 4:13
            ('腓立比书', 4, 13): '我靠着那加给我力量的，凡事都能做。',
            # Jeremiah 29:11
            ('耶利米书', 29, 11): '耶和华说：我知道我向你们所怀的意念是赐平安的意念，不是降灾祸的意念。',
            # Proverbs 3:5
            ('箴言', 3, 5): '你要专心仰赖耶和华，不可倚靠自己的聪明。',
            # Matthew 11:28
            ('马太福音', 11, 28): '凡劳苦担重担的人可以到我这里来，我就使你们得安息。',
            # Isaiah 40:31
            ('以赛亚书', 40, 31): '但那等候耶和华的必从新得力。他们必如鹰展翅上腾。',
            # 2 Corinthians 5:7
            ('哥林多后书', 5, 7): '因我们行事为人是凭着信心，不是凭着眼见。',
            # Matthew 28:20
            ('马太福音', 28, 20): '凡我所吩咐你们的，都教训他们遵守，我就常与你们同在，直到世界的末了。',
            # Romans 10:17
            ('罗马书', 10, 17): '可见信道是从听道来的，听道是从基督的话来的。',
            # Galatians 2:20
            ('加拉太书', 2, 20): '我已经与基督同钉十字架，现在活着的不再是我，乃是基督在我里面活着。',
            # Ephesians 2:8
            ('以弗所书', 2, 8): '你们得救是本乎恩，也因着信。这并不是出于自己，乃是神所赐的。',
        }
        
        # Try to find the exact translation
        key = (chinese_book, chapter, verse)
        if key in chinese_translations:
            return chinese_translations[key]
        
        # Fallback to a popular verse if exact match not found
        fallback_verses = [
            '耶和华是我的牧者，我必不致缺乏。',
            '神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不至灭亡，反得永生。',
            '我们晓得万事都互相效力，叫爱神的人得益处。',
            '我靠着那加给我力量的，凡事都能做。',
            '耶和华说：我知道我向你们所怀的意念是赐平安的意念，不是降灾祸的意念。'
        ]
        
        import random
        return random.choice(fallback_verses)
    
    def get_popular_chinese_verse(self) -> Dict[str, Any]:
        """
        Get a popular Chinese Bible verse
        
        Returns:
            Dict with Chinese verse data
        """
        popular_chinese_verses = [
            {'text': '耶和华是我的牧者，我必不致缺乏。', 'reference': '诗篇 23:1'},
            {'text': '神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不至灭亡，反得永生。', 'reference': '约翰福音 3:16'},
            {'text': '我们晓得万事都互相效力，叫爱神的人得益处。', 'reference': '罗马书 8:28'},
            {'text': '我靠着那加给我力量的，凡事都能做。', 'reference': '腓立比书 4:13'},
            {'text': '耶和华说：我知道我向你们所怀的意念是赐平安的意念，不是降灾祸的意念。', 'reference': '耶利米书 29:11'},
            {'text': '你要专心仰赖耶和华，不可倚靠自己的聪明。', 'reference': '箴言 3:5'},
            {'text': '凡劳苦担重担的人可以到我这里来，我就使你们得安息。', 'reference': '马太福音 11:28'},
            {'text': '但那等候耶和华的必从新得力。他们必如鹰展翅上腾。', 'reference': '以赛亚书 40:31'}
        ]
        
        import random
        return random.choice(popular_chinese_verses)
    
    def get_chinese_verse(self, english_reference: str) -> Optional[Dict[str, Any]]:
        """
        Get Chinese version of an English verse reference
        
        Args:
            english_reference: English verse reference (e.g., "John 3:16")
            
        Returns:
            Chinese verse data or None if failed
        """
        try:
            # Parse the English reference
            parts = english_reference.split()
            if len(parts) < 2:
                return None
            
            book = parts[0].lower()
            chapter_verse = parts[1].split(':')
            
            if len(chapter_verse) != 2:
                return None
            
            try:
                chapter = int(chapter_verse[0])
                verse = int(chapter_verse[1])
            except ValueError:
                return None
            
            # Get the Chinese verse using the same book/chapter/verse
            return self.get_verse_by_reference(book, chapter, verse)
            
        except Exception as e:
            logger.error(f"Error getting Chinese verse for {english_reference}: {e}")
            return None
    
    def format_verse_for_reply(self, verse_data: Dict[str, Any], theme: str) -> str:
        """
        Format verse data for X reply
        
        Args:
            verse_data: Dict containing verse text and reference
            theme: Theme that inspired the verse
            
        Returns:
            Formatted string for reply
        """
        if not verse_data:
            return f"耶和华是我的牧者，我必不致缺乏。\n\n— 诗篇 23:1"
        
        text = verse_data.get('text', '')
        reference = verse_data.get('reference', '')
        
        return f"{text}\n\n— {reference}"
