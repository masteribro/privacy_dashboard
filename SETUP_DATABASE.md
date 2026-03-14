# Database Setup Instructions

Due to the new features added (Audit Logging, Subject Access Requests, Privacy Preferences), the database schema needs to be updated. Follow these steps:

## Option 1: Automatic Migration (Recommended)

The database will automatically create all new tables on first run. However, if you're getting errors about missing columns in the `consent` table, run the migration script:

```bash
python migrate_db.py
```

## Option 2: Manual Database Reset (If Issues Persist)

If you encounter persistent database errors:

1. **Delete the old database:**
   ```bash
   rm instance/privacy_dashboard.db
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

   The database will be automatically created with the new schema.

3. **Seed demo data:**
   The demo data will be created automatically when you first access the dashboard.

## What Changed

The following new tables were added:
- `ccpa_opt_out` - Tracks user privacy preferences
- `subject_access_request` - Manages data request workflows
- `audit_log` - Records all user actions for compliance
- `user_preference` - Stores user language and theme preferences

The `consent` table also gained a new `consent_type` column.

## Verification

After running the migration, verify that the application works by:
1. Logging in with the demo account
2. Navigating to Dashboard - should load without errors
3. Going to "My Data" - should display data properly
4. Clicking "Data Requests" - should show the new interface
5. Clicking "Privacy Preferences" - should show privacy settings

## Troubleshooting

If you still see errors:
- Make sure Python 3.7+ is installed
- Check that Flask and SQLAlchemy are properly installed
- Delete the database and restart the application

For more help, check the traceback in the terminal output.
