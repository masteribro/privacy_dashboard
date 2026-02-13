from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, Organisation, DataSource, DataItem, Consent
from datetime import datetime
import random

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///privacy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create tables and sample data
@app.before_first_request
def create_tables():
    db.create_all()
    
    # Only add sample data if database is empty
    if Organisation.query.count() == 0:
        create_sample_organisations()
        create_sample_data_for_demo_user()

def create_sample_organisations():
    """Add some sample companies to the database"""
    organisations = [
        Organisation(name="🏦 SimulatedBank", description="Digital banking platform", logo="🏦"),
        Organisation(name="📱 SimulatedSocial", description="Social media network", logo="📱"),
        Organisation(name="🛒 SimulatedShop", description="Online marketplace", logo="🛒"),
        Organisation(name="🏥 SimulatedHealth", description="Healthcare provider", logo="🏥"),
        Organisation(name="📧 SimulatedEmail", description="Email service", logo="📧"),
        Organisation(name="🎵 SimulatedStream", description="Music streaming", logo="🎵"),
    ]
    
    for org in organisations:
        db.session.add(org)
    
    db.session.commit()
    print("✅ Sample organisations created!")

def create_sample_data_for_demo_user():
    """Create a demo user and sample data for testing"""
    # Check if demo user exists
    demo_user = User.query.filter_by(username='demo').first()
    if not demo_user:
        # Create demo user
        demo_user = User(
            username='demo',
            email='demo@example.com',
            password=generate_password_hash('password123')
        )
        db.session.add(demo_user)
        db.session.commit()
        
        # Get all organisations
        orgs = Organisation.query.all()
        
        # For each organisation, create a data source and sample data
        for org in orgs:
            # Create connection
            data_source = DataSource(
                user_id=demo_user.id,
                organisation_id=org.id,
                status='active'
            )
            db.session.add(data_source)
            db.session.flush()  # Get the ID
            
            # Add sample data items based on organisation type
            if 'Bank' in org.name:
                add_banking_data(data_source.id, demo_user.id, org.id)
            elif 'Social' in org.name:
                add_social_data(data_source.id, demo_user.id, org.id)
            elif 'Shop' in org.name:
                add_shopping_data(data_source.id, demo_user.id, org.id)
            elif 'Health' in org.name:
                add_health_data(data_source.id, demo_user.id, org.id)
            else:
                add_general_data(data_source.id, demo_user.id, org.id)
            
            # Add consents
            add_consents(demo_user.id, org.id)
        
        db.session.commit()
        print("✅ Sample data created for demo user!")

def add_banking_data(data_source_id, user_id, org_id):
    """Add sample banking data"""
    items = [
        DataItem(data_source_id=data_source_id, category="financial", name="Account Type", value="Current Account", purpose="Service provision"),
        DataItem(data_source_id=data_source_id, category="financial", name="Account Number", value="****1234", purpose="Service provision"),
        DataItem(data_source_id=data_source_id, category="financial", name="Sort Code", value="12-34-56", purpose="Service provision"),
        DataItem(data_source_id=data_source_id, category="financial", name="Balance", value="£1,234.56", purpose="Service provision"),
        DataItem(data_source_id=data_source_id, category="personal", name="Full Name", value="Demo User", purpose="Identity verification"),
        DataItem(data_source_id=data_source_id, category="personal", name="Email", value="demo@example.com", purpose="Contact"),
        DataItem(data_source_id=data_source_id, category="personal", name="Phone", value="+44 **** ****56", purpose="Contact"),
        DataItem(data_source_id=data_source_id, category="transaction", name="Last Transaction", value="Amazon - £29.99", purpose="Transaction history"),
    ]
    
    for item in items:
        db.session.add(item)

def add_social_data(data_source_id, user_id, org_id):
    """Add sample social media data"""
    items = [
        DataItem(data_source_id=data_source_id, category="personal", name="Display Name", value="DemoUser123", purpose="Profile"),
        DataItem(data_source_id=data_source_id, category="personal", name="Email", value="demo@example.com", purpose="Account"),
        DataItem(data_source_id=data_source_id, category="personal", name="Date of Birth", value="01/01/1990", purpose="Age verification"),
        DataItem(data_source_id=data_source_id, category="behavioural", name="Posts", value="157 posts", purpose="Service"),
        DataItem(data_source_id=data_source_id, category="behavioural", name="Followers", value="342", purpose="Service"),
        DataItem(data_source_id=data_source_id, category="behavioural", name="Following", value="289", purpose="Service"),
        DataItem(data_source_id=data_source_id, category="preference", name="Interests", value="Technology, Music, Travel", purpose="Personalisation"),
    ]
    
    for item in items:
        db.session.add(item)

def add_shopping_data(data_source_id, user_id, org_id):
    """Add sample e-commerce data"""
    items = [
        DataItem(data_source_id=data_source_id, category="personal", name="Full Name", value="Demo User", purpose="Delivery"),
        DataItem(data_source_id=data_source_id, category="personal", name="Email", value="demo@example.com", purpose="Order updates"),
        DataItem(data_source_id=data_source_id, category="address", name="Shipping Address", value="123 Demo Street, Leicester, UK", purpose="Delivery"),
        DataItem(data_source_id=data_source_id, category="payment", name="Payment Method", value="VISA ****4242", purpose="Payment"),
        DataItem(data_source_id=data_source_id, category="transaction", name="Order History", value="24 orders", purpose="Service"),
        DataItem(data_source_id=data_source_id, category="preference", name="Size Preferences", value="M, L", purpose="Recommendations"),
    ]
    
    for item in items:
        db.session.add(item)

