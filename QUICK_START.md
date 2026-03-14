# Quick Start Guide

## What Was Fixed

1. **Database Error Fixed** - The dashboard, consents, and data requests now work without database errors
2. **CCPA Removed** - All California-specific privacy references have been replaced with general privacy preferences suitable for Nigeria and globally
3. **Auto-Setup** - The app now automatically creates the database and demo data on first run

## How to Run

### On Your Local Machine

```bash
# 1. Install dependencies (if not already done)
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser and go to
http://localhost:5000

# 4. Log in with demo account
Username: demo
Password: demo123
```

### Demo Features Now Working

After logging in, you can:

1. **Dashboard** - View privacy health score and summary
2. **My Data** - See all connected organizations and your data with sensitivity indicators
3. **Consents** - Manage and withdraw your consents
4. **Data Requests** - Submit Subject Access Requests (GDPR Article 15)
5. **Privacy Preferences** - Control data sharing and targeted advertising (localized for you)
6. **Audit Logs** - See complete history of all your actions
7. **Data Flow** - Visual diagram of how data moves through the ecosystem
8. **Privacy Policy, Terms, Data Processing** - Legal documentation pages

## Key Changes from Original

### ✅ Fixed
- Database automatically initializes on startup
- No more "no such column" errors
- All pages load correctly

### 🌍 Localized
- Removed CCPA (California law) references
- Replaced with universal privacy preferences
- Still fully GDPR compliant
- Suitable for Nigeria and global users

### 📝 Terminology Changed
- "CCPA Settings" → "Privacy Preferences"
- "Opt-out of data sales" → "Opt-out of data sharing"
- All legal references updated to be location-agnostic

## File Structure

```
privacy_dashboard/
├── app.py                          # Main Flask app
├── database.py                     # SQLAlchemy models
├── requirements.txt                # Python dependencies
├── templates/
│   ├── base.html                  # Navigation & layout
│   ├── dashboard.html             # Home page
│   ├── mydata.html                # Your data overview
│   ├── consents.html              # Consent management
│   ├── data_requests.html         # SAR requests
│   ├── privacy_preferences.html   # NEW - Privacy settings
│   ├── audit_logs.html            # Activity logs
│   ├── data_flow.html             # Data visualization
│   ├── privacy_policy.html        # Legal page
│   ├── terms_of_service.html      # Legal page
│   └── data_processing.html       # Legal page
├── static/
│   └── style.css                  # Styling
├── QUICK_START.md                 # This file
├── FIXES_APPLIED.md               # What was fixed
└── SETUP_DATABASE.md              # Database troubleshooting
```

## Troubleshooting

### "ModuleNotFoundError" when running app
```bash
pip install -r requirements.txt
```

### Database errors still appearing
```bash
# Delete old database and restart
rm privacy.db  # or rm instance/privacy.db
python app.py
```

### Can't log in
- Use exactly: `demo` / `demo123`
- Check that the database initialized (look for "[DB INIT]" messages in terminal)

### Wrong password for demo
- Password is hardcoded as `demo123` in `app.py` line 41
- To change it, edit that line and restart

## About Your Location

The application previously had California-specific (CCPA) language because it was built as an academic project template. This has now been corrected to be:

- Globally compatible
- GDPR compliant (primary regulation)
- Suitable for Nigeria and any other jurisdiction
- Universal privacy principles (no location lock-in)

All privacy controls work the same way regardless of location!

## Need Help?

Check these files:
- **Setup issues** → `SETUP_DATABASE.md`
- **What changed** → `FIXES_APPLIED.md`
- **Database problems** → Run `python init_db.py` to reinitialize

## Demo Data Provided

The app comes with sample data pre-loaded:
- 3 Organizations (Tech Corp, Social Networks, E-Commerce Store)
- Various data items in different categories
- Sample consents
- Audit trail history

This is just for demonstration - all data is simulated and local to your machine.

Happy privacy managing!
