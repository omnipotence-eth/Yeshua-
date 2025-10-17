"""
X (Twitter) API integration for posting and interactions using OAuth 1.0a or OAuth 2.0
"""

import requests
from requests_oauthlib import OAuth1
import os
import logging
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class XAPI:
    def __init__(self):
        # X API credentials - try OAuth 2.0 first, then fall back to OAuth 1.0a
        self.client_id = os.getenv('X_CLIENT_ID')
        self.client_secret = os.getenv('X_CLIENT_SECRET')
        self.access_token = os.getenv('X_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')
        self.api_key = os.getenv('X_API_KEY')
        self.api_secret = os.getenv('X_API_SECRET')
        
        # Determine authentication method
        self.auth_method = None
        self.auth = None
        self.headers = {}
        
        # Use OAuth 1.0a (most reliable for posting)
        if all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            self.auth_method = "oauth1a"
            self.auth = OAuth1(
                self.api_key,
                self.api_secret,
                self.access_token,
                self.access_token_secret
            )
            logger.info("Using OAuth 1.0a authentication")
            
        # Fall back to OAuth 2.0 User Context (if we have client credentials)
        elif all([self.client_id, self.client_secret, self.access_token]):
            self.auth_method = "oauth2_user"
            # For OAuth 2.0 User Context, we need to use OAuth1 with the access token
            self.auth = OAuth1(
                self.client_id,
                client_secret=self.client_secret,
                resource_owner_key=self.access_token,
                resource_owner_secret=self.access_token_secret
            )
            logger.info("Using OAuth 2.0 User Context authentication")
            
        else:
            raise ValueError("Missing X API credentials. Please check your .env file.")
        
        # API endpoints
        self.base_url = "https://api.twitter.com/2"
        self.tweets_url = f"{self.base_url}/tweets"
        self.users_url = f"{self.base_url}/users"
        
        # Rate limiting tracking
        self.daily_interactions = 0
        self.max_daily_interactions = int(os.getenv('MAX_INTERACTIONS_PER_DAY', '3'))  # Reduced for threads
        self.daily_posts = 0
        self.max_daily_posts = int(os.getenv('MAX_POSTS_PER_DAY', '1'))  # 1 thread = 2 tweets
    
    def post_tweet(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Post a tweet using OAuth 2.0 User Context
        
        Args:
            text: Tweet content (max 280 characters)
            
        Returns:
            Response data or None if failed
        """
        try:
            if len(text) > 280:
                logger.warning(f"Tweet too long ({len(text)} chars), truncating...")
                text = text[:277] + "..."
            
            payload = {
                "text": text
            }
            
            logger.info(f"Posting tweet: {text[:50]}...")
            
            # Both OAuth 2.0 User Context and OAuth 1.0a use auth parameter
            response = requests.post(
                self.tweets_url,
                json=payload,
                auth=self.auth,
                timeout=30
            )
            
            if response.status_code == 201:
                data = response.json()
                logger.info(f"Tweet posted successfully: {data.get('data', {}).get('id')}")
                return data
            else:
                logger.error(f"Failed to post tweet: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error posting tweet: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error posting tweet: {e}")
            return None
    
    def post_thread(self, posts: List[str]) -> Optional[List[Dict[str, Any]]]:
        """
        Post a thread of tweets
        
        Args:
            posts: List of tweet texts (max 280 characters each)
            
        Returns:
            List of response data or None if failed
        """
        try:
            if not posts:
                logger.error("No posts provided for thread")
                return None
            
            thread_results = []
            previous_tweet_id = None
            
            for i, post_text in enumerate(posts):
                if len(post_text) > 280:
                    logger.warning(f"Tweet {i+1} too long ({len(post_text)} chars), truncating...")
                    post_text = post_text[:277] + "..."
                
                payload = {
                    "text": post_text
                }
                
                # If this is a reply in the thread, add reply context
                if previous_tweet_id:
                    payload["reply"] = {
                        "in_reply_to_tweet_id": previous_tweet_id
                    }
                
                logger.info(f"Posting thread tweet {i+1}/{len(posts)}: {post_text[:50]}...")
                
                # Both OAuth 2.0 User Context and OAuth 1.0a use auth parameter
                response = requests.post(
                    self.tweets_url,
                    json=payload,
                    auth=self.auth,
                    timeout=30
                )
                
                if response.status_code == 201:
                    data = response.json()
                    tweet_id = data.get('data', {}).get('id')
                    logger.info(f"Thread tweet {i+1} posted successfully: {tweet_id}")
                    thread_results.append(data)
                    previous_tweet_id = tweet_id
                    
                    # Small delay between thread posts to avoid rate limits
                    if i < len(posts) - 1:  # Don't delay after the last tweet
                        import time
                        time.sleep(1)
                else:
                    logger.error(f"Failed to post thread tweet {i+1}: {response.status_code} - {response.text}")
                    return None
            
            logger.info(f"Thread posted successfully: {len(thread_results)} tweets")
            self.daily_posts += 1  # Increment daily post counter
            return thread_results
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error posting thread: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error posting thread: {e}")
            return None
    
    def reply_to_tweet(self, text: str, reply_to_tweet_id: str) -> Optional[Dict[str, Any]]:
        """
        Reply to a specific tweet using OAuth 2.0
        
        Args:
            text: Reply content
            reply_to_tweet_id: ID of the tweet to reply to
            
        Returns:
            Response data or None if failed
        """
        try:
            if len(text) > 280:
                logger.warning(f"Reply too long ({len(text)} chars), truncating...")
                text = text[:277] + "..."
            
            payload = {
                "text": text,
                "reply": {
                    "in_reply_to_tweet_id": reply_to_tweet_id
                }
            }
            
            logger.info(f"Replying to tweet {reply_to_tweet_id}: {text[:50]}...")
            response = requests.post(
                self.tweets_url,
                json=payload,
                auth=self.auth,
                timeout=30
            )
            
            if response.status_code == 201:
                data = response.json()
                logger.info(f"Reply posted successfully: {data.get('data', {}).get('id')}")
                self.daily_interactions += 1
                return data
            else:
                logger.error(f"Failed to post reply: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error posting reply: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error posting reply: {e}")
            return None
    
    def get_user_tweets(self, user_id: str, max_results: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Get recent tweets from a user using OAuth 2.0
        
        Args:
            user_id: X user ID
            max_results: Maximum number of tweets to fetch (1-100)
            
        Returns:
            List of tweet data or None if failed
        """
        try:
            url = f"{self.users_url}/{user_id}/tweets"
            params = {
                "max_results": max(5, min(max_results, 100)),  # X API requires min 5
                "tweet.fields": "created_at,public_metrics,context_annotations",
                "exclude": "retweets,replies"  # Exclude retweets and replies
            }
            
            logger.info(f"Fetching tweets for user {user_id}...")
            response = requests.get(
                url,
                params=params,
                auth=self.auth,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                tweets = data.get('data', [])
                logger.info(f"Fetched {len(tweets)} tweets for user {user_id}")
                return tweets
            else:
                logger.error(f"Failed to fetch tweets: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching tweets: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching tweets: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get user data by username using OAuth 2.0
        
        Args:
            username: X username (without @)
            
        Returns:
            User data or None if failed
        """
        try:
            url = f"{self.users_url}/by/username/{username}"
            params = {
                "user.fields": "id,username,name,public_metrics"
            }
            
            logger.info(f"Fetching user data for @{username}...")
            response = requests.get(
                url,
                params=params,
                auth=self.auth,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('data')
                if user_data:
                    logger.info(f"Found user: {user_data.get('name')} (@{user_data.get('username')})")
                return user_data
            else:
                logger.error(f"Failed to fetch user data: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching user data: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching user data: {e}")
            return None
    
    def can_interact_today(self) -> bool:
        """
        Check if we can still interact today (rate limiting)
        
        Returns:
            True if we can still interact
        """
        return self.daily_interactions < self.max_daily_interactions
    
    def can_post_today(self) -> bool:
        """
        Check if we can still post today (rate limiting)
        
        Returns:
            True if we can still post
        """
        return self.daily_posts < self.max_daily_posts
    
    def get_remaining_interactions(self) -> int:
        """
        Get remaining interactions for today
        
        Returns:
            Number of remaining interactions
        """
        return max(0, self.max_daily_interactions - self.daily_interactions)
    
    def reset_daily_counter(self):
        """Reset daily interaction counter (call this daily)"""
        self.daily_interactions = 0
        logger.info("Daily interaction counter reset")
    
    def reset_daily_posts(self):
        """Reset daily posts counter (for testing)"""
        self.daily_posts = 0
        logger.info("Daily posts counter reset")
    
    def get_recommended_bio(self) -> str:
        """
        Get the recommended bio text for bot disclosure
        
        Returns:
            Recommended bio text
        """
        return "🤖 Daily Bible verses in English & Chinese\nAutomated account - not monitored 24/7"
    
    def update_bio(self, bio_text: str = None) -> bool:
        """
        Update bot bio with disclosure
        
        Args:
            bio_text: Bio text to set (uses recommended if None)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if bio_text is None:
                bio_text = self.get_recommended_bio()
            
            logger.info("=" * 60)
            logger.info("X BIO UPDATE REQUIRED")
            logger.info("=" * 60)
            logger.info(f"Recommended bio text:")
            logger.info(f"'{bio_text}'")
            logger.info("=" * 60)
            logger.info("Please manually update your X bio with the text above")
            logger.info("Go to: X.com → Profile → Edit Profile → Bio")
            logger.info("=" * 60)
            return True
        except Exception as e:
            logger.error(f"Error updating bio: {e}")
            return False
    
    def get_tweet_text(self, tweet_data: Dict[str, Any]) -> str:
        """
        Extract text content from tweet data
        
        Args:
            tweet_data: Tweet data from API
            
        Returns:
            Tweet text content
        """
        return tweet_data.get('text', '')
    
    def get_tweet_id(self, tweet_data: Dict[str, Any]) -> str:
        """
        Extract ID from tweet data
        
        Args:
            tweet_data: Tweet data from API
            
        Returns:
            Tweet ID
        """
        return tweet_data.get('id', '')
    
    def is_recent_tweet(self, tweet_data: Dict[str, Any], hours_threshold: int = 24) -> bool:
        """
        Check if tweet is recent enough for interaction
        
        Args:
            tweet_data: Tweet data from API
            hours_threshold: Hours threshold for "recent"
            
        Returns:
            True if tweet is recent
        """
        try:
            from datetime import datetime, timezone, timedelta
            
            created_at = tweet_data.get('created_at')
            if not created_at:
                return False
            
            # Parse the timestamp
            tweet_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            threshold_time = datetime.now(timezone.utc) - timedelta(hours=hours_threshold)
            
            return tweet_time > threshold_time
            
        except Exception as e:
            logger.error(f"Error checking tweet recency: {e}")
            return False
