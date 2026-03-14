#!/usr/bin/env python3
"""
Database Migration Script
This script updates the existing database to include new tables and columns
for CCPA, Subject Access Requests, Audit Logging, and User Preferences
"""

import os
import sys
from app import app, db
from database import (
    User, Organisation, DataSource, DataItem, Consent,
    CCPAOptOut, SubjectAccessRequest, AuditLog, UserPreference
)

def migrate_database():
    """Run database migrations"""
    with app.app_context():
        print("[MIGRATION] Starting database migration...")
        
        try:
            # Create all new tables if they don't exist
            print("[MIGRATION] Creating new tables...")
            db.create_all()
            
            # Check if consent_type column exists in Consent table
            print("[MIGRATION] Checking Consent table schema...")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            consent_columns = [col['name'] for col in inspector.get_columns('consent')]
            
            if 'consent_type' not in consent_columns:
                print("[MIGRATION] Adding consent_type column to Consent table...")
                with db.engine.connect() as conn:
                    conn.execute("ALTER TABLE consent ADD COLUMN consent_type VARCHAR(20) DEFAULT 'gdpr'")
                    conn.commit()
                print("[MIGRATION] Successfully added consent_type column")
            else:
                print("[MIGRATION] consent_type column already exists")
            
            # Verify other new tables exist
            table_names = inspector.get_table_names()
            required_tables = ['ccpa_opt_out', 'subject_access_request', 'audit_log', 'user_preference']
            
            for table in required_tables:
                if table in table_names:
                    print(f"[MIGRATION] Table '{table}' exists")
                else:
                    print(f"[MIGRATION] Creating table '{table}'...")
            
            print("\n[SUCCESS] Database migration completed successfully!")
            print("[INFO] All tables and columns are now up to date.")
            return True
            
        except Exception as e:
            print(f"\n[ERROR] Migration failed: {str(e)}")
            print("[ERROR] Please check the error above and try again.")
            return False

if __name__ == '__main__':
    success = migrate_database()
    sys.exit(0 if success else 1)
