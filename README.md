# BNB Bible Bot

A comprehensive X (Twitter) bot that combines spiritual inspiration with BNB ecosystem insights, posting daily Bible verses and BNB market analysis.

## Features

- **Daily Bible Verses**: Posts inspiring Bible verses in English and Chinese threads
- **BNB Market Analysis**: 24-hour BNB price, volume, and market cap updates
- **Trending Coins**: BSC ecosystem trending tokens and market movements
- **Ecosystem News**: Curated BNB ecosystem news and developments
- **Upcoming Projects**: YZi Labs and Binance-backed projects
- **AI-Powered**: Uses Ollama (Llama 3) for intelligent verse selection based on market sentiment
- **API Optimized**: Stays within X free tier limits (500 posts/month)

## Requirements

- Python 3.8+
- X (Twitter) API access (free tier)
- Ollama with Llama 3 model
- Internet connection

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama**:
   ```bash
   # Install Ollama (visit https://ollama.ai for installation instructions)
   # Pull the Llama 3 model
   ollama pull llama3
   ```

4. **Set up X API credentials**:
   - Copy `env_template.txt` to `.env`
   - Fill in your X API credentials:
     ```
     X_API_KEY=your_api_key_here
     X_API_SECRET=your_api_secret_here
     X_ACCESS_TOKEN=your_access_token_here
     X_ACCESS_TOKEN_SECRET=your_access_token_secret_here
     ```

5. **Get X API credentials**:
   - Go to [X Developer Portal](https://developer.twitter.com/)
   - Create a new app
   - Generate API keys and access tokens
   - Ensure your app has read and write permissions

## Usage

### Basic Usage

Run the complete BNB daily routine:
```bash
python bnb_bot.py
```

### Specific Commands

**Run morning routine (4 posts)**:
```bash
python scheduler.py
```

**Test connections**:
```bash
python -c "from bnb_bot import BNBBibleBot; print('Bot ready!')"
```

### Scheduling

#### Option 1: Cron (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add daily posting at 8 AM UTC
0 8 * * * cd /path/to/bot && python bot.py

# Add interaction runs 3x daily
0 10 * * * cd /path/to/bot && python bot.py interact
0 14 * * * cd /path/to/bot && python bot.py interact
0 18 * * * cd /path/to/bot && python bot.py interact
```

#### Option 2: Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to daily at 8:00 AM
4. Set action to start program: `python`
5. Add arguments: `bot.py`
6. Set start in: your bot directory

#### Option 3: GitHub Actions (Free)
Create `.github/workflows/bot.yml`:
```yaml
name: Bible Verse Bot
on:
  schedule:
    - cron: '0 8 * * *'  # 8 AM UTC daily
jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run bot
        env:
          X_API_KEY: ${{ secrets.X_API_KEY }}
          X_API_SECRET: ${{ secrets.X_API_SECRET }}
          X_ACCESS_TOKEN: ${{ secrets.X_ACCESS_TOKEN }}
          X_ACCESS_TOKEN_SECRET: ${{ secrets.X_ACCESS_TOKEN_SECRET }}
        run: python bot.py
```

## Configuration

### Target Accounts
Edit `config.py` to modify target accounts:
```python
TARGET_ACCOUNTS = {
    'VitalikButerin': '295218901',
    'saylor': '244647486',
    # Add more accounts...
}
```

### Daily Themes
Modify daily themes in `config.py`:
```python
DAILY_THEMES = {
    'monday': 'hope',
    'tuesday': 'wisdom',
    # Customize themes...
}
```

### Rate Limiting
Adjust interaction limits in `.env`:
```
MAX_INTERACTIONS_PER_DAY=5
```

## File Structure

```
├── bot.py              # Main bot script
├── bible_api.py        # Bible API integration
├── ai_module.py        # Ollama AI integration
├── x_api.py           # X (Twitter) API integration
├── config.py          # Configuration settings
├── requirements.txt   # Python dependencies
├── .env.template     # Environment variables template
├── .env              # Your API credentials (create this)
├── README.md         # This file
└── bot.log           # Log file (created when running)
```

## API Usage

### Bible API
- Uses `bible-api.com` (free, no key required)
- Fetches Chinese Union Version (CUV) verses
- Includes comprehensive book name mapping

### X API
- Uses X API v2 with OAuth 1.0a
- Free tier supports posting and reading
- Rate limited to stay within free tier

### Ollama AI
- Local AI model (Llama 3)
- Analyzes post themes
- Suggests relevant Bible verses
- No external API costs

## Monitoring

- Check `bot.log` for detailed logs
- Monitor your X account for posts
- Verify interactions are appropriate
- Check API usage in X Developer Portal

## Troubleshooting

### Common Issues

**"Ollama connection failed"**:
- Ensure Ollama is running: `ollama serve`
- Verify Llama 3 is installed: `ollama list`
- Install if missing: `ollama pull llama3`

**"Missing X API credentials"**:
- Check `.env` file exists and has correct credentials
- Verify API keys have proper permissions
- Ensure no extra spaces in credentials

**"Failed to post tweet"**:
- Check X API rate limits
- Verify account has posting permissions
- Check tweet content for policy violations

**"No suitable tweets found"**:
- Target accounts may not have recent posts
- Posts may not meet relevance criteria
- Check if accounts are still active

### Debug Mode

Run with verbose logging:
```bash
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
import bot
bot.main()
"
```

## Cost Analysis

- **X API**: Free tier (1,500 tweets/month)
- **Bible API**: Free (bible-api.com)
- **Ollama**: Free (local AI)
- **Hosting**: Free (local machine or GitHub Actions)
- **Total**: $0/month

## Compliance

- Bot status disclosed in bio
- Rate limited to avoid spam
- Respectful, inspirational content only
- Follows X Terms of Service
- Non-proselytizing approach

## Support

For issues or questions:
1. Check the logs in `bot.log`
2. Verify all dependencies are installed
3. Test individual components with `python bot.py test`
4. Check X API status and rate limits

## License

This project is for educational and personal use. Please respect X's Terms of Service and use responsibly.
