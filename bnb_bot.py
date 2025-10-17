"""
BNB-Focused Bible Verse Bot
Combines spiritual inspiration with BNB market analysis and insights
"""

import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

from x_api import XAPI
from bible_api import BibleAPI
from ai_module import AIVerseSelector
from bnb_analysis import BNBAnalysis
from config import API_LIMITS, TARGET_ACCOUNTS, DAILY_THEMES, THEME_VERSE_SUGGESTIONS

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bnb_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BNBBibleBot:
    def __init__(self):
        """Initialize the BNB-focused Bible verse bot"""
        self.x_api = XAPI()
        self.bible_api = BibleAPI()
        self.ai_module = AIVerseSelector()
        self.bnb_analysis = BNBAnalysis()
        
        # Usage tracking
        self.usage_file = 'api_usage.json'
        self.usage = self.load_usage()
        
        # Calculate daily limits
        self.daily_post_limit = API_LIMITS['daily_posts']
        self.daily_read_limit = API_LIMITS['daily_reads']
        self.posts_per_thread = API_LIMITS['posts_per_thread']
        
        logger.info(f"BNB Bible Bot initialized - Daily limits: {self.daily_post_limit} posts, {self.daily_read_limit} reads")

    def load_usage(self) -> Dict:
        """Load API usage from file"""
        try:
            if os.path.exists(self.usage_file):
                with open(self.usage_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading usage file: {e}")
        
        # Initialize with current month
        current_month = datetime.now().strftime('%Y-%m')
        return {
            'month': current_month,
            'posts_used': 0,
            'reads_used': 0,
            'last_reset': datetime.now().isoformat()
        }

    def save_usage(self):
        """Save API usage to file"""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(self.usage, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving usage file: {e}")

    def reset_monthly_usage(self):
        """Reset usage counter for new month"""
        current_month = datetime.now().strftime('%Y-%m')
        if self.usage['month'] != current_month:
            self.usage = {
                'month': current_month,
                'posts_used': 0,
                'reads_used': 0,
                'last_reset': datetime.now().isoformat()
            }
            self.save_usage()
            logger.info(f"Reset usage for new month: {current_month}")

    def can_post(self, posts_needed: int = 1) -> bool:
        """Check if we can post without exceeding limits"""
        self.reset_monthly_usage()
        
        # Check monthly limit
        if self.usage['posts_used'] + posts_needed > API_LIMITS['monthly_posts']:
            logger.warning(f"Monthly post limit reached: {self.usage['posts_used']}/{API_LIMITS['monthly_posts']}")
            return False
        
        # Check daily limit
        today = datetime.now().strftime('%Y-%m-%d')
        daily_posts = self.usage.get('daily_posts', {}).get(today, 0)
        if daily_posts + posts_needed > self.daily_post_limit:
            logger.warning(f"Daily post limit reached: {daily_posts}/{self.daily_post_limit}")
            return False
        
        return True

    def can_read(self, reads_needed: int = 1) -> bool:
        """Check if we can make read requests without exceeding limits"""
        self.reset_monthly_usage()
        
        # Check monthly limit
        if self.usage['reads_used'] + reads_needed > API_LIMITS['monthly_reads']:
            logger.warning(f"Monthly read limit reached: {self.usage['reads_used']}/{API_LIMITS['monthly_reads']}")
            return False
        
        # Check daily limit
        today = datetime.now().strftime('%Y-%m-%d')
        daily_reads = self.usage.get('daily_reads', {}).get(today, 0)
        if daily_reads + reads_needed > self.daily_read_limit:
            logger.warning(f"Daily read limit reached: {daily_reads}/{self.daily_read_limit}")
            return False
        
        return True

    def record_post(self, count: int = 1):
        """Record API post usage"""
        self.usage['posts_used'] += count
        
        # Track daily usage
        today = datetime.now().strftime('%Y-%m-%d')
        if 'daily_posts' not in self.usage:
            self.usage['daily_posts'] = {}
        self.usage['daily_posts'][today] = self.usage['daily_posts'].get(today, 0) + count
        
        self.save_usage()
        logger.info(f"Recorded {count} posts. Total: {self.usage['posts_used']}/{API_LIMITS['monthly_posts']}")

    def record_read(self, count: int = 1):
        """Record API read usage"""
        self.usage['reads_used'] += count
        
        # Track daily usage
        today = datetime.now().strftime('%Y-%m-%d')
        if 'daily_reads' not in self.usage:
            self.usage['daily_reads'] = {}
        self.usage['daily_reads'][today] = self.usage['daily_reads'].get(today, 0) + count
        
        self.save_usage()
        logger.info(f"Recorded {count} reads. Total: {self.usage['reads_used']}/{API_LIMITS['monthly_reads']}")

    def post_morning_scripture(self) -> bool:
        """Post morning scripture in English and Chinese thread"""
        if not self.can_post(self.posts_per_thread):
            logger.warning("Cannot post morning scripture - limit reached")
            return False
        
        try:
            # Get verse reference
            verse_ref, _ = self.bnb_analysis.create_morning_scripture_post()
            
            # Parse verse reference (e.g., "Jeremiah 29:11")
            parts = verse_ref.split()
            book = parts[0]
            chapter_verse = parts[1].split(':')
            chapter = int(chapter_verse[0])
            verse = int(chapter_verse[1])
            
            # Get English and Chinese versions
            english_verse = self.bible_api.get_verse_by_reference(book, chapter, verse)
            chinese_verse = self.bible_api.get_verse_by_reference(book, chapter, verse)
            
            if not english_verse or not chinese_verse:
                logger.error("Failed to fetch verse for morning scripture")
                return False
            
            # Format posts (just the scripture, nothing else)
            english_post = self.bible_api.format_verse_for_post(english_verse)
            chinese_post = self.bible_api.format_verse_for_post(chinese_verse)
            
            # Post thread
            success = self.x_api.post_thread([english_post, chinese_post])
            
            if success:
                self.record_post(self.posts_per_thread)
                logger.info(f"Posted morning scripture: {verse_ref}")
                return True
            else:
                logger.error("Failed to post morning scripture")
                return False
                
        except Exception as e:
            logger.error(f"Error posting morning scripture: {e}")
            return False

    def post_bnb_ecosystem_news(self) -> bool:
        """Post BNB ecosystem news in English and Chinese thread"""
        if not self.can_post(self.posts_per_thread):
            logger.warning("Cannot post ecosystem news - limit reached")
            return False
        
        try:
            # Get ecosystem news
            news_items = self.bnb_analysis.get_bnb_ecosystem_news()
            
            # Format English post
            english_post = self.bnb_analysis.format_ecosystem_news_post(news_items)
            
            # Create Chinese version (simplified for now)
            chinese_post = f"BNB生态系统新闻 (24小时)\n\n"
            for i, news in enumerate(news_items[:3], 1):
                title = news.get('title', 'Unknown')
                chinese_post += f"{i}. {title}\n"
            chinese_post += "\n#BNB #BSC #生态系统 #新闻"
            
            # Post thread
            success = self.x_api.post_thread([english_post, chinese_post])
            
            if success:
                self.record_post(self.posts_per_thread)
                logger.info("Posted BNB ecosystem news")
                return True
            else:
                logger.error("Failed to post ecosystem news")
                return False
                
        except Exception as e:
            logger.error(f"Error posting ecosystem news: {e}")
            return False

    def post_bsc_trending_coins(self) -> bool:
        """Post BSC trending coins in English and Chinese thread"""
        if not self.can_post(self.posts_per_thread):
            logger.warning("Cannot post trending coins - limit reached")
            return False
        
        try:
            # Get trending BSC coins
            trending_coins = self.bnb_analysis.get_bsc_trending_coins(5)
            
            # Format English post
            english_post = self.bnb_analysis.format_trending_coins_post(trending_coins)
            
            # Create Chinese version
            chinese_post = f"BSC生态系统热门代币 (24小时)\n\n"
            for i, coin in enumerate(trending_coins[:5], 1):
                name = coin.get('name', 'Unknown')
                symbol = coin.get('symbol', '')
                price = coin.get('current_price', 0)
                change = coin.get('price_change_percentage_24h', 0)
                
                if price >= 1:
                    price_str = f"${price:,.2f}"
                else:
                    price_str = f"${price:.6f}"
                
                change_emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                chinese_post += f"{i}. {name} ({symbol})\n"
                chinese_post += f"   {price_str} {change_emoji} {change:+.2f}%\n\n"
            
            chinese_post += "#BSC #BNB #DeFi #热门"
            
            # Post thread
            success = self.x_api.post_thread([english_post, chinese_post])
            
            if success:
                self.record_post(self.posts_per_thread)
                logger.info("Posted BSC trending coins")
                return True
            else:
                logger.error("Failed to post trending coins")
                return False
                
        except Exception as e:
            logger.error(f"Error posting trending coins: {e}")
            return False

    def post_upcoming_bnb_projects(self) -> bool:
        """Post upcoming BNB projects in English and Chinese thread"""
        if not self.can_post(self.posts_per_thread):
            logger.warning("Cannot post upcoming projects - limit reached")
            return False
        
        try:
            # Get upcoming projects
            projects = self.bnb_analysis.get_upcoming_bnb_projects()
            
            # Format English post
            english_post = self.bnb_analysis.format_upcoming_projects_post(projects)
            
            # Create Chinese version
            chinese_post = f"即将推出的BNB项目与投资\n\n"
            
            # Group by backer
            yzi_projects = [p for p in projects if p.get('backer') == 'YZi Labs']
            binance_projects = [p for p in projects if p.get('backer') == 'Binance']
            
            if yzi_projects:
                chinese_post += "YZi Labs 支持:\n"
                for project in yzi_projects[:3]:
                    name = project.get('name', 'Unknown')
                    category = project.get('category', '')
                    chinese_post += f"• {name} ({category})\n"
                chinese_post += "\n"
            
            if binance_projects:
                chinese_post += "币安支持:\n"
                for project in binance_projects[:2]:
                    name = project.get('name', 'Unknown')
                    category = project.get('category', '')
                    chinese_post += f"• {name} ({category})\n"
                chinese_post += "\n"
            
            chinese_post += "#BNB #BSC #投资 #创新"
            
            # Post thread
            success = self.x_api.post_thread([english_post, chinese_post])
            
            if success:
                self.record_post(self.posts_per_thread)
                logger.info("Posted upcoming BNB projects")
                return True
            else:
                logger.error("Failed to post upcoming projects")
                return False
                
        except Exception as e:
            logger.error(f"Error posting upcoming projects: {e}")
            return False

    def post_bnb_insight(self) -> bool:
        """Post BNB educational insight"""
        if not self.can_post(1):
            logger.warning("Cannot post BNB insight - limit reached")
            return False
        
        try:
            # Get BNB insights
            insights = self.bnb_analysis.get_bnb_insights()
            
            # Select random insight
            import random
            insight = random.choice(insights)
            
            # Format post
            post_text = self.bnb_analysis.format_bnb_insight_post(insight)
            
            # Post
            success = self.x_api.post_tweet(post_text)
            
            if success:
                self.record_post(1)
                logger.info("Posted BNB insight")
                return True
            else:
                logger.error("Failed to post BNB insight")
                return False
                
        except Exception as e:
            logger.error(f"Error posting BNB insight: {e}")
            return False

    def post_bnb_security_tip(self) -> bool:
        """Post BNB security tip"""
        if not self.can_post(1):
            logger.warning("Cannot post security tip - limit reached")
            return False
        
        try:
            # Get security tips
            tips = self.bnb_analysis.get_bnb_security_tips()
            
            # Select random tip
            import random
            tip = random.choice(tips)
            
            # Format post
            post_text = self.bnb_analysis.format_security_tip_post(tip)
            
            # Post
            success = self.x_api.post_tweet(post_text)
            
            if success:
                self.record_post(1)
                logger.info("Posted BNB security tip")
                return True
            else:
                logger.error("Failed to post security tip")
                return False
                
        except Exception as e:
            logger.error(f"Error posting security tip: {e}")
            return False

    def post_bnb_educational_content(self) -> bool:
        """Post BNB educational content"""
        if not self.can_post(1):
            logger.warning("Cannot post educational content - limit reached")
            return False
        
        try:
            # Get educational topics
            topics = self.bnb_analysis.get_bnb_educational_content()
            
            # Select random topic
            import random
            topic = random.choice(topics)
            
            # Format post
            post_text = self.bnb_analysis.format_educational_post(topic)
            
            # Post
            success = self.x_api.post_tweet(post_text)
            
            if success:
                self.record_post(1)
                logger.info("Posted BNB educational content")
                return True
            else:
                logger.error("Failed to post educational content")
                return False
                
        except Exception as e:
            logger.error(f"Error posting educational content: {e}")
            return False

    def post_market_relevant_verse(self) -> bool:
        """Post Bible verse relevant to current market conditions"""
        if not self.can_post(self.posts_per_thread):
            logger.warning("Cannot post market verse - limit reached")
            return False
        
        try:
            # Get BNB market data
            bnb_data = self.bnb_analysis.get_bnb_detailed_data()
            
            # Select market-relevant verse
            selected_verse = self.ai_module.select_news_relevant_verse("market conditions", bnb_data)
            
            # Get English and Chinese versions
            english_verse = self.bible_api.get_verse_by_reference(selected_verse, chinese=False)
            chinese_verse = self.bible_api.get_verse_by_reference(selected_verse, chinese=True)
            
            if not english_verse or not chinese_verse:
                logger.error("Failed to fetch market-relevant verse")
                return False
            
            # Format posts
            english_post = self.bible_api.format_verse_for_post(english_verse, chinese=False)
            chinese_post = self.bible_api.format_verse_for_post(chinese_verse, chinese=True)
            
            # Post thread
            success = self.x_api.post_thread([english_post, chinese_post])
            
            if success:
                self.record_post(self.posts_per_thread)
                logger.info(f"Posted market-relevant verse: {selected_verse}")
                return True
            else:
                logger.error("Failed to post market-relevant verse")
                return False
                
        except Exception as e:
            logger.error(f"Error posting market-relevant verse: {e}")
            return False

    def run_bnb_interactions(self) -> int:
        """Run interactions with BNB-focused accounts"""
        interactions = 0
        
        if not self.can_read(1):
            logger.warning("Cannot run interactions - read limit reached")
            return 0
        
        try:
            # Get tweets from target accounts
            for username, user_id in TARGET_ACCOUNTS.items():
                if not self.can_read(1):
                    break
                
                try:
                    tweets = self.x_api.get_user_tweets(user_id, max_results=5)
                    self.record_read(1)
                    
                    if tweets and len(tweets) > 0:
                        # Find a tweet to reply to
                        for tweet in tweets:
                            if not self.can_post(1):
                                break
                            
                            # Use AI to determine if we should reply
                            should_reply = self.ai_module.is_relevant_for_interaction(tweet.get('text', ''))
                            
                            if should_reply:
                                # Get BNB market data for context
                                bnb_data = self.bnb_analysis.get_bnb_detailed_data()
                                
                                # Get appropriate verse
                                theme = self.ai_module.analyze_post_theme(tweet.get('text', ''))
                                verse_suggestions = THEME_VERSE_SUGGESTIONS.get(theme, THEME_VERSE_SUGGESTIONS['faith'])
                                selected_verse = self.ai_module.suggest_verse_for_theme(theme)
                                
                                # Get verse
                                verse = self.bible_api.get_verse_by_reference(selected_verse, chinese=True)
                                
                                if verse:
                                    reply_text = self.bible_api.format_verse_for_reply(verse)
                                    
                                    # Reply to tweet
                                    success = self.x_api.reply_to_tweet(tweet['id'], reply_text)
                                    
                                    if success:
                                        self.record_post(1)
                                        interactions += 1
                                        logger.info(f"Replied to {username}: {selected_verse}")
                                        break  # Only reply to one tweet per account
                                    else:
                                        logger.error(f"Failed to reply to {username}")
                                
                except Exception as e:
                    logger.error(f"Error interacting with {username}: {e}")
        
        except Exception as e:
            logger.error(f"Error running BNB interactions: {e}")
        
        return interactions

    def run_bnb_daily_routine(self):
        """Run optimized BNB-focused daily routine"""
        logger.info("Starting BNB-focused daily routine...")
        
        # Show current usage
        today = datetime.now().strftime('%Y-%m-%d')
        daily_posts = self.usage.get('daily_posts', {}).get(today, 0)
        daily_reads = self.usage.get('daily_reads', {}).get(today, 0)
        
        logger.info(f"Current daily usage: {daily_posts}/{self.daily_post_limit} posts, {daily_reads}/{self.daily_read_limit} reads")
        
        results = {
            'morning_scripture': False,
            'ecosystem_news': False,
            'trending_coins': False,
            'upcoming_projects': False,
            'bnb_insights': 0,
            'security_tips': 0,
            'educational_content': 0,
            'market_verses': 0,
            'interactions': 0
        }
        
        # Morning routine (4 posts)
        # 1. Morning scripture (just the verse, nothing else)
        results['morning_scripture'] = self.post_morning_scripture()
        
        # 2. BNB ecosystem news
        results['ecosystem_news'] = self.post_bnb_ecosystem_news()
        
        # 3. BSC trending coins
        results['trending_coins'] = self.post_bsc_trending_coins()
        
        # 4. Upcoming BNB projects
        results['upcoming_projects'] = self.post_upcoming_bnb_projects()
        
        # Additional content throughout the day
        # 5. Post BNB insights
        for i in range(2):  # 2 BNB insights
            if self.post_bnb_insight():
                results['bnb_insights'] += 1
        
        # 6. Post security tips
        for i in range(2):  # 2 security tips
            if self.post_bnb_security_tip():
                results['security_tips'] += 1
        
        # 7. Post educational content
        for i in range(2):  # 2 educational posts
            if self.post_bnb_educational_content():
                results['educational_content'] += 1
        
        # 8. Post market-relevant verses
        for i in range(2):  # 2 market verses (4 posts total)
            if self.post_market_relevant_verse():
                results['market_verses'] += 1
        
        # 9. Run interactions
        results['interactions'] = self.run_bnb_interactions()
        
        # Final stats
        final_daily_posts = self.usage.get('daily_posts', {}).get(today, 0)
        final_daily_reads = self.usage.get('daily_reads', {}).get(today, 0)
        
        logger.info(f"BNB daily routine completed:")
        logger.info(f"- Morning scripture: {'✓' if results['morning_scripture'] else '✗'}")
        logger.info(f"- Ecosystem news: {'✓' if results['ecosystem_news'] else '✗'}")
        logger.info(f"- Trending coins: {'✓' if results['trending_coins'] else '✗'}")
        logger.info(f"- Upcoming projects: {'✓' if results['upcoming_projects'] else '✗'}")
        logger.info(f"- BNB insights: {results['bnb_insights']}")
        logger.info(f"- Security tips: {results['security_tips']}")
        logger.info(f"- Educational content: {results['educational_content']}")
        logger.info(f"- Market verses: {results['market_verses']}")
        logger.info(f"- Interactions: {results['interactions']}")
        logger.info(f"- Final usage: {final_daily_posts}/{self.daily_post_limit} posts, {final_daily_reads}/{self.daily_read_limit} reads")
        
        return results

def main():
    """Main function for testing"""
    bot = BNBBibleBot()
    
    # Run BNB daily routine
    result = bot.run_bnb_daily_routine()
    
    print(f"\nBNB Daily Routine Results:")
    print(f"  Morning analysis: {result['morning_analysis']}")
    print(f"  BNB insights: {result['bnb_insights']}")
    print(f"  Security tips: {result['security_tips']}")
    print(f"  Educational content: {result['educational_content']}")
    print(f"  Market verses: {result['market_verses']}")
    print(f"  Interactions: {result['interactions']}")

if __name__ == "__main__":
    main()
