from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# This creates the database object
db = SQLAlchemy()

# User Model - stores user accounts
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: one user has many data sources
    data_sources = db.relationship('DataSource', backref='user', lazy=True)

# Organisation Model - companies that hold your data
class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    logo = db.Column(db.String(200))  # emoji or icon name
    
    # Relationship
    data_sources = db.relationship('DataSource', backref='organisation', lazy=True)

# DataSource Model - connects users to organisations
class DataSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)
    connected_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, disconnected
    
    # Relationship
    data_items = db.relationship('DataItem', backref='data_source', lazy=True)

# DataItem Model - individual pieces of data
class DataItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_source_id = db.Column(db.Integer, db.ForeignKey('data_source.id'), nullable=False)
    category = db.Column(db.String(50))  # personal, financial, location
    name = db.Column(db.String(100))     # e.g., "Email Address"
    value = db.Column(db.String(500))    # e.g., "user@example.com"
    purpose = db.Column(db.String(200))  # why they have it
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Consent Model - permissions you've given
class Consent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)
    purpose = db.Column(db.String(100))   # e.g., "Marketing emails"
    consent_type = db.Column(db.String(20), default='gdpr')  # gdpr, ccpa
    status = db.Column(db.String(20), default='active')  # active, withdrawn, opted_out
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    withdrawn_at = db.Column(db.DateTime, nullable=True)

# CCPA Opt-Out Model - California Consumer Privacy Act opt-outs
class CCPAOptOut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)
    opt_out_type = db.Column(db.String(50))  # sale, sharing, targeted_advertising
    opted_out_at = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(500), nullable=True)

# Subject Access Request Model - GDPR Article 15
class SubjectAccessRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, completed, rejected
    data_format = db.Column(db.String(20), default='json')  # json, csv
    completed_at = db.Column(db.DateTime, nullable=True)
    rejection_reason = db.Column(db.String(500), nullable=True)
    description = db.Column(db.String(500))

# Audit Log Model - tracks all user actions
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100))  # view_data, export_data, withdraw_consent, etc
    resource_type = db.Column(db.String(50))  # organisation, consent, data_item, request
    resource_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.String(500))  # additional info about the action
    ip_address = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='success')  # success, failed

# User Preferences Model - language and display preferences
class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    language = db.Column(db.String(10), default='en')  # en, es, fr, de
    theme = db.Column(db.String(20), default='light')  # light, dark
    newsletter = db.Column(db.Boolean, default=True)  # privacy newsletters
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
