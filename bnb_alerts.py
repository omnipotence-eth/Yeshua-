"""
BNB Chain Real-Time Alerts System
Monitors market movements, whale transactions, and new listings
"""

import requests
import time
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class BNBAlerts:
    """Real-time BNB chain monitoring and alerting system"""
    
    def __init__(self):
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        self.bscscan_base = "https://api.bscscan.com/api"
        self.dexscreener_base = "https://api.dexscreener.com/latest/dex"
        
        # Alert thresholds
        self.price_alert_threshold = 10.0  # 10% price movement
        self.volume_alert_threshold = 1000000  # $1M volume spike
        self.whale_threshold = 100000  # $100K+ transactions
        
        # Tracked tokens
        self.tracked_tokens = {
            'BNB': 'binancecoin',
            'CAKE': 'pancakeswap-token',
            'TWT': 'trust-wallet-token',
            'XVS': 'venus',
            'ALPACA': 'alpaca-finance',
            'BIFI': 'beefy-finance-2'
        }
        
        # Recent alerts to avoid spam
        self.recent_alerts = {}
        self.alert_cooldown = 300  # 5 minutes between same alerts
    
    def get_bnb_price_data(self) -> Optional[Dict]:
        """Get current BNB price and market data"""
        try:
            url = f"{self.coingecko_base}/coins/binancecoin"
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
            
            return {
                'price': market_data.get('current_price', {}).get('usd', 0),
                'change_24h': market_data.get('price_change_percentage_24h', 0),
                'volume_24h': market_data.get('total_volume', {}).get('usd', 0),
                'market_cap': market_data.get('market_cap', {}).get('usd', 0),
                'high_24h': market_data.get('high_24h', {}).get('usd', 0),
                'low_24h': market_data.get('low_24h', {}).get('usd', 0)
            }
            
        except Exception as e:
            logger.error(f"Error fetching BNB price data: {e}")
            return None
    
    def get_bsc_trending_tokens(self) -> List[Dict]:
        """Get trending BSC tokens from DexScreener"""
        try:
            url = f"{self.dexscreener_base}/tokens/trending"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            pairs = data.get('pairs', [])
            
            # Filter for BSC pairs
            bsc_pairs = [pair for pair in pairs if pair.get('chainId') == 'bsc']
            
            trending_tokens = []
            for pair in bsc_pairs[:10]:  # Top 10 trending
                base_token = pair.get('baseToken', {})
                quote_token = pair.get('quoteToken', {})
                
                if quote_token.get('symbol') == 'WBNB':  # BNB pairs only
                    trending_tokens.append({
                        'symbol': base_token.get('symbol', ''),
                        'name': base_token.get('name', ''),
                        'address': base_token.get('address', ''),
                        'price': float(pair.get('priceUsd', 0)),
                        'price_change_24h': float(pair.get('priceChange', {}).get('h24', 0)),
                        'volume_24h': float(pair.get('volume', {}).get('h24', 0)),
                        'liquidity': float(pair.get('liquidity', {}).get('usd', 0)),
                        'dex_url': pair.get('url', ''),
                        'pair_address': pair.get('pairAddress', '')
                    })
            
            return trending_tokens
            
        except Exception as e:
            logger.error(f"Error fetching trending BSC tokens: {e}")
            return []
    
    def check_price_alerts(self) -> List[Dict]:
        """Check for significant price movements"""
        alerts = []
        
        # Check BNB price
        bnb_data = self.get_bnb_price_data()
        if bnb_data:
            change_24h = abs(bnb_data['change_24h'])
            if change_24h >= self.price_alert_threshold:
                alert_key = f"bnb_price_{int(change_24h)}"
                if self._should_alert(alert_key):
                    alerts.append({
                        'type': 'price_alert',
                        'token': 'BNB',
                        'price': bnb_data['price'],
                        'change_24h': bnb_data['change_24h'],
                        'volume_24h': bnb_data['volume_24h'],
                        'message': self._format_price_alert('BNB', bnb_data)
                    })
                    self._record_alert(alert_key)
        
        # Check trending tokens
        trending_tokens = self.get_bsc_trending_tokens()
        for token in trending_tokens:
            change_24h = abs(token['price_change_24h'])
            if change_24h >= self.price_alert_threshold:
                alert_key = f"{token['symbol']}_price_{int(change_24h)}"
                if self._should_alert(alert_key):
                    alerts.append({
                        'type': 'price_alert',
                        'token': token['symbol'],
                        'price': token['price'],
                        'change_24h': token['price_change_24h'],
                        'volume_24h': token['volume_24h'],
                        'address': token['address'],
                        'dex_url': token['dex_url'],
                        'message': self._format_price_alert(token['symbol'], token)
                    })
                    self._record_alert(alert_key)
        
        return alerts
    
    def check_volume_alerts(self) -> List[Dict]:
        """Check for unusual volume spikes"""
        alerts = []
        
        trending_tokens = self.get_bsc_trending_tokens()
        for token in trending_tokens:
            volume_24h = token['volume_24h']
            if volume_24h >= self.volume_alert_threshold:
                alert_key = f"{token['symbol']}_volume_{int(volume_24h/1000000)}M"
                if self._should_alert(alert_key):
                    alerts.append({
                        'type': 'volume_alert',
                        'token': token['symbol'],
                        'volume_24h': volume_24h,
                        'price': token['price'],
                        'liquidity': token['liquidity'],
                        'address': token['address'],
                        'dex_url': token['dex_url'],
                        'message': self._format_volume_alert(token)
                    })
                    self._record_alert(alert_key)
        
        return alerts
    
    def check_new_listings(self) -> List[Dict]:
        """Check for new token listings (simplified version)"""
        alerts = []
        
        # This would ideally use a real-time API or webhook
        # For now, we'll check for very new tokens with low liquidity
        trending_tokens = self.get_bsc_trending_tokens()
        for token in trending_tokens:
            liquidity = token['liquidity']
            if liquidity < 100000 and liquidity > 10000:  # New but not dead
                alert_key = f"{token['symbol']}_new_listing"
                if self._should_alert(alert_key):
                    alerts.append({
                        'type': 'new_listing',
                        'token': token['symbol'],
                        'name': token['name'],
                        'address': token['address'],
                        'liquidity': liquidity,
                        'price': token['price'],
                        'dex_url': token['dex_url'],
                        'message': self._format_new_listing_alert(token)
                    })
                    self._record_alert(alert_key)
        
        return alerts
    
    def _format_price_alert(self, symbol: str, data: Dict) -> str:
        """Format price alert message"""
        change = data['change_24h']
        emoji = "🚀" if change > 0 else "📉"
        direction = "PUMP" if change > 0 else "DUMP"
        
        if symbol == 'BNB':
            return f"{emoji} BNB {direction} ALERT!\n\n" \
                   f"Price: ${data['price']:,.2f}\n" \
                   f"24h Change: {change:+.2f}%\n" \
                   f"Volume: ${data['volume_24h']:,.0f}\n\n" \
                   f"#BNB #BSC #Alert"
        else:
            return f"{emoji} {symbol} {direction} ALERT!\n\n" \
                   f"Price: ${data['price']:.6f}\n" \
                   f"24h Change: {change:+.2f}%\n" \
                   f"Volume: ${data['volume_24h']:,.0f}\n\n" \
                   f"Contract: {data.get('address', 'N/A')[:10]}...\n" \
                   f"#BSC #DeFi #Alert"
    
    def _format_volume_alert(self, token: Dict) -> str:
        """Format volume alert message"""
        volume_m = token['volume_24h'] / 1000000
        return f"📊 {token['symbol']} VOLUME SPIKE!\n\n" \
               f"24h Volume: ${volume_m:.1f}M\n" \
               f"Price: ${token['price']:.6f}\n" \
               f"Liquidity: ${token['liquidity']:,.0f}\n\n" \
               f"Contract: {token['address'][:10]}...\n" \
               f"#BSC #Volume #Alert"
    
    def _format_new_listing_alert(self, token: Dict) -> str:
        """Format new listing alert message"""
        return f"🆕 NEW BSC TOKEN ALERT!\n\n" \
               f"{token['name']} ({token['symbol']})\n" \
               f"Price: ${token['price']:.8f}\n" \
               f"Liquidity: ${token['liquidity']:,.0f}\n\n" \
               f"Contract: {token['address'][:10]}...\n" \
               f"⚠️ DYOR - New tokens are risky!\n" \
               f"#BSC #NewListing #DeFi"
    
    def _should_alert(self, alert_key: str) -> bool:
        """Check if we should send this alert (avoid spam)"""
        now = time.time()
        last_alert = self.recent_alerts.get(alert_key, 0)
        return (now - last_alert) > self.alert_cooldown
    
    def _record_alert(self, alert_key: str):
        """Record that we sent this alert"""
        self.recent_alerts[alert_key] = time.time()
    
    def get_all_alerts(self) -> List[Dict]:
        """Get all current alerts"""
        all_alerts = []
        all_alerts.extend(self.check_price_alerts())
        all_alerts.extend(self.check_volume_alerts())
        all_alerts.extend(self.check_new_listings())
        return all_alerts
    
    def format_alert_for_tweet(self, alert: Dict) -> str:
        """Format alert for X posting"""
        return alert['message']

def main():
    """Test the alerts system"""
    alerts = BNBAlerts()
    
    print("BNB Chain Alerts System Test")
    print("=" * 50)
    
    # Test price alerts
    price_alerts = alerts.check_price_alerts()
    print(f"Price alerts: {len(price_alerts)}")
    
    # Test volume alerts
    volume_alerts = alerts.check_volume_alerts()
    print(f"Volume alerts: {len(volume_alerts)}")
    
    # Test new listings
    new_listings = alerts.check_new_listings()
    print(f"New listings: {len(new_listings)}")
    
    # Show all alerts
    all_alerts = alerts.get_all_alerts()
    print(f"\nTotal alerts: {len(all_alerts)}")
    
    for alert in all_alerts:
        print(f"\n{alert['type'].upper()} ALERT:")
        print(alerts.format_alert_for_tweet(alert))

if __name__ == "__main__":
    main()
