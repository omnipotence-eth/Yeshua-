"""
BNB Analysis Module for Bible Verse Bot
Provides BNB price data, market analysis, and news integration
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

logger = logging.getLogger(__name__)

class BNBAnalysis:
    def __init__(self):
        """Initialize BNB analysis module"""
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        self.news_api_key = None  # Will be set from environment if available
        
        # BSC ecosystem token IDs for trending analysis
        self.bsc_tokens = [
            'binancecoin', 'pancakeswap-token', 'trust-wallet-token', 'venus-bnb',
            'alpaca-finance', 'autofarm', 'beefy-finance', 'bunny', 'cake',
            'venus', 'bakeryswap', 'burger-swap', 'dodo', 'ellipsis',
            'mdex', 'pancakebunny', 'safemoon', 'swipe', 'tokens-of-babel',
            'waultswap', 'bscpad', 'bscstarter', 'bscx', 'bunnypark',
            'goose-finance', 'jetswap', 'knightswap', 'moonpot', 'pancake-hunny'
        ]
        
    def get_bnb_price_data(self) -> Optional[Dict]:
        """Get BNB price data from CoinGecko API"""
        try:
            # CoinGecko free tier allows 10-50 calls per minute
            url = f"{self.coingecko_base_url}/simple/price"
            params = {
                'ids': 'binancecoin',
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true',
                'include_market_cap': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            bnb_data = data.get('binancecoin', {})
            
            if bnb_data:
                return {
                    'price': bnb_data.get('usd', 0),
                    'change_24h': bnb_data.get('usd_24h_change', 0),
                    'volume_24h': bnb_data.get('usd_24h_vol', 0),
                    'market_cap': bnb_data.get('usd_market_cap', 0),
                    'timestamp': datetime.now().isoformat()
                }
            
        except Exception as e:
            logger.error(f"Error fetching BNB price data: {e}")
        
        return None
    
    def get_bnb_detailed_data(self) -> Optional[Dict]:
        """Get detailed BNB market data"""
        try:
            url = f"{self.coingecko_base_url}/coins/binancecoin"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'true',
                'community_data': 'false',
                'developer_data': 'false',
                'sparkline': 'false'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            market_data = data.get('market_data', {})
            
            if market_data:
                return {
                    'current_price': market_data.get('current_price', {}).get('usd', 0),
                    'price_change_24h': market_data.get('price_change_24h', 0),
                    'price_change_percentage_24h': market_data.get('price_change_percentage_24h', 0),
                    'market_cap': market_data.get('market_cap', {}).get('usd', 0),
                    'total_volume': market_data.get('total_volume', {}).get('usd', 0),
                    'high_24h': market_data.get('high_24h', {}).get('usd', 0),
                    'low_24h': market_data.get('low_24h', {}).get('usd', 0),
                    'circulating_supply': market_data.get('circulating_supply', 0),
                    'total_supply': market_data.get('total_supply', 0),
                    'max_supply': market_data.get('max_supply', 0),
                    'timestamp': datetime.now().isoformat()
                }
            
        except Exception as e:
            logger.error(f"Error fetching detailed BNB data: {e}")
        
        return None
    
    def format_price_analysis(self, data: Dict) -> str:
        """Format BNB price analysis for posting"""
        if not data:
            return "BNB data temporarily unavailable. 🙏"
        
        price = data.get('current_price', 0)
        change_24h = data.get('price_change_percentage_24h', 0)
        volume_24h = data.get('total_volume', 0)
        market_cap = data.get('market_cap', 0)
        high_24h = data.get('high_24h', 0)
        low_24h = data.get('low_24h', 0)
        
        # Format numbers
        price_str = f"${price:,.2f}" if price else "N/A"
        change_str = f"{change_24h:+.2f}%" if change_24h else "N/A"
        volume_str = f"${volume_24h:,.0f}" if volume_24h else "N/A"
        market_cap_str = f"${market_cap:,.0f}" if market_cap else "N/A"
        high_str = f"${high_24h:,.2f}" if high_24h else "N/A"
        low_str = f"${low_24h:,.2f}" if low_24h else "N/A"
        
        # Determine trend emoji
        trend_emoji = "📈" if change_24h > 0 else "📉" if change_24h < 0 else "➡️"
        
        analysis = f"""BNB Market Analysis (24h)

{trend_emoji} Price: {price_str} ({change_str})
📊 Volume: {volume_str}
💎 Market Cap: {market_cap_str}
📈 24h High: {high_str}
📉 24h Low: {low_str}

