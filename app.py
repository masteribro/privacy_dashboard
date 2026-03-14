from flask import Flask, render_template, redirect, url_for, request, flash, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, Organisation, DataSource, DataItem, Consent, CCPAOptOut, SubjectAccessRequest, AuditLog, UserPreference
from datetime import datetime
import json

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'f7a9e3c1b2d5a8e4c6f1a3b9d2e5c8a17b4e6f8a2c9d1b3e5f7a8c0d2e4f6a8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///privacy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ========== DATABASE AUTO-INITIALIZATION ==========
with app.app_context():
    # Create all tables if they don't exist
    db.create_all()
    
    # Check if demo user exists, if not create it
    demo_user = User.query.filter_by(username='demo').first()
    if not demo_user:
        print("[DB INIT] Creating demo user...")
        demo_user = User(
            username='demo',
            email='demo@privacyfirst.local',
            password=generate_password_hash('demo123')
        )
        db.session.add(demo_user)
        db.session.flush()
        
        # Create sample organisations and data
        orgs = [
            Organisation(name='Tech Corp', description='Cloud storage and productivity platform', logo='☁️'),
            Organisation(name='Social Networks Inc', description='Social media and communication platform', logo='👥'),
            Organisation(name='E-Commerce Store', description='Online shopping and retail platform', logo='🛍️')
        ]
        for org in orgs:
            db.session.add(org)
        db.session.flush()
        
        # Create data sources and items
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
        
        # Create consents
        consents = [
            Consent(user_id=demo_user.id, organisation_id=1, purpose='Data processing', consent_type='gdpr', status='active'),
            Consent(user_id=demo_user.id, organisation_id=2, purpose='Marketing emails', consent_type='gdpr', status='active'),
            Consent(user_id=demo_user.id, organisation_id=3, purpose='Order fulfillment', consent_type='gdpr', status='active'),
        ]
        for consent in consents:
            db.session.add(consent)
        
        # Create user preferences
        prefs = UserPreference(user_id=demo_user.id, language='en', theme='light', newsletter=True)
        db.session.add(prefs)
        
        db.session.commit()
        print("[DB INIT] Demo data created successfully!")

# ========== ALL FUNCTIONS DEFINED HERE ==========

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

# ========== ROUTES ==========

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])  # THIS WAS MISSING!
def login():
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if username exists
        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        # Check if email exists
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
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
    
    # Calculate health score
    health_score = 70
    if total_consents > 0:
        consent_ratio = active_consents / total_consents
        health_score += int((0.5 - consent_ratio) * 20)
    
    if total_orgs > 5:
        health_score -= (total_orgs - 5) * 2
    
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
    data_sources = DataSource.query.filter_by(user_id=current_user.id, status='active').all()
    
    organisations_data = []
    
    for ds in data_sources:
        org = Organisation.query.get(ds.organisation_id)
        data_items = DataItem.query.filter_by(data_source_id=ds.id).all()
        
        categories = {}
        for item in data_items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        
        organisations_data.append({
            'organisation': org,
            'categories': categories,
            'total_items': len(data_items)
        })
    
    log_audit("view_mydata", "user", current_user.id, "Viewed personal data")
    return render_template('mydata.html', organisations_data=organisations_data)

@app.route('/data-flow')
@login_required
def data_flow():
    """Data flow visualization showing how data moves through the ecosystem"""
    log_audit("view_data_flow", "user", current_user.id, "Viewed data flow visualization")
    return render_template('data_flow.html')

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

@app.route('/withdraw-consent/<int:consent_id>')
@login_required
def withdraw_consent(consent_id):
    consent = Consent.query.get(consent_id)
    
    if consent and consent.user_id == current_user.id:
        consent.status = 'withdrawn'
        consent.withdrawn_at = datetime.utcnow()
        db.session.commit()
        flash('Consent withdrawn successfully', 'success')
    else:
        flash('Consent not found', 'danger')
    
    return redirect(url_for('consents'))

