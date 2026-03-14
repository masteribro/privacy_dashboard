# What Happens When You Create a New Account

## Key Difference: Demo Account vs New Account

### Demo Account (demo / demo123)
- **Gets sample data**: 3 organizations with data already connected
- **Has pre-made consents**: 3 consents already set up
- **Has audit logs**: Some activity history
- **Privacy score**: Shows ~60% (calculated from consents)
- **Purpose**: For testing/demonstration

### New Account (When You Register)
- **Starts completely empty**: No organizations connected
- **No consents**: Manage Consents page is empty
- **No data sources**: My Data page is empty
- **No audit logs**: Audit Logs page is empty
- **Privacy score**: Shows 100% (perfect score because no data is being collected)
- **Purpose**: Real user account

---

## Registration Flow

1. **Create Account**
   ```
   Username: yourname
   Email: your@email.com
   Password: secure123
   ```

2. **After Registration**
   - User record is created in database
   - Password is hashed (bcrypt)
   - UserPreference record created (default: English, light theme)
   - Redirected to login page

3. **After Login**
   - User session is created
   - Redirected to dashboard
   - Dashboard shows empty state (0 organizations, 0 data items)

---

## Empty New Account Dashboard

When you login as a new user, you'll see:

```
Your Privacy Health Score
├─ 100% (Perfect!)
│  └─ Reason: No data collected = no privacy risk
│
├─ Organizations: 0
├─ Data Items: 0
├─ Consents: 0
└─ Recommendations
   └─ "Start by connecting your first organization..."
```

### Why 100%?
New accounts have a **perfect privacy score** because:
- No organizations connected = no data shared
- No active consents = no permissions given
- No audit logs = clean activity history

---

## What You Can Do With a New Account

1. **Add Consents Manually**
   - Currently not available in UI (demo only)
   - Can add via Python/database directly
   - See `HOW_TO_ADD_CONSENTS.md`

2. **Create Data Requests**
   - Request a copy of your data (even though you have none)
   - Good for testing the SAR workflow

3. **View Privacy Preferences**
   - Set opt-out preferences for future organizations
   - All empty until you add organizations

4. **Check Audit Logs**
   - Will show your login/logout activities
   - Empty on first login

5. **Access Legal Pages**
   - Privacy Policy
   - Terms of Service
   - Data Processing Information

---

## Database Records Created for New User

When you register as `johndoe`, these records are created:

```
users table:
├─ id: 5 (auto-incremented)
├─ username: johndoe
├─ email: john@example.com
├─ password: (bcrypt hashed)
└─ created_at: 2026-03-14 22:30:00

user_preference table:
├─ user_id: 5
├─ language: en
├─ theme: light
└─ newsletter: true

audit_logs table:
└─ (empty until user takes actions)

No records created in:
├─ data_sources (empty)
├─ data_items (empty)
├─ consents (empty)
├─ ccpa_opt_out (empty)
├─ subject_access_request (empty)
└─ (etc.)
```

---

## How to Add Sample Data to New Account

If you want to add sample data to your new account:

### Option 1: Via Python Shell
```python
from app import app, db
from database import User, Organisation, DataSource, DataItem, Consent

with app.app_context():
    # Get your user
    user = User.query.filter_by(username='johndoe').first()
    
    # Create an organization
    org = Organisation(name='My Bank', description='Online Banking', logo='🏦')
    db.session.add(org)
    db.session.flush()
    
    # Connect user to organization
    ds = DataSource(user_id=user.id, organisation_id=org.id, status='active')
    db.session.add(ds)
    db.session.flush()
    
    # Add a data item
    item = DataItem(
        data_source_id=ds.id,
        category='financial',
        name='Account Balance',
        value='₦500,000',
        purpose='Balance display'
    )
    db.session.add(item)
    
    # Add consent
    consent = Consent(
        user_id=user.id,
        organisation_id=org.id,
        purpose='Financial services',
        consent_type='gdpr',
        status='active'
    )
    db.session.add(consent)
    db.session.commit()
```

### Option 2: Using Reset Script
```bash
# Reset database and create demo user
python reset_db.py
```

---

## Privacy Score for New Users

Since new users start with **0 organizations** and **0 active data collections**:

```
Privacy Score = 70 (base)
              + int((0.5 - 0/0) * 20)  [undefined - treated as 0]
              - (0 - 5) * 2  [no penalty]
              = 70 (capped at 100 for new users)
```

**Result: 100% Privacy Score** (Perfect protection)

Once you add organizations and consents, the score will adjust based on how many consents you've given out.

---

## Summary Table

| Feature | Demo Account | New Account |
|---------|--------------|-------------|
| Organizations | 3 pre-loaded | 0 (empty) |
| Data Items | ~12 items | 0 (empty) |
| Consents | 3 active | 0 (empty) |
| Audit Logs | Has history | Empty |
| Privacy Score | ~60% | 100% |
| Data Requests | Can download | No data to download |
| Status | Demo/Test | Real user |

---

## Next Steps

1. **Create a new account** and explore the empty state
2. **Try data requests** to see the SAR workflow
3. **Add consents manually** via Python (see HOW_TO_ADD_CONSENTS.md)
4. **Test audit logs** - they'll show your actions
5. **Check privacy score changes** as you add data

