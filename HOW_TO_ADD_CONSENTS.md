# How to Add Consents and Understanding Privacy Health Score

## Question 1: How to Add Consent to Show in "Manage Consent"

### Where Consents Come From

Consents are displayed on the **Manage Consent** page by querying the `Consent` database table. The page shows all consents grouped by organization.

**File**: `/app.py` lines 382-397
```python
@app.route('/consents')
@login_required
def consents():
    all_consents = Consent.query.filter_by(user_id=current_user.id).all()
    consents_by_org = {}
    for consent in all_consents:
        org = Organisation.query.get(consent.organisation_id)
        if org.name not in consents_by_org:
            consents_by_org[org.name] = {
                'organisation': org,
                'consents': []
            }
        consents_by_org[org.name]['consents'].append(consent)
    return render_template('consents.html', consents_by_org=consents_by_org)
```

### Method 1: Add Consent Directly in Database (Quick Test)

Using Python, run this in a Flask shell:

```python
from app import app, db
from database import Consent, User
from datetime import datetime

with app.app_context():
    # Get demo user (user_id = 1)
    # Add new consent for Tech Corp (org_id = 1)
    new_consent = Consent(
        user_id=1,
        organisation_id=1,
        purpose='Newsletter Subscription',
        consent_type='gdpr',
        status='active',
        granted_at=datetime.utcnow()
    )
    db.session.add(new_consent)
    db.session.commit()
    print("Consent added successfully!")
```

### Method 2: Create an Add Consent Route (Recommended)

Add this route to `app.py`:

```python
@app.route('/add-consent', methods=['GET', 'POST'])
@login_required
def add_consent():
    if request.method == 'POST':
        org_id = request.form.get('organisation_id')
        purpose = request.form.get('purpose')
        
        new_consent = Consent(
            user_id=current_user.id,
            organisation_id=org_id,
            purpose=purpose,
            consent_type='gdpr',
            status='active'
        )
        db.session.add(new_consent)
        db.session.commit()
        
        log_audit("add_consent", "consent", org_id, f"Purpose: {purpose}")
        flash('Consent added successfully', 'success')
        return redirect(url_for('consents'))
    
    organisations = Organisation.query.all()
    return render_template('add_consent.html', organisations=organisations)
```

### Method 3: Auto-Create Demo Consents (Already Done)

Your `app.py` already creates sample consents on initialization (lines 60-64):

```python
# Create consents
consents = [
    Consent(user_id=demo_user.id, organisation_id=1, purpose='Data processing', consent_type='gdpr', status='active'),
    Consent(user_id=demo_user.id, organisation_id=2, purpose='Marketing emails', consent_type='gdpr', status='active'),
    Consent(user_id=demo_user.id, organisation_id=3, purpose='Order fulfillment', consent_type='gdpr', status='active'),
]
```

**To see these consents**: Login as `demo` / `demo123` and go to "Manage Consents"

---

## Question 2: Privacy Health Score - NOT Hard Coded

### Where Does the 70% Come From?

**File**: `/app.py` lines 318-340
```python
def dashboard():
    # ... get data_sources ...
    
    # Calculate privacy health score
    total_orgs = len(data_sources)
    active_consents = Consent.query.filter_by(user_id=current_user.id, status='active').count()
    total_consents = Consent.query.filter_by(user_id=current_user.id).count()
    
    # Calculate health score
    health_score = 70  # <-- Base score
    
    # If you have more active consents withdrawn, score decreases
    if total_consents > 0:
        consent_ratio = active_consents / total_consents
        health_score += int((0.5 - consent_ratio) * 20)  # Up to +20 if all active
    
    # If you have more than 5 orgs, score decreases
    if total_orgs > 5:
        health_score -= (total_orgs - 5) * 2  # -2 per org over 5
    
    # Ensure score stays between 0-100
    health_score = max(0, min(100, health_score))
```

### How the Score is Calculated

**Base Score**: 70 (starting point)

**Consent Adjustment** (max ±20 points):
- If 50% or more consents are active: +20 points (reaches 90)
- If 50% consents withdrawn: 0 adjustment
- If all consents withdrawn: -20 points (reaches 50)
- Formula: `(0.5 - consent_ratio) * 20`

**Organization Penalty** (max -∞):
- Each organisation over 5: -2 points
- Example: 7 orgs = -4 points

**Final Score**: Clamped between 0 and 100

### Example Scenarios

| Scenario | Calc | Score |
|----------|------|-------|
| Demo user (3 orgs, 3 active consents) | 70 + int((0.5-1.0)*20) - 0 = 70 + (-10) = | **60** |
| 5 orgs, all consents withdrawn | 70 + int((0.5-0)*20) - 0 = 70 + 10 = | **80** |
| 10 orgs, 50% consents withdrawn | 70 + 0 - (10-5)*2 = 70 + 0 - 10 = | **60** |

### How to Customize the Score

Edit `app.py` line 331 to change the base score:

```python
health_score = 50  # Changed from 70 to 50
```

Or change the consent weight (line 334):

```python
health_score += int((0.5 - consent_ratio) * 30)  # Changed from 20 to 30 for more impact
```

Or change the org penalty (line 337):

```python
if total_orgs > 3:  # Changed from 5
    health_score -= (total_orgs - 3) * 3  # Changed penalty from 2 to 3
```

---

## Summary

- **To add consents**: Either add to database directly or create an `/add-consent` route
- **The 70% is NOT hardcoded**: It's dynamically calculated based on your consents and organizations
- **All demo consents already exist**: Login as `demo` to see them in "Manage Consents"