@app.route('/export-data')
@login_required
def export_data():
    data_sources = DataSource.query.filter_by(user_id=current_user.id).all()
    
    export_data = {
        'user': current_user.username,
        'email': current_user.email,
        'created_at': str(current_user.created_at),
        'export_date': str(datetime.now()),
        'organisations': []
    }
    
    for ds in data_sources:
        org = Organisation.query.get(ds.organisation_id)
        items = DataItem.query.filter_by(data_source_id=ds.id).all()
        
        org_data = {
            'name': org.name,
            'connected_since': str(ds.connected_at),
            'data_items': [{'category': i.category, 'name': i.name, 'value': i.value, 'purpose': i.purpose} 
                          for i in items]
        }
        export_data['organisations'].append(org_data)
    
    log_audit("export_data", "user", current_user.id, "Exported full privacy data")
    
    return Response(
        json.dumps(export_data, indent=2),
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment;filename=my-privacy-data.json'}
    )

@app.route('/quick-demo')
def quick_demo():
    demo_user = User.query.filter_by(username='demo').first()
    if demo_user:
        login_user(demo_user)
        flash('Logged in as Demo User', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Demo user not found. Please check database.', 'danger')
        return redirect(url_for('index'))

# ========== AUDIT LOGGING UTILITY ==========

def log_audit(action, resource_type, resource_id=None, details="", status="success"):
    """Log user actions for compliance and security"""
    try:
        ip_address = request.remote_addr if request else None
        audit_log = AuditLog(
            user_id=current_user.id if current_user.is_authenticated else None,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            status=status
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        print(f"[AUDIT LOG ERROR] {e}")

# ========== DATA REQUEST ROUTES (GDPR Article 15 - SAR) ==========

@app.route('/data-requests')
@login_required
def data_requests():
    """View all Subject Access Requests"""
    requests = SubjectAccessRequest.query.filter_by(user_id=current_user.id).order_by(SubjectAccessRequest.request_date.desc()).all()
    log_audit("view_data_requests", "request", details="Viewed SAR list")
    return render_template('data_requests.html', requests=requests)

@app.route('/request-data', methods=['GET', 'POST'])
@login_required
def request_data():
    """File a new Subject Access Request"""
    if request.method == 'POST':
        description = request.form.get('description')
        data_format = request.form.get('format', 'json')
        
        sar = SubjectAccessRequest(
            user_id=current_user.id,
            description=description,
            data_format=data_format,
            status='completed'  # auto-complete for demo
        )
        db.session.add(sar)
        db.session.commit()
        
        log_audit("create_sar", "request", sar.id, f"Format: {data_format}")
        flash('Data request submitted successfully!', 'success')
        return redirect(url_for('data_requests'))
    
    return render_template('request_data.html')

@app.route('/download-sar/<int:request_id>')
@login_required
def download_sar(request_id):
    """Download Subject Access Request data"""
    sar = SubjectAccessRequest.query.get(request_id)
    
    if not sar or sar.user_id != current_user.id:
        flash('Request not found', 'danger')
        return redirect(url_for('data_requests'))
    
    if sar.status != 'completed':
        flash('Request not yet completed', 'warning')
        return redirect(url_for('data_requests'))
    
    # Generate data export (reuse export-data logic)
    data_sources = DataSource.query.filter_by(user_id=current_user.id).all()
    
    export_data = {
        'type': 'Subject Access Request',
        'sar_id': sar.id,
        'user': current_user.username,
        'email': current_user.email,
        'request_date': str(sar.request_date),
        'download_date': str(datetime.now()),
        'organisations': []
    }
    
    for ds in data_sources:
        org = Organisation.query.get(ds.organisation_id)
        items = DataItem.query.filter_by(data_source_id=ds.id).all()
        
        org_data = {
            'name': org.name,
            'connected_since': str(ds.connected_at),
            'data_items': [{'category': i.category, 'name': i.name, 'value': i.value, 'purpose': i.purpose} 
                          for i in items]
        }
        export_data['organisations'].append(org_data)
    
    log_audit("download_sar", "request", request_id, "Downloaded SAR data")
    
    return Response(
        json.dumps(export_data, indent=2),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename=sar-{request_id}.json'}
    )

# ========== PRIVACY PREFERENCE ROUTES ==========

@app.route('/privacy-preferences')
@login_required
def privacy_preferences():
    """Privacy Preferences for data protection rights"""
    opt_outs = CCPAOptOut.query.filter_by(user_id=current_user.id).all()
    opt_out_types = {opt.opt_out_type for opt in opt_outs}
    organisations = Organisation.query.all()
    
    log_audit("view_privacy_preferences", "privacy", details="Viewed privacy preferences")
    
    return render_template('privacy_preferences.html', 
                         opt_out_types=opt_out_types,
                         all_opt_outs=opt_outs,
                         organisations=organisations)

@app.route('/privacy-opt-out/<opt_type>', methods=['POST'])
@login_required
def privacy_opt_out(opt_type):
    """Opt out from data sharing or targeted advertising"""
    valid_types = ['sharing', 'targeted_advertising']
    
    if opt_type not in valid_types:
        return {'status': 'error', 'message': 'Invalid preference type'}, 400
    
    org_id = request.form.get('organisation_id')
    reason = request.form.get('reason', '')
    
    # Check if already opted out
    existing = CCPAOptOut.query.filter_by(
        user_id=current_user.id,
        organisation_id=org_id,
        opt_out_type=opt_type
    ).first()
    
    if not existing:
        opt_out = CCPAOptOut(
            user_id=current_user.id,
            organisation_id=org_id,
            opt_out_type=opt_type,
            reason=reason
        )
        db.session.add(opt_out)
        db.session.commit()
        
        log_audit("privacy_opt_out", "privacy", org_id, f"Type: {opt_type}")
        flash(f'Successfully opted out from {opt_type}', 'success')
    else:
        flash('Already opted out from this', 'info')
    
    return redirect(url_for('privacy_preferences'))

@app.route('/privacy-opt-in/<int:opt_out_id>', methods=['POST'])
@login_required
def privacy_opt_in(opt_out_id):
    """Revoke privacy opt-out and opt back in"""
    opt_out = CCPAOptOut.query.get(opt_out_id)
    
    if opt_out and opt_out.user_id == current_user.id:
        log_audit("privacy_opt_in", "privacy", opt_out.organisation_id, f"Type: {opt_out.opt_out_type}")
        db.session.delete(opt_out)
        db.session.commit()
        flash('You have opted back in', 'success')
    else:
        flash('Preference not found', 'danger')
    
    return redirect(url_for('privacy_preferences'))

# ========== AUDIT LOG ROUTES ==========

@app.route('/audit-logs')
@login_required
def audit_logs():
    """View audit logs of all user actions"""
    logs = AuditLog.query.filter_by(user_id=current_user.id).order_by(AuditLog.timestamp.desc()).limit(100).all()
    
    log_audit("view_audit_logs", "audit", details="Viewed audit logs")
    
    return render_template('audit_logs.html', logs=logs)

# ========== LEGAL PAGES ==========

@app.route('/privacy-policy')
def privacy_policy():
    """Privacy Policy page"""
    return render_template('privacy_policy.html')

@app.route('/terms-of-service')
def terms_of_service():
    """Terms of Service page"""
    return render_template('terms_of_service.html')

@app.route('/data-processing')
def data_processing():
    """Data Processing Information page"""
    return render_template('data_processing.html')

# ========== DATABASE INITIALIZATION (NOW AT THE BOTTOM - AFTER ALL FUNCTIONS) ==========

with app.app_context():
    db.create_all()
    
    # Only add sample data if database is empty
    if Organisation.query.count() == 0:
        create_sample_organisations()
        create_sample_data_for_demo_user()

# ========== RUN THE APP ==========

if __name__ == '__main__':
    app.run(debug=True)
