# Database Issues - Complete Fix Guide

## Problem Summary

Your application is experiencing database schema errors:
- **Error**: `sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: consent.consent_type`
- **Cause**: The old database file still has the OLD schema without the new columns (`consent_type`, etc.)
- **Routing Error**: `BuildError: Could not build url for endpoint 'ccpa_settings'` - Route was renamed to `privacy_preferences`

## Solution

### Step 1: Fix the Broken Route Reference (ALREADY DONE)
✅ Updated `templates/data_flow.html` to use `privacy_preferences` instead of `ccpa_settings`

### Step 2: Reset Your Database

The automatic initialization code didn't work because the old database file still exists. We need to delete it and create a fresh one.

#### Option A: Using the Reset Script (RECOMMENDED)

```bash
cd ~/VsProject/privacy_dashboard

# Run the reset script
python reset_db.py
```

This will:
- Delete the old database file
- Create a new database with the correct schema
- Seed demo data
- Create demo user (demo / demo123)

#### Option B: Manual Reset

If the script doesn't work, do this manually:

1. **Find and delete the old database:**
   ```bash
   # Check for database in instance folder
   rm -f ~/VsProject/privacy_dashboard/instance/privacy.db
   
   # Also check root folder
   rm -f ~/VsProject/privacy_dashboard/privacy.db
   ```

2. **Delete Python cache:**
   ```bash
   find ~/VsProject/privacy_dashboard -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
   find ~/VsProject/privacy_dashboard -type f -name "*.pyc" -delete
   ```

3. **Restart Flask:**
   ```bash
   # Kill any running Flask processes
   lsof -i :5000
   kill -9 <PID>
   
   # Restart
   python app.py
   ```

## What Changed

### Files Modified:
- ✅ `templates/data_flow.html` - Fixed broken `ccpa_settings` route reference
- ✅ `app.py` - Has auto-initialization code that will run on next startup

### Files Added:
- ✅ `reset_db.py` - Database reset utility script

## After Fixing

1. **Login**: `demo` / `demo123`
2. **Test Dashboard**: Click "Dashboard" - should work now
3. **Test Data Flow**: Click "Data Flow" - should work now
4. **Test All Pages**: Try all navigation links

## If You Still Get Errors

### Error: "Address already in use"
```bash
lsof -i :5000
kill -9 <PID>
python app.py
```

### Error: "no such column" still shows
1. Double-check database is deleted: `ls -la ~/VsProject/privacy_dashboard/instance/privacy.db`
2. Run reset script again: `python reset_db.py`
3. If still failing, delete all database files and restart Flask

### Error: "Could not build url for endpoint"
The route names were updated from `ccpa_settings` to `privacy_preferences`. This should be fixed in the updated code.

## Verification Checklist

After running `reset_db.py`, verify:

- [ ] Database file exists at: `instance/privacy.db`
- [ ] Can login with: `demo` / `demo123`
- [ ] Dashboard page loads without errors
- [ ] Data Flow page loads without errors
- [ ] Privacy Preferences page loads (no CCPA-specific content)
- [ ] Audit Logs page loads
- [ ] Data Requests page loads
- [ ] Consents page loads
- [ ] My Data page loads with demo data

## Technical Details

### New Database Schema
The reset script creates these NEW tables with proper columns:

1. **consent** - Now has `consent_type` field (gdpr)
2. **ccpa_opt_out** - New table for privacy preferences
3. **subject_access_request** - New table for SAR workflow
4. **audit_log** - New table for action tracking
5. **user_preference** - New table for user settings

### Demo Data Seeded
- **User**: demo / demo123
- **Organizations**: Tech Corp, Social Networks Inc, E-Commerce Store
- **Data Items**: ~9 sample items across organizations
- **Consents**: 3 active consents

## Support

If you continue to have issues:

1. Check that Flask is running on port 5000
2. Verify Python virtual environment is activated
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Check database permissions: `ls -la instance/`
