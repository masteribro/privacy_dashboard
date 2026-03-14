#!/usr/bin/env python3
"""
Database Initialization Script
This script initializes the database with all tables and demo data
"""

import os
import sys
from app import app, db
from database import (
    User, Organisation, DataSource, DataItem, Consent,
    CCPAOptOut, SubjectAccessRequest, AuditLog, UserPreference
)
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with tables and demo data"""
    with app.app_context():
        print("[INIT] Starting database initialization...")
        
        try:
            # Create all tables
            print("[INIT] Creating database tables...")
            db.create_all()
            print("[INIT] All tables created successfully")
            
            # Check if demo user already exists
            existing_user = User.query.filter_by(username='demo').first()
            
            if not existing_user:
                print("[INIT] Creating demo user...")
                
                # Create demo user
                demo_user = User(
                    username='demo',
                    email='demo@privacyfirst.local',
                    password=generate_password_hash('demo123')
                )
                db.session.add(demo_user)
                db.session.flush()  # Get the user ID
                
                # Create demo organisations
                orgs = [
                    Organisation(
                        name='Tech Corp',
                        description='Cloud storage and productivity platform',
                        logo='☁️'
                    ),
                    Organisation(
                        name='Social Networks Inc',
                        description='Social media and communication platform',
                        logo='👥'
                    ),
                    Organisation(
                        name='E-Commerce Store',
                        description='Online shopping and retail platform',
                        logo='🛍️'
                    )
                ]
                
                for org in orgs:
                    db.session.add(org)
                db.session.flush()
                
                # Create data sources
                for org in orgs:
                    ds = DataSource(
                        user_id=demo_user.id,
                        organisation_id=org.id,
                        status='active'
                    )
                    db.session.add(ds)
                db.session.flush()
                
                # Create data items for Tech Corp
                tech_items = [
                    DataItem(data_source_id=1, category='personal', name='Full Name', value='John Demo', purpose='Account identification'),
                    DataItem(data_source_id=1, category='personal', name='Email Address', value='demo@privacyfirst.local', purpose='Communication'),
                    DataItem(data_source_id=1, category='personal', name='Phone Number', value='+234-80-XXXX-XXXX', purpose='Two-factor authentication'),
                    DataItem(data_source_id=1, category='location', name='Last Login Location', value='Lagos, Nigeria', purpose='Security monitoring'),
                    DataItem(data_source_id=1, category='personal', name='Account Created', value='2024-01-15', purpose='Record keeping'),
                ]
                
                # Create data items for Social Networks
                social_items = [
                    DataItem(data_source_id=2, category='personal', name='Profile Name', value='Demo User', purpose='Profile display'),
                    DataItem(data_source_id=2, category='personal', name='Bio', value='Privacy-conscious user', purpose='Profile information'),
                    DataItem(data_source_id=2, category='location', name='Current City', value='Lagos', purpose='Location-based features'),
                    DataItem(data_source_id=2, category='personal', name='Account Status', value='Active', purpose='Service delivery'),
                    DataItem(data_source_id=2, category='personal', name='Follow Count', value='245', purpose='Analytics'),
                ]
                
                # Create data items for E-Commerce
                ecom_items = [
                    DataItem(data_source_id=3, category='personal', name='Shipping Address', value='123 Demo Street, Lagos', purpose='Order delivery'),
                    DataItem(data_source_id=3, category='financial', name='Account Type', value='Premium Member', purpose='Membership management'),
                    DataItem(data_source_id=3, category='personal', name='Purchase History', value='15 purchases in last year', purpose='Personalized recommendations'),
                    DataItem(data_source_id=3, category='personal', name='Wishlist Items', value='4 items saved', purpose='Product suggestions'),
                    DataItem(data_source_id=3, category='personal', name='Preferred Shipping', value='Express Delivery', purpose='Service optimization'),
                ]
                
                for item in tech_items + social_items + ecom_items:
                    db.session.add(item)
                
                # Create demo consents
                consents = [
                    Consent(user_id=demo_user.id, organisation_id=1, purpose='Data processing', consent_type='gdpr', status='active'),
                    Consent(user_id=demo_user.id, organisation_id=2, purpose='Marketing emails', consent_type='gdpr', status='active'),
                    Consent(user_id=demo_user.id, organisation_id=3, purpose='Order fulfillment', consent_type='gdpr', status='active'),
                ]
                
                for consent in consents:
                    db.session.add(consent)
                
                # Create demo user preference
                prefs = UserPreference(
                    user_id=demo_user.id,
                    language='en',
                    theme='light',
                    newsletter=True
                )
                db.session.add(prefs)
                
                db.session.commit()
                print("[INIT] Demo user and data created successfully")
                print("[INIT] Login with: username='demo', password='demo123'")
            else:
                print("[INIT] Demo user already exists - skipping data creation")
            
            print("\n[SUCCESS] Database initialization completed!")
            return True
            
        except Exception as e:
            print(f"\n[ERROR] Initialization failed: {str(e)}")
            print("[ERROR] Traceback:")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
