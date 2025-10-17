# GitHub Actions Setup for BNB Bible Bot

This guide will help you set up GitHub Actions to run your BNB Bible Bot automatically in the cloud.

## Benefits of GitHub Actions

- ✅ **Free hosting** (2000 minutes/month for public repos)
- ✅ **Automatic scheduling** (cron jobs)
- ✅ **Manual triggering** (run on demand)
- ✅ **No server maintenance** required
- ✅ **Automatic scaling** and reliability
- ✅ **Built-in logging** and monitoring

## Setup Steps

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `bnb-bible-bot`
3. Make it **public** (for free GitHub Actions minutes)
4. Upload all your bot files to the repository

### 2. Set Up Repository Secrets

Go to your repository → **Settings** → **Secrets and variables** → **Actions**

Add these secrets (click "New repository secret" for each):

#### Required Secrets:
```
X_API_KEY = your_x_api_key
X_API_SECRET = your_x_api_secret
X_ACCESS_TOKEN = your_x_access_token
X_ACCESS_TOKEN_SECRET = your_x_access_token_secret
```

#### Optional Secrets:
```
X_CLIENT_ID = your_x_client_id
X_CLIENT_SECRET = your_x_client_secret
BOT_USERNAME = your_bot_username
POSTING_TIME = 08:00
MAX_INTERACTIONS_PER_DAY = 5
BSCSCAN_API_KEY = your_bscscan_api_key
```

### 3. Upload Bot Files

Upload these files to your repository:
- `bnb_bot.py`
- `bible_api.py`
- `ai_module.py`
- `x_api.py`
- `config.py`
- `bnb_analysis.py`
- `bnb_alerts.py`
- `bnb_interactive.py`
- `bnb_onchain_analytics.py`
- `bnb_trading_integrations.py`
- `scheduler.py`
- `requirements.txt`
- `.github/workflows/bnb-bot.yml`

### 4. Test the Workflow

1. Go to **Actions** tab in your repository
2. Click on **BNB Bible Bot** workflow
3. Click **Run workflow** → **Run workflow** (manual trigger)
4. Select action: `morning`, `insights`, `interactions`, or `full`
5. Click **Run workflow**

## Schedule Overview

The bot runs automatically at these times (UTC):

| Time | Action | Description |
|------|--------|-------------|
| 8:00 AM | Morning Routine | Bible verse + BNB analysis + trending coins + projects |
| 10:00 AM | BNB Insights | Market analysis and insights |
| 12:00 PM | Interactions | Reply to mentions and engage |
| 2:00 PM | BNB Insights | Market analysis and insights |
| 4:00 PM | Interactions | Reply to mentions and engage |
| 6:00 PM | BNB Insights | Market analysis and insights |
| 8:00 PM | Interactions | Reply to mentions and engage |

## Manual Triggers

You can manually trigger the bot anytime:

1. Go to **Actions** → **BNB Bible Bot**
2. Click **Run workflow**
3. Choose what to run:
   - **morning**: Full morning routine (4 posts)
   - **insights**: BNB market insights
   - **interactions**: Reply to mentions
   - **full**: Complete daily routine

## Monitoring

### View Logs
1. Go to **Actions** tab
2. Click on any workflow run
3. Click on **run-bot** job
4. View detailed logs

### Check Status
- ✅ Green checkmark = Success
- ❌ Red X = Failed
- 🟡 Yellow circle = Running

## Troubleshooting

### Common Issues

1. **"Missing X API credentials"**
   - Check that all secrets are set correctly
   - Verify secret names match exactly

2. **"Ollama connection failed"**
   - This is normal - Ollama installs automatically
   - First run may take longer

3. **"Rate limit exceeded"**
   - Bot will retry automatically
   - Check X API usage limits

4. **"Workflow failed"**
   - Check the logs in Actions tab
   - Verify all files are uploaded correctly

### Rate Limits

GitHub Actions free tier:
- **Public repos**: 2000 minutes/month
- **Private repos**: 500 minutes/month

Your bot uses ~2-3 minutes per run, so you can run it ~600-1000 times per month for free!

## Customization

### Change Schedule
Edit `.github/workflows/bnb-bot.yml` and modify the cron expressions:

```yaml
schedule:
  - cron: '0 8 * * *'  # 8:00 AM UTC daily
  - cron: '0 20 * * *' # 8:00 PM UTC daily
```

### Add More Actions
Add new jobs in the workflow file:

```yaml
- name: Custom Action
  run: |
    python -c "from bnb_bot import BNBBibleBot; bot = BNBBibleBot(); bot.custom_function()"
```

## Security Notes

- ✅ Secrets are encrypted and never visible in logs
- ✅ Each run gets a fresh environment
- ✅ No persistent storage between runs
- ✅ Automatic cleanup after each run

## Cost

- **GitHub Actions**: Free (2000 minutes/month)
- **X API**: Free tier (500 posts/month)
- **CoinGecko API**: Free tier
- **Bible API**: Free
- **Ollama**: Free (runs in GitHub Actions)

**Total cost: $0/month!** 🎉

## Next Steps

1. Set up your GitHub repository
2. Add all the secrets
3. Upload your bot files
4. Test with a manual run
5. Let it run automatically!

Your bot will now run 24/7 in the cloud without any server maintenance required!
