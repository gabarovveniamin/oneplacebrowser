# Google OAuth Setup Guide for Comet Browser

## Prerequisites
- Google Cloud Project
- OAuth 2.0 Desktop Application credentials

## Setup Steps

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the following APIs:
   - Google+ API
   - People API

### 2. Create OAuth 2.0 Credentials
1. Go to **Credentials** in Google Cloud Console
2. Click **Create Credentials** → **OAuth client ID**
3. Choose **Desktop application**
4. Accept the default settings and click **Create**
5. A JSON file will be downloaded - this is your credentials file

### 3. Configure Comet Browser
1. Run the browser once - it will create `~/.comet_browser/google_credentials.json`
2. When prompted, either:
   - Copy your downloaded credentials JSON to that location, OR
   - Click "Sign in with Google" and complete the authentication

### 4. First Run
```bash
cd myaichrome
python -m src.main
```

## Features Enabled

✅ **Google OAuth Authentication**
   - Sign in with your Google account
   - User data is securely stored locally

✅ **History Tracking**
   - Complete browsing history with timestamps
   - Search history by URL or title
   - View → History menu

✅ **Bookmarks**
   - Add bookmarks from the toolbar (☆ button)
   - View bookmarks from View → Bookmarks
   - Delete bookmarks you no longer need

✅ **User Management**
   - User info displayed in the toolbar
   - Separate history for each authenticated user
   - Clear history option with confirmation

## Files Generated
- `~/.comet_browser/browser.db` - SQLite database for history/bookmarks
- `~/.comet_browser/user_data.json` - Stored user information
- `~/.comet_browser/google_credentials.json` - OAuth credentials
- `~/.comet_browser/google_token.json` - OAuth refresh token

## Troubleshooting

**"Could not retrieve user information"**
- Check that credentials JSON is properly configured
- Make sure People API is enabled in Google Cloud Console

**"Sign in failed"**
- Verify your Google credentials JSON file is in `~/.comet_browser/`
- Check that OAuth consent screen is configured in Google Cloud Console

**History not saving**
- Make sure you're signed in (icon shows user name, not "Guest")
- Check that `~/.comet_browser/` directory is writable
