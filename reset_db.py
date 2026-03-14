#!/usr/bin/env python3
"""
Database Reset Script
Deletes the old database and creates a fresh one with all new tables
Run this to fix: "no such column: consent.consent_type"
"""

import os
import sys
from pathlib import Path

# Add the project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import app, db
from database import User, Organisation, DataSource, DataItem, Consent, CCPAOptOut, SubjectAccessRequest, AuditLog, UserPreference
from werkzeug.security import generate_password_hash

def reset_database():
    """Reset the database to fresh state with new schema"""
    
    # Path to database file
    db_path = project_root / 'instance' / 'privacy.db'
    
    print("[DB RESET] Starting database reset...")
    
    # Delete old database if it exists
    if db_path.exists():
        print(f"[DB RESET] Deleting old database at {db_path}")
        db_path.unlink()
        print("[DB RESET] Old database deleted")
    else:
        print("[DB RESET] No existing database found, creating new one")
    
    # Also check for privacy.db in root directory
    root_db = project_root / 'privacy.db'
    if root_db.exists():
        print(f"[DB RESET] Deleting old database at {root_db}")
        root_db.unlink()
        print("[DB RESET] Old root database deleted")
    
    with app.app_context():
        print("[DB RESET] Creating all tables with new schema...")
        db.create_all()
        print("[DB RESET] All tables created successfully")
        
        # Create demo user
        print("[DB RESET] Creating demo user...")
        demo_user = User(
            username='demo',
            email='demo@privacyfirst.local',
            password=generate_password_hash('demo123')
        )
        db.session.add(demo_user)
        db.session.flush()
        
        # Create sample organisations
        print("[DB RESET] Creating sample organisations...")
        orgs = [
            Organisation(name='Tech Corp', description='Cloud storage and productivity platform', logo='☁️'),
            Organisation(name='Social Networks Inc', description='Social media and communication platform', logo='👥'),
            Organisation(name='E-Commerce Store', description='Online shopping and retail platform', logo='🛍️')
        ]
        for org in orgs:
            db.session.add(org)
        db.session.flush()
        
        # Create data sources and items
        print("[DB RESET] Creating sample data sources and items...")
        for i, org in enumerate(orgs, 1):
            ds = DataSource(user_id=demo_user.id, organisation_id=org.id, status='active')
            db.session.add(ds)
            db.session.flush()
            
            # Sample data items
            if i == 1:  # Tech Corp
                items = [
                    DataItem(data_source_id=ds.id, category='personal', name='Full Name', value='John Demo', purpose='Account identification'),
                    DataItem(data_source_id=ds.id, category='personal', name='Email Address', value='demo@privacyfirst.local', purpose='Communication'),
                    DataItem(data_source_id=ds.id, category='location', name='Last Login Location', value='Lagos, Nigeria', purpose='Security'),
                ]
            elif i == 2:  # Social Networks
                items = [
                    DataItem(data_source_id=ds.id, category='personal', name='Profile Name', value='Demo User', purpose='Profile display'),
                    DataItem(data_source_id=ds.id, category='personal', name='Bio', value='Privacy-conscious user', purpose='Profile info'),
                    DataItem(data_source_id=ds.id, category='location', name='Current City', value='Lagos', purpose='Location features'),
                ]
            else:  # E-Commerce
                items = [
                    DataItem(data_source_id=ds.id, category='personal', name='Shipping Address', value='123 Demo Street, Lagos', purpose='Order delivery'),
                    DataItem(data_source_id=ds.id, category='financial', name='Account Type', value='Premium Member', purpose='Membership'),
                    DataItem(data_source_id=ds.id, category='personal', name='Purchase History', value='15 purchases', purpose='Recommendations'),
                ]
            
            for item in items:
                db.session.add(item)
        
        db.session.flush()
        
        # Create consents with the new consent_type field
        print("[DB RESET] Creating sample consents...")
        consents = [
            Consent(user_id=demo_user.id, organisation_id=1, purpose='Data processing', consent_type='gdpr', status='active'),
            Consent(user_id=demo_user.id, organisation_id=2, purpose='Marketing emails', consent_type='gdpr', status='active'),
            Consent(user_id=demo_user.id, organisation_id=3, purpose='Order fulfillment', consent_type='gdpr', status='active'),
        ]
        for consent in consents:
            db.session.add(consent)
        
        # Create user preferences
        print("[DB RESET] Creating user preferences...")
        prefs = UserPreference(user_id=demo_user.id, language='en', theme='light', newsletter=True)
        db.session.add(prefs)
        
        # Commit all changes
        db.session.commit()
        print("[DB RESET] Demo data committed to database")
        
    print("[DB RESET] SUCCESS! Database has been reset with new schema")
    print("[DB RESET] Login with: demo / demo123")
    return True

if __name__ == '__main__':
    try:
        reset_database()
        sys.exit(0)
    except Exception as e:
        print(f"[DB RESET] ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
