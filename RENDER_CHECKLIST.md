# 🚀 Render Deployment Checklist

Complete this checklist before deploying to Render.com

## Pre-Deployment Setup

- [ ] Have a GitHub account and push code to a repository
- [ ] Create Render.com account (free tier available)
- [ ] Have your Telegram bot token from @BotFather
- [ ] Know your channel URL (e.g., https://t.me/yourchannel)
- [ ] Verify bot is admin in all target channels
- [ ] All target channel IDs are correct in `config.py`

## Code Preparation

- [ ] `.env` file is in `.gitignore` (prevent secrets in git)
- [ ] `requirements.txt` is up to date
- [ ] `runtime.txt` specifies Python 3.13
- [ ] `Procfile` exists for background worker
- [ ] `render.yaml` is configured
- [ ] No hardcoded tokens or secrets in code

## Configuration Verification

- [ ] `config.py` loads BOT_TOKEN from environment variables
- [ ] `config.py` handles missing `.env` gracefully
- [ ] Channel list is correct in `config.py`
- [ ] Owner ID is set correctly

## File Checklist

Required files for Render deployment:
- [ ] `bot.py` - Main bot file
- [ ] `config.py` - Configuration
- [ ] `requirements.txt` - Python dependencies
- [ ] `runtime.txt` - Python version (3.13)
- [ ] `Procfile` - Start command
- [ ] `render.yaml` - Render configuration
- [ ] `.gitignore` - Exclude sensitive files
- [ ] `handlers/` - Handler modules
- [ ] `middleware/` - Middleware modules
- [ ] `utils/` - Utility modules

## Deployment Steps

1. **Prepare Repository**
   - [ ] Initialize git repository
   - [ ] Commit all files
   - [ ] Push to GitHub

2. **Create Render Service**
   - [ ] Connect GitHub repository
   - [ ] Select "Background Worker"
   - [ ] Set Python 3.13 as runtime

3. **Configure Environment Variables**
   - [ ] Add `BOT_TOKEN`
   - [ ] Add `SHARE_LINK`
   - [ ] Set `ENVIRONMENT=production`
   - [ ] Set `LOG_LEVEL=INFO`
   - [ ] Set `REMOVE_LINKS=true`

4. **Deploy**
   - [ ] Click "Create Service"
   - [ ] Wait for build to complete
   - [ ] Check logs for startup messages

## Post-Deployment Verification

- [ ] Bot starts without errors (check Logs tab)
- [ ] Bot responds to `/start` command
- [ ] Test message posts to channels
- [ ] Check Render logs for any errors
- [ ] Verify channel links work in messages

## Monitoring

- [ ] Check logs daily initially
- [ ] Monitor for any error patterns
- [ ] Test posting regularly
- [ ] Keep GitHub repository updated with changes
- [ ] Update environment variables if needed

## Troubleshooting

If something isn't working:

1. Check the **Logs** tab in Render dashboard
2. Look for error messages
3. Verify all environment variables are set
4. Ensure bot token is correct
5. Check channel IDs and permissions
6. Review [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed troubleshooting

## Updating on Render

To deploy new changes:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render automatically redeploys when you push to main branch!

## Quick Links

- [Render Dashboard](https://dashboard.render.com)
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Detailed guide
- [python-telegram-bot Docs](https://python-telegram-bot.readthedocs.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

**Ready to deploy!** Follow the steps above and your bot will be running 24/7 on Render.com 🎉