def add_health_data(data_source_id, user_id, org_id):
    """Add sample health data"""
    items = [
        DataItem(data_source_id=data_source_id, category="health", name="Blood Type", value="O+", purpose="Medical records"),
        DataItem(data_source_id=data_source_id, category="personal", name="NHS Number", value="*** *** 1234", purpose="Identification"),
        DataItem(data_source_id=data_source_id, category="health", name="Allergies", value="Penicillin", purpose="Medical safety"),
        DataItem(data_source_id=data_source_id, category="appointment", name="Last Appointment", value="15 May 2025", purpose="Records"),
        DataItem(data_source_id=data_source_id, category="appointment", name="Next Appointment", value="20 June 2025", purpose="Reminders"),
    ]
    
    for item in items:
        db.session.add(item)

def add_general_data(data_source_id, user_id, org_id):
    """Add sample general data"""
    items = [
        DataItem(data_source_id=data_source_id, category="personal", name="Email Address", value="demo@example.com", purpose="Account"),
        DataItem(data_source_id=data_source_id, category="personal", name="Full Name", value="Demo User", purpose="Account"),
        DataItem(data_source_id=data_source_id, category="account", name="Account Created", value="January 2023", purpose="Records"),
        DataItem(data_source_id=data_source_id, category="account", name="Last Login", value="Today", purpose="Security"),
    ]
    
    for item in items:
        db.session.add(item)

def add_consents(user_id, org_id):
    """Add sample consents for an organisation"""
    consents = [
        Consent(user_id=user_id, organisation_id=org_id, purpose="Marketing emails", status="active"),
        Consent(user_id=user_id, organisation_id=org_id, purpose="Share with partners", status="withdrawn"),
        Consent(user_id=user_id, organisation_id=org_id, purpose="Personalisation", status="active"),
    ]
    
    for consent in consents:
        db.session.add(consent)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------------- ROUTES (Pages) ----------------------

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - shows privacy health score and overview"""
    
    # Get user's data
    data_sources = DataSource.query.filter_by(user_id=current_user.id, status='active').all()
    
    # Calculate privacy health score
    total_orgs = len(data_sources)
    
    # Get consents
    active_consents = Consent.query.filter_by(user_id=current_user.id, status='active').count()
    total_consents = Consent.query.filter_by(user_id=current_user.id).count()
    
    # Get data items count
    data_items_count = 0
    for ds in data_sources:
        data_items_count += DataItem.query.filter_by(data_source_id=ds.id).count()
    
    # Calculate health score (simple formula)
    health_score = 70  # Base score
    
    # More consents = lower score (you gave more permission)
    if total_consents > 0:
        consent_ratio = active_consents / total_consents
        health_score += int((0.5 - consent_ratio) * 20)
    
    # More organisations = lower score (more data out there)
    if total_orgs > 5:
        health_score -= (total_orgs - 5) * 2
    
    # Clamp between 0-100
    health_score = max(0, min(100, health_score))
    
    return render_template('dashboard.html', 
                          user=current_user,
                          total_orgs=total_orgs,
                          data_items_count=data_items_count,
                          active_consents=active_consents,
                          total_consents=total_consents,
                          health_score=health_score)

@app.route('/mydata')
@login_required
def mydata():
    """View all your data across organisations"""
    
    # Get all data sources for current user
    data_sources = DataSource.query.filter_by(user_id=current_user.id, status='active').all()
    
    # Organise data by organisation
    organisations_data = []
    
    for ds in data_sources:
        org = Organisation.query.get(ds.organisation_id)
        data_items = DataItem.query.filter_by(data_source_id=ds.id).all()
        
        # Group by category
        categories = {}
        for item in data_items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        
        organisations_data.append({
            'organisation': org,
            'data_source': ds,
            'categories': categories,
            'total_items': len(data_items)
        })
    
    return render_template('mydata.html', organisations_data=organisations_data)

@app.route('/consents')
@login_required
def consents():
    """View and manage consents"""
    
    # Get all consents for current user
    all_consents = Consent.query.filter_by(user_id=current_user.id).all()
    
    # Group by organisation
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

@app.route('/withdraw-consent/<int:consent_id>')
@login_required
def withdraw_consent(consent_id):
    """Withdraw a consent"""
    
    consent = Consent.query.get(consent_id)
    
    # Check if this consent belongs to the current user
    if consent and consent.user_id == current_user.id:
        consent.status = 'withdrawn'
        consent.withdrawn_at = datetime.utcnow()
        db.session.commit()
        flash('Consent withdrawn successfully', 'success')
    else:
        flash('Consent not found', 'danger')
    
    return redirect(url_for('consents'))

@app.route('/quick-demo')
def quick_demo():
    """Quick login as demo user for testing"""
    demo_user = User.query.filter_by(username='demo').first()
    if demo_user:
        login_user(demo_user)
        flash('Logged in as Demo User', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Demo user not found. Please check database.', 'danger')
        return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)