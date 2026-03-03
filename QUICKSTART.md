# Quick Start Guide - Comet Browser

## ⚡ Quick Start (2 minutes)

### 1. Install Dependencies
```bash
cd myaichrome
pip install -r requirements.txt
```

### 2. Run the Browser
```bash
python -m src.main
```

### 3. Choose Your Option
- **🔐 Sign in with Google** - Full features with custom history
- **👥 Continue as Guest** - Use browser without account

## 🎯 Feature Quick Reference

### View History
1. Click **View** menu
2. Select **History**
3. Search by typing in the search box
4. Double-click any entry to visit

### Add Bookmark
1. Visit a page
2. Click ☆ star button in toolbar
3. Bookmark is saved!

### View Bookmarks
1. Click **View** menu  
2. Select **Bookmarks**
3. Double-click to visit saved pages

### Clear History
1. Click **Edit** menu
2. Select **Clear History**
3. Confirm deletion

### Sign Out
Just close the browser and run again - you'll be prompted to log in or continue as guest.

## 📚 Full Documentation

- **[GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)** - OAuth configuration details
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical implementation details
- **[README.md](README.md)** - Full project documentation

## 🐛 Troubleshooting

**"Can't find QWebEngineView"**
```
pip install PyQt6-WebEngine==6.6.0
```

**"History not saving"**
- Make sure you're signed in (toolbar shows user name, not "Guest")
- Check that `~/.comet_browser/` directory exists

**"Bookmark dialog not opening"**
- Make sure you've visited at least one page
- Browser must be in focus

## 🎨 Features Installed

✅ Google OAuth authentication
✅ Complete browsing history  
✅ Bookmarks management
✅ User account system
✅ Search history
✅ Multi-user support
✅ Time-stamped history entries
✅ Guest mode (no login required)

## 🎓 What's New?

### History System
- **Automatic**: Every page you visit is automatically saved
- **Searchable**: Find pages by URL or title
- **Timestamped**: See exactly when you visited each page
- **Clearable**: Remove all history in one click
- **User-specific**: Each user has separate history

### OAuth Integration  
- **Secure**: Google's official authentication
- **Local**: Your data stays on your computer
- **Optional**: Guest mode available anytime
- **Seamless**: One-click login experience

### UI Improvements
- User profile display in toolbar
- Professional history/bookmarks dialogs
- Search functionality in all views
- Confirmation dialogs for destructive actions

---

**Need help?** Check the documentation files listed above or create an issue!
