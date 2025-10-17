"""
BNB Bot Interactive Features
Handles mentions, polls, custom queries, and user engagement
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class BNBInteractive:
    """Interactive features for BNB Bible Bot"""
    
    def __init__(self):
        self.commands = {
            'price': self._handle_price_query,
            'volume': self._handle_volume_query,
            'trending': self._handle_trending_query,
            'whale': self._handle_whale_query,
            'gas': self._handle_gas_query,
            'help': self._handle_help_query,
            'verse': self._handle_verse_query,
            'prayer': self._handle_prayer_request
        }
        
        # User interaction tracking
        self.user_interactions = {}
        self.daily_queries = {}
    
    def process_mention(self, mention_text: str, user_handle: str) -> Optional[str]:
        """Process user mentions and return appropriate response"""
        try:
            # Extract command from mention
            command = self._extract_command(mention_text)
            
            if not command:
                return self._handle_general_mention(user_handle)
            
            # Track user interaction
            self._track_user_interaction(user_handle, command)
            
            # Execute command
            if command in self.commands:
                return self.commands[command](mention_text, user_handle)
            else:
                return self._handle_unknown_command(command, user_handle)
                
        except Exception as e:
            logger.error(f"Error processing mention: {e}")
            return f"Sorry @{user_handle}, I encountered an error. Please try again! 🙏"
    
    def _extract_command(self, text: str) -> Optional[str]:
        """Extract command from mention text"""
        text = text.lower()
        
        # Look for specific commands
        if any(word in text for word in ['price', 'cost', 'value']):
            return 'price'
        elif any(word in text for word in ['volume', 'trading']):
            return 'volume'
        elif any(word in text for word in ['trending', 'hot', 'popular']):
            return 'trending'
        elif any(word in text for word in ['whale', 'big', 'large']):
            return 'whale'
        elif any(word in text for word in ['gas', 'fee', 'cost']):
            return 'gas'
        elif any(word in text for word in ['help', 'commands']):
            return 'help'
        elif any(word in text for word in ['verse', 'scripture', 'bible']):
            return 'verse'
        elif any(word in text for word in ['prayer', 'pray', 'blessing']):
            return 'prayer'
        
        return None
    
    def _handle_price_query(self, text: str, user_handle: str) -> str:
        """Handle price queries"""
        # Extract token symbol if mentioned
        token_symbol = self._extract_token_symbol(text)
        
        if token_symbol:
            return f"@{user_handle} Here's the current price for {token_symbol}:\n\n" \
                   f"📊 Price: $X.XX\n" \
                   f"📈 24h Change: +X.XX%\n" \
                   f"💰 Volume: $X.XXM\n\n" \
                   f"#BSC #DeFi #Price"
        else:
            return f"@{user_handle} Current BNB ecosystem prices:\n\n" \
                   f"🪙 BNB: $X.XX (+X.XX%)\n" \
                   f"🥞 CAKE: $X.XX (+X.XX%)\n" \
                   f"🔒 TWT: $X.XX (+X.XX%)\n\n" \
                   f"#BNB #BSC #Prices"
    
    def _handle_volume_query(self, text: str, user_handle: str) -> str:
        """Handle volume queries"""
        return f"@{user_handle} BSC Volume Leaders (24h):\n\n" \
               f"📊 Top Volume Tokens:\n" \
               f"1. BNB: $XXX.XM\n" \
               f"2. CAKE: $XX.XM\n" \
               f"3. TWT: $X.XM\n\n" \
               f"#BSC #Volume #DeFi"
    
    def _handle_trending_query(self, text: str, user_handle: str) -> str:
        """Handle trending queries"""
        return f"@{user_handle} 🔥 BSC Trending Now:\n\n" \
               f"1. TokenA: +XX.XX%\n" \
               f"2. TokenB: +XX.XX%\n" \
               f"3. TokenC: +XX.XX%\n\n" \
               f"⚠️ DYOR before investing!\n" \
               f"#BSC #Trending #DeFi"
    
    def _handle_whale_query(self, text: str, user_handle: str) -> str:
        """Handle whale activity queries"""
        return f"@{user_handle} 🐋 Recent BSC Whale Activity:\n\n" \
               f"• Large BNB transfer: XXX,XXX BNB\n" \
               f"• CAKE accumulation: XXX,XXX CAKE\n" \
               f"• New whale wallet detected\n\n" \
               f"#BSC #Whale #Activity"
    
    def _handle_gas_query(self, text: str, user_handle: str) -> str:
        """Handle gas fee queries"""
        return f"@{user_handle} ⛽ Current BSC Gas Fees:\n\n" \
               f"• Standard: X Gwei\n" \
               f"• Fast: X Gwei\n" \
               f"• Instant: X Gwei\n\n" \
               f"💡 BSC fees are much lower than Ethereum!\n" \
               f"#BSC #Gas #Fees"
    
    def _handle_help_query(self, text: str, user_handle: str) -> str:
        """Handle help queries"""
        return f"@{user_handle} 🤖 BNB Bible Bot Commands:\n\n" \
               f"• 'price' - Get token prices\n" \
               f"• 'volume' - Check trading volume\n" \
               f"• 'trending' - See trending tokens\n" \
               f"• 'whale' - Whale activity alerts\n" \
               f"• 'gas' - Current gas fees\n" \
               f"• 'verse' - Daily scripture\n" \
               f"• 'prayer' - Prayer request\n\n" \
               f"Just mention me with any command! 🙏\n" \
               f"#BNB #BSC #Help"
    
    def _handle_verse_query(self, text: str, user_handle: str) -> str:
        """Handle verse requests"""
        return f"@{user_handle} 📖 Today's Scripture:\n\n" \
               f"\"For I know the plans I have for you,\" declares the Lord, \"plans to prosper you and not to harm you, plans to give you hope and a future.\"\n\n" \
               f"— Jeremiah 29:11\n\n" \
               f"May this verse guide your trading decisions! 🙏\n" \
               f"#Faith #BNB #Scripture"
    
    def _handle_prayer_request(self, text: str, user_handle: str) -> str:
        """Handle prayer requests"""
        return f"@{user_handle} 🙏 Prayer for you:\n\n" \
               f"Lord, bless @{user_handle} with wisdom in their investments, protection from scams, and peace in market volatility. Guide their decisions and prosper their journey in the BNB ecosystem. Amen.\n\n" \
               f"#Prayer #BNB #Blessing"
    
    def _handle_general_mention(self, user_handle: str) -> str:
        """Handle general mentions without specific commands"""
        return f"@{user_handle} Hello! 👋\n\n" \
               f"I'm your BNB Bible Bot, here to help with:\n" \
               f"• Market alerts & analysis\n" \
               f"• Daily scripture inspiration\n" \
               f"• BSC ecosystem updates\n\n" \
               f"Try: '@BNBBibleBot price' or '@BNBBibleBot help'\n" \
               f"#BNB #BSC #Welcome"
    
    def _handle_unknown_command(self, command: str, user_handle: str) -> str:
        """Handle unknown commands"""
        return f"@{user_handle} I didn't understand '{command}' 😅\n\n" \
               f"Try these commands:\n" \
               f"• price, volume, trending\n" \
               f"• whale, gas, help\n" \
               f"• verse, prayer\n\n" \
               f"#BNB #BSC #Help"
    
    def _extract_token_symbol(self, text: str) -> Optional[str]:
        """Extract token symbol from text"""
        # Look for common token symbols
        tokens = ['BNB', 'CAKE', 'TWT', 'XVS', 'ALPACA', 'BIFI', 'USDT', 'USDC']
        text_upper = text.upper()
        
        for token in tokens:
            if token in text_upper:
                return token
        
        return None
    
    def _track_user_interaction(self, user_handle: str, command: str):
        """Track user interactions for analytics"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today not in self.daily_queries:
            self.daily_queries[today] = {}
        
        if user_handle not in self.daily_queries[today]:
            self.daily_queries[today][user_handle] = 0
        
        self.daily_queries[today][user_handle] += 1
        
        # Store in user interactions
        if user_handle not in self.user_interactions:
            self.user_interactions[user_handle] = []
        
        self.user_interactions[user_handle].append({
            'command': command,
            'timestamp': datetime.now().isoformat()
        })
    
    def create_engagement_poll(self) -> str:
        """Create an engagement poll for the community"""
        polls = [
            {
                'question': 'What\'s your favorite BSC DeFi protocol?',
                'options': ['PancakeSwap', 'Venus', 'Alpaca Finance', 'Beefy Finance'],
                'hashtags': '#BSC #DeFi #Poll'
            },
            {
                'question': 'How do you stay updated on BNB ecosystem?',
                'options': ['Twitter/X', 'Telegram', 'Discord', 'Reddit'],
                'hashtags': '#BNB #Community #Poll'
            },
            {
                'question': 'What\'s your BNB trading strategy?',
                'options': ['HODL', 'Day Trade', 'Swing Trade', 'Yield Farm'],
                'hashtags': '#BNB #Trading #Strategy'
            }
        ]
        
        import random
        poll = random.choice(polls)
        
        return f"📊 Community Poll:\n\n" \
               f"{poll['question']}\n\n" \
               f"Vote in the replies:\n" \
               f"1️⃣ {poll['options'][0]}\n" \
               f"2️⃣ {poll['options'][1]}\n" \
               f"3️⃣ {poll['options'][2]}\n" \
               f"4️⃣ {poll['options'][3]}\n\n" \
               f"{poll['hashtags']}"
    
    def create_educational_thread(self) -> List[str]:
        """Create an educational thread about BNB ecosystem"""
        threads = [
            [
                "🎓 BNB Ecosystem Education Thread 🧵\n\n1/5 What is BNB Chain?\n\nBNB Chain is a blockchain network built for running smart contract-based applications. It's designed to run alongside Binance Chain, offering smart contracts and staking functionality.",
                "2/5 Key Features:\n\n• Low transaction fees (~$0.10)\n• Fast block times (3 seconds)\n• EVM compatible\n• 100+ validators\n• Cross-chain compatibility",
                "3/5 Popular DeFi Protocols:\n\n• PancakeSwap - DEX & yield farming\n• Venus - Lending & borrowing\n• Alpaca Finance - Leveraged yield farming\n• Beefy Finance - Yield optimizer",
                "4/5 Security Tips:\n\n• Always verify contract addresses\n• Use official websites only\n• Start with small amounts\n• Never share your seed phrase\n• Use hardware wallets for large amounts",
                "5/5 Getting Started:\n\n• Get BNB for gas fees\n• Connect MetaMask to BSC\n• Start with established protocols\n• Join BSC communities for support\n\n#BNB #BSC #Education #DeFi"
            ],
            [
                "🛡️ BSC Security Best Practices 🧵\n\n1/4 Wallet Security:\n\n• Use hardware wallets (Ledger/Trezor)\n• Never share private keys\n• Enable 2FA on exchanges\n• Use different wallets for different purposes",
                "2/4 Smart Contract Safety:\n\n• Verify contract addresses on BscScan\n• Check audit reports\n• Start with small test amounts\n• Be wary of new unaudited projects",
                "3/4 Trading Safety:\n\n• DYOR (Do Your Own Research)\n• Don't FOMO into pumps\n• Set stop losses\n• Diversify your portfolio\n• Never invest more than you can lose",
                "4/4 Community Safety:\n\n• Beware of fake accounts\n• Don't click suspicious links\n• Verify information from multiple sources\n• Report scams to authorities\n\n#BSC #Security #Safety #DeFi"
            ]
        ]
        
        import random
        return random.choice(threads)
    
    def get_user_stats(self, user_handle: str) -> Dict:
        """Get user interaction statistics"""
        if user_handle not in self.user_interactions:
            return {'total_interactions': 0, 'commands_used': []}
        
        interactions = self.user_interactions[user_handle]
        commands_used = [i['command'] for i in interactions]
        
        return {
            'total_interactions': len(interactions),
            'commands_used': list(set(commands_used)),
            'last_interaction': interactions[-1]['timestamp'] if interactions else None
        }

def main():
    """Test the interactive features"""
    interactive = BNBInteractive()
    
    print("BNB Interactive Features Test")
    print("=" * 50)
    
    # Test mention processing
    test_mentions = [
        "@BNBBibleBot what's the BNB price?",
        "@BNBBibleBot show me trending tokens",
        "@BNBBibleBot help",
        "@BNBBibleBot give me a verse",
        "@BNBBibleBot pray for me"
    ]
    
    for mention in test_mentions:
        print(f"\nMention: {mention}")
        response = interactive.process_mention(mention, "testuser")
        print(f"Response: {response[:100]}...")
    
    # Test poll creation
    print(f"\nPoll:\n{interactive.create_engagement_poll()}")
    
    # Test educational thread
    thread = interactive.create_educational_thread()
    print(f"\nEducational Thread ({len(thread)} tweets):")
    for i, tweet in enumerate(thread, 1):
        print(f"{i}: {tweet[:50]}...")

if __name__ == "__main__":
    main()