#BNB #Binance #Crypto"""
        
        return analysis
    
    def get_bnb_news_themes(self) -> List[str]:
        """Get current BNB-related news themes for verse selection"""
        # This would ideally fetch from news API, but for now we'll use common themes
        themes = [
            'market_volatility',
            'crypto_regulation', 
            'blockchain_innovation',
            'decentralization',
            'financial_wisdom',
            'patience',
            'hope',
            'perseverance',
            'trust',
            'stewardship'
        ]
        
        # Add time-based themes
        current_hour = datetime.now().hour
        if 6 <= current_hour < 12:
            themes.extend(['morning_blessing', 'new_opportunities', 'fresh_start'])
        elif 12 <= current_hour < 18:
            themes.extend(['midday_strength', 'perseverance', 'focus'])
        else:
            themes.extend(['evening_reflection', 'gratitude', 'peace'])
        
        return themes
    
    def get_news_relevant_verse_theme(self, bnb_data: Dict) -> str:
        """Determine verse theme based on BNB market data"""
        if not bnb_data:
            return 'hope'
        
        change_24h = bnb_data.get('price_change_percentage_24h', 0)
        volume_24h = bnb_data.get('total_volume', 0)
        
        # Determine theme based on market conditions
        if change_24h > 5:
            return 'gratitude'  # Strong gains
        elif change_24h > 0:
            return 'hope'  # Positive movement
        elif change_24h > -5:
            return 'patience'  # Minor decline
        else:
            return 'perseverance'  # Significant decline
        
        # Volume-based themes
        if volume_24h > 1000000000:  # High volume
            return 'market_volatility'
        
        return 'faith'  # Default theme
    
    def create_morning_analysis_thread(self) -> Tuple[str, str]:
        """Create morning thread with BNB analysis"""
        # Get BNB data
        bnb_data = self.get_bnb_detailed_data()
        
        # Get news-relevant theme
        theme = self.get_news_relevant_verse_theme(bnb_data)
        
        # Format BNB analysis
        bnb_analysis = self.format_price_analysis(bnb_data)
        
        # Create morning greeting
        morning_greeting = f"""Good morning BNB community! 🌅

Starting the day with faith and financial wisdom.

{bnb_analysis}"""
        
        return morning_greeting, theme
    
    def get_bnb_insights(self) -> List[str]:
        """Get BNB insights and value propositions"""
        insights = [
            "BNB powers the Binance Smart Chain ecosystem",
            "Used for trading fee discounts on Binance",
            "Governance token for BSC network decisions",
            "Burning mechanism reduces supply over time",
            "Multi-chain utility across BSC and other networks",
            "Staking rewards available for holders",
            "Integration with DeFi protocols",
            "NFT marketplace and gaming applications"
        ]
        
        return insights
    
    def format_bnb_insight_post(self, insight: str) -> str:
        """Format BNB insight for posting"""
        return f"""BNB Insight 💡

{insight}

Understanding the fundamentals helps build long-term confidence in your investments.

#BNB #Binance #CryptoEducation #DeFi"""
    
    def get_bnb_security_tips(self) -> List[str]:
        """Get BNB security tips"""
        tips = [
            "Always use official Binance channels for support",
            "Enable 2FA on your Binance account",
            "Store BNB in hardware wallets for long-term holding",
            "Never share your private keys or seed phrases",
            "Verify transaction addresses before sending",
            "Use official BSC network for BNB transactions",
            "Keep your software wallets updated",
            "Be cautious of phishing websites and fake apps"
        ]
        
        return tips
    
    def format_security_tip_post(self, tip: str) -> str:
        """Format security tip for posting"""
        return f"""BNB Security Tip 🔒

{tip}

Protecting your investments is as important as making them.

#BNB #Security #Crypto #Binance"""
    
    def get_bnb_educational_content(self) -> List[Dict]:
        """Get BNB educational content topics"""
        topics = [
            {
                'title': 'What is BNB?',
                'content': 'BNB (Binance Coin) is the native cryptocurrency of the Binance ecosystem, used for trading fees, staking, and governance.',
                'hashtags': '#BNB #Binance #CryptoEducation'
            },
            {
                'title': 'BNB Burning Mechanism',
                'content': 'Binance burns BNB tokens quarterly, reducing supply and potentially increasing value over time.',
                'hashtags': '#BNB #Tokenomics #Deflationary'
            },
            {
                'title': 'BSC vs Ethereum',
                'content': 'Binance Smart Chain offers lower fees and faster transactions compared to Ethereum, while maintaining compatibility.',
                'hashtags': '#BSC #Ethereum #DeFi #BNB'
            },
            {
                'title': 'BNB Staking Rewards',
                'content': 'Stake BNB to earn rewards while supporting network security and governance.',
                'hashtags': '#BNB #Staking #Rewards #Governance'
            }
        ]
        
        return topics
    
    def format_educational_post(self, topic: Dict) -> str:
        """Format educational content for posting"""
        return f"""BNB Education 📚

{topic['title']}

{topic['content']}

{topic['hashtags']}"""
    
    def get_market_sentiment_verse_theme(self, bnb_data: Dict) -> str:
        """Get verse theme based on market sentiment"""
        if not bnb_data:
            return 'faith'
        
        change_24h = bnb_data.get('price_change_percentage_24h', 0)
        
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
    
    def get_bsc_trending_coins(self, limit: int = 10) -> List[Dict]:
        """Get trending coins in BSC ecosystem"""
        try:
            # Get trending coins from CoinGecko
            url = f"{self.coingecko_base_url}/search/trending"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            trending_coins = data.get('coins', [])
            
            # Filter for BSC ecosystem coins
            bsc_trending = []
            for coin in trending_coins[:limit * 2]:  # Get more to filter
                coin_id = coin.get('item', {}).get('id', '')
                if coin_id in self.bsc_tokens:
                    bsc_trending.append({
                        'id': coin_id,
                        'name': coin.get('item', {}).get('name', ''),
                        'symbol': coin.get('item', {}).get('symbol', '').upper(),
                        'market_cap_rank': coin.get('item', {}).get('market_cap_rank', 0),
                        'thumb': coin.get('item', {}).get('thumb', '')
                    })
                    
                    if len(bsc_trending) >= limit:
                        break
            
            # If not enough trending BSC coins, get top BSC coins by market cap
            if len(bsc_trending) < limit:
                bsc_trending.extend(self.get_top_bsc_coins(limit - len(bsc_trending)))
            
            return bsc_trending[:limit]
            
        except Exception as e:
            logger.error(f"Error fetching BSC trending coins: {e}")
            return self.get_top_bsc_coins(limit)
    
    def get_top_bsc_coins(self, limit: int = 10) -> List[Dict]:
        """Get top BSC coins by market cap"""
        try:
            # Get market data for BSC tokens
            url = f"{self.coingecko_base_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'ids': ','.join(self.bsc_tokens[:20]),  # Limit to avoid rate limits
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': 'false'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return [{
                'id': coin.get('id', ''),
                'name': coin.get('name', ''),
                'symbol': coin.get('symbol', '').upper(),
                'current_price': coin.get('current_price', 0),
                'price_change_percentage_24h': coin.get('price_change_percentage_24h', 0),
                'market_cap': coin.get('market_cap', 0),
                'market_cap_rank': coin.get('market_cap_rank', 0)
            } for coin in data]
            
        except Exception as e:
            logger.error(f"Error fetching top BSC coins: {e}")
            return []
    
    def format_trending_coins_post(self, trending_coins: List[Dict]) -> str:
        """Format trending BSC coins for posting"""
        if not trending_coins:
            return "BSC trending data temporarily unavailable. 🙏"
        
        post = "🔥 BSC Ecosystem Trending Coins (24h)\n\n"
        
        for i, coin in enumerate(trending_coins[:5], 1):
            name = coin.get('name', 'Unknown')
            symbol = coin.get('symbol', '')
            price = coin.get('current_price', 0)
            change = coin.get('price_change_percentage_24h', 0)
            
            # Format price
            if price >= 1:
                price_str = f"${price:,.2f}"
            else:
                price_str = f"${price:.6f}"
            
            # Format change with emoji
            change_emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            change_str = f"{change:+.2f}%"
            
            post += f"{i}. {name} ({symbol})\n"
            post += f"   {price_str} {change_emoji} {change_str}\n\n"
        
        post += "#BSC #BNB #DeFi #Trending"
        
        return post
    
    def get_bnb_ecosystem_news(self) -> List[Dict]:
        """Get BNB ecosystem news and updates"""
        # This would ideally fetch from news API, but for now we'll use curated content
        news_items = [
            {
                'title': 'YZi Labs Launches $1B Builder Fund',
                'summary': 'Binance\'s venture arm announces massive funding for BNB ecosystem projects',
                'category': 'funding',
                'impact': 'high'
            },
            {
                'title': 'BSC Network Upgrades',
                'summary': 'Latest BSC network improvements enhance transaction speed and reduce fees',
                'category': 'technology',
                'impact': 'medium'
            },
            {
                'title': 'New DeFi Protocols Launch',
                'summary': 'Several innovative DeFi projects launch on BSC this week',
                'category': 'defi',
                'impact': 'medium'
            },
            {
                'title': 'BNB Token Burn',
                'summary': 'Latest quarterly BNB burn reduces circulating supply',
                'category': 'tokenomics',
                'impact': 'high'
            },
            {
                'title': 'Cross-Chain Bridge Updates',
                'summary': 'Enhanced cross-chain capabilities for BSC ecosystem',
                'category': 'infrastructure',
                'impact': 'medium'
            }
        ]
        
        return news_items
    
    def format_ecosystem_news_post(self, news_items: List[Dict]) -> str:
        """Format BNB ecosystem news for posting"""
        if not news_items:
            return "BNB ecosystem news temporarily unavailable. 🙏"
        
        post = "BNB Ecosystem News (24h)\n\n"
        
        for i, news in enumerate(news_items[:2], 1):  # Reduced to 2 items
            title = news.get('title', 'Unknown')
            # Truncate long titles
            if len(title) > 40:
                title = title[:37] + "..."
            post += f"{i}. {title}\n"
        
        post += "#BNB #BSC #Ecosystem #News"
        
        return post
    
    def get_upcoming_bnb_projects(self) -> List[Dict]:
        """Get upcoming BNB projects and investments"""
        projects = [
            {
                'name': 'Aster',
                'description': 'Multichain DEX enhancing cross-chain trading capabilities',
                'category': 'DeFi',
                'backer': 'YZi Labs',
                'status': 'funded'
            },
            {
                'name': 'Blum',
                'description': 'AI-integrated DeFi platform optimizing trading strategies',
                'category': 'AI/DeFi',
                'backer': 'YZi Labs',
                'status': 'funded'
            },
            {
                'name': 'Sahara AI',
                'description': 'AI-driven analytics tool for market insights',
                'category': 'AI',
                'backer': 'YZi Labs',
                'status': 'funded'
            },
            {
                'name': 'Perena',
                'description': 'Real-world asset tokenization platform',
                'category': 'RWA',
                'backer': 'YZi Labs',
                'status': 'funded'
            },
            {
                'name': 'Sophon',
                'description': 'Decentralized science initiative for open research',
                'category': 'DeSci',
                'backer': 'YZi Labs',
                'status': 'funded'
            },
            {
                'name': 'BSC Gaming Hub',
                'description': 'Gaming infrastructure and NFT marketplace',
                'category': 'Gaming',
                'backer': 'Binance',
                'status': 'development'
            },
            {
                'name': 'Green BSC',
                'description': 'Carbon-neutral blockchain initiatives',
                'category': 'Sustainability',
                'backer': 'Binance',
                'status': 'development'
            }
        ]
        
        return projects
    
    def format_upcoming_projects_post(self, projects: List[Dict]) -> str:
        """Format upcoming BNB projects for posting"""
        if not projects:
            return "BNB upcoming projects data temporarily unavailable. 🙏"
        
        post = "Upcoming BNB Projects & Investments\n\n"
        
        # Group by backer
        yzi_projects = [p for p in projects if p.get('backer') == 'YZi Labs']
        binance_projects = [p for p in projects if p.get('backer') == 'Binance']
        
        if yzi_projects:
            post += "YZi Labs Backed:\n"
            for project in yzi_projects[:2]:  # Reduced to 2
                name = project.get('name', 'Unknown')
                category = project.get('category', '')
                post += f"• {name} ({category})\n"
        
        if binance_projects:
            post += "\nBinance Supported:\n"
            for project in binance_projects[:1]:  # Reduced to 1
                name = project.get('name', 'Unknown')
                category = project.get('category', '')
                post += f"• {name} ({category})\n"
        
        post += "#BNB #BSC #Investments #Innovation"
        
        return post
    
    def create_morning_scripture_post(self) -> tuple:
        """Create morning scripture post in English and Chinese"""
        # Get today's theme
        from datetime import datetime
        from config import DAILY_THEMES
        
        day_name = datetime.now().strftime('%A').lower()
        theme = DAILY_THEMES.get(day_name, 'hope')
        
        # Get inspirational verse for the theme
        inspirational_verses = {
            'hope': 'Jeremiah 29:11',
            'wisdom': 'Proverbs 3:5-6',
            'perseverance': 'Romans 5:3-4',
            'faith': 'Hebrews 11:1',
            'love': '1 Corinthians 13:4-7',
            'peace': 'Philippians 4:7',
            'gratitude': '1 Thessalonians 5:18'
        }
        
        verse_ref = inspirational_verses.get(theme, 'Jeremiah 29:11')
        
        # Return tuple for English and Chinese posts
        english_post = verse_ref
        chinese_post = verse_ref  # Will be replaced with Chinese version in bot
        
        return english_post, chinese_post

def main():
    """Test the BNB analysis module"""
    bnb_analysis = BNBAnalysis()
    
    # Test price data
    print("Testing BNB price data...")
    price_data = bnb_analysis.get_bnb_price_data()
    print(f"Price data: {price_data}")
    
    # Test detailed data
    print("\nTesting detailed BNB data...")
    detailed_data = bnb_analysis.get_bnb_detailed_data()
    print(f"Detailed data: {detailed_data}")
    
    # Test morning analysis
    print("\nTesting morning analysis...")
    morning_post, theme = bnb_analysis.create_morning_analysis_thread()
    print(f"Morning post: {morning_post}")
    print(f"Selected theme: {theme}")

if __name__ == "__main__":
    main()
