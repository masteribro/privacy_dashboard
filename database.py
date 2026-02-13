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
    status = db.Column(db.String(20), default='active')  # active, withdrawn
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    withdrawn_at = db.Column(db.DateTime, nullable=True)