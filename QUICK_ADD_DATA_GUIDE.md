# Quick Add Data Feature Guide

## Overview

The "Quick Add Data" feature allows new users to instantly populate their privacy dashboard with sample data without needing to use the Python command line. This feature is perfect for:

- Testing the dashboard functionality
- Learning how the privacy features work
- Demonstrating the app to others

## What Gets Added

When you click "Add Sample Data" on your dashboard, the following is automatically created:

### Organizations (3):
1. **TechFlow Cloud** - Cloud storage platform
2. **ConnectSocial** - Social media platform
3. **ShopHub Nigeria** - E-commerce platform

### Data Items (12 total):
Each organization has 4 data items across different categories:
- **Personal**: Name, Email, Bio, etc.
- **Location**: City, Last login location
- **Financial**: Account type, Payment info
- **Other**: Storage usage, Friends list, Purchase history

### Consents (3 total):
- One consent per organization
- All set to "GDPR" type
- All set to "Active" status
- Different purposes for each

### User Preferences:
- Language: English
- Theme: Light
- Newsletter: Enabled

## How to Use

### For New Users:

1. **Create a new account**
   - Go to Register page
   - Fill in username, email, and password
   - Click Register

2. **Login** with your new credentials

3. **View the Welcome Message**
   - Dashboard shows "Perfect Privacy Score: 100%"
   - Blue info box says "Welcome to Your Privacy Dashboard!"
   - Blue button: "Add Sample Data"

4. **Click "Add Sample Data"**
   - Page processes and creates all sample data
   - Success message appears
   - Dashboard refreshes with populated data

5. **Explore Features**
   - View My Data: See all 3 organizations and 12 data items
   - Manage Consents: See the 3 active consents
   - Privacy Score: Should drop to 60% (from added data)
   - Audit Logs: Will show the "populate_sample_data" action

## Data Structure

### Sample Data Per Organization

#### TechFlow Cloud
- Full Name: "User Account"
- Email Address: "user@example.com"
- Last Login Location: "Lagos, Nigeria"
- Storage Usage: "2.5 GB"

#### ConnectSocial
- Display Name: "User Profile"
- Bio/About: "Privacy-conscious user"
- Current City: "Lagos"
- Friends List: "127 connections"

#### ShopHub Nigeria
- Delivery Address: "Lagos, Nigeria"
- Account Type: "Premium Member"
- Purchase History: "5 recent orders"
- Phone Number: "+234xxxxxxxxxx"

## Privacy Score Impact

**Before Adding Data:**
- Score: 100% (perfect!)
- Reasoning: No data collected = perfect privacy

**After Adding Data:**
- Score: 60%
- Reasoning: 3 organizations × 3 active consents = 0.5 ratio
- Formula: 70 + int((0.5 - 1.0) × 20) = 60%

## Technical Details

### Backend Route: `/populate-sample-data`
- Method: POST
- Requires: Login
- Purpose: Creates sample data for new user

### What it Checks:
- User is logged in (required)
- User has no existing data
- If user already has data, shows warning

### Error Handling:
- If data already exists: "You already have data populated!"
- If error occurs: Transaction rolls back, error logged
- All actions are tracked in audit logs

### Audit Logging:
Every action is logged as:
- Action: "populate_sample_data"
- Resource Type: "user"
- Status: "success" or "failed"

## Customization

You can modify the sample data by editing the `populate_sample_data()` function in `app.py`:

```python
sample_orgs = [
    {
        'name': 'Your Organization Name',
        'description': 'Your description',
        'logo': '🔧'  # Your emoji
    }
]
```

## Removing Sample Data

To remove sample data and start fresh:

1. **Via Database:**
   ```python
   from app import db
   db.session.execute("DELETE FROM data_item WHERE id > 0")
   db.session.execute("DELETE FROM data_source WHERE id > 0")
   db.session.execute("DELETE FROM consent WHERE id > 0")
   db.session.execute("DELETE FROM organisation WHERE id > 0")
   db.session.commit()
   ```

2. **Via SQL:**
   Delete from tables in order: data_item → data_source → consent → organisation

3. **Via Reset:**
   Run `python reset_db.py` to reset entire database

## Testing the Feature

### Test Scenario 1: New User Journey
1. Create new account (testuser/test123)
2. See 100% privacy score
3. Click "Add Sample Data"
4. Verify 3 organizations appear
5. Check privacy score is now 60%

### Test Scenario 2: Existing Data Check
1. Login as demo
2. Try to add sample data again
3. Should get warning: "You already have data populated!"

### Test Scenario 3: Audit Trail
1. Create new account
2. Add sample data
3. Go to Audit Logs
4. Should see "populate_sample_data" action

## Troubleshooting

### Issue: Button doesn't appear
- Check: Are you logged in?
- Check: Do you already have organizations?
- Solution: Create new account if needed

### Issue: Data not appearing after clicking
- Refresh the page (Ctrl+R)
- Check dashboard stats (should show 3 organizations)
- Go to "My Data" page to see details

### Issue: Privacy score still 100%
- Dashboard may be cached
- Refresh page
- Logout and login again

## Future Enhancements

Possible improvements to this feature:

1. **Bulk Edit**: Edit sample data before adding
2. **Customization Modal**: Choose organizations to add
3. **Different Scenarios**: Easy/Medium/Hard privacy scenarios
4. **Export Templates**: Save custom datasets as templates
5. **Random Data**: Generate different data each time
