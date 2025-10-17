"""
Scheduler for Bible Verse Bot
Runs the bot on a schedule when hosted on always-on services
"""

import schedule
import time
import logging
import sys
from datetime import datetime
from bnb_bot import BNBBibleBot

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_bnb_morning_routine():
    """Run BNB morning routine (4 posts)"""
    try:
        logger.info("Starting BNB morning routine...")
        bot = BNBBibleBot()
        
        # Morning posts
        bot.post_morning_scripture()
        bot.post_bnb_ecosystem_news()
        bot.post_bsc_trending_coins()
        bot.post_upcoming_bnb_projects()
        
        logger.info("BNB morning routine completed")
    except Exception as e:
        logger.error(f"Error in BNB morning routine: {e}")

def run_bnb_daily():
    """Run BNB-focused daily routine"""
    try:
        logger.info("Starting BNB daily routine...")
        bot = BNBBibleBot()
        result = bot.run_bnb_daily_routine()
        logger.info(f"BNB daily routine completed: {result}")
    except Exception as e:
        logger.error(f"Error in BNB daily routine: {e}")

def run_bnb_interactions():
    """Run BNB interactions only"""
    try:
        logger.info("Starting BNB interactions...")
        bot = BNBBibleBot()
        count = bot.run_bnb_interactions()
        logger.info(f"BNB interactions completed: {count}")
    except Exception as e:
        logger.error(f"Error in BNB interactions: {e}")

def run_bnb_insights():
    """Run BNB insights posting"""
    try:
        logger.info("Starting BNB insights...")
        bot = BNBBibleBot()
        # Post various BNB content
        bot.post_bnb_insight()
        bot.post_bnb_security_tip()
        bot.post_bnb_educational_content()
        logger.info("BNB insights completed")
    except Exception as e:
        logger.error(f"Error in BNB insights: {e}")

def main():
    """Main scheduler function"""
    logger.info("Bible Verse Bot Scheduler starting...")
    
    # Schedule BNB morning routine at 8 AM UTC (4 posts)
    schedule.every().day.at("08:00").do(run_bnb_morning_routine)
    
    # Schedule BNB insights throughout the day
    schedule.every().day.at("10:00").do(run_bnb_insights)
    schedule.every().day.at("14:00").do(run_bnb_insights)
    schedule.every().day.at("18:00").do(run_bnb_insights)
    
    # Schedule BNB interactions
    schedule.every().day.at("12:00").do(run_bnb_interactions)
    schedule.every().day.at("16:00").do(run_bnb_interactions)
    schedule.every().day.at("20:00").do(run_bnb_interactions)
    
    logger.info("BNB-focused scheduler configured:")
    logger.info("- BNB morning routine: 8:00 AM UTC (inspiration + news + trending + projects)")
    logger.info("- BNB insights: 10:00 AM, 2:00 PM, 6:00 PM UTC")
    logger.info("- BNB interactions: 12:00 PM, 4:00 PM, 8:00 PM UTC")
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
