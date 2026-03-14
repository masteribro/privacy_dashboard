# Chapter 3: Methodology / System Design

## 3.1 Introduction
This chapter describes the methodology used to design and develop the Privacy Dashboard system. It covers the system architecture, database design, user interface design, and the technologies selected for implementation.

## 3.2 System Development Methodology

### 3.2.1 Development Approach
**Agile/Iterative Development:**
The Privacy Dashboard was developed using an iterative approach with the following phases:

1. **Requirements Gathering** - Understanding user needs for privacy control
2. **Design** - Creating system architecture and database schemas
3. **Implementation** - Building features incrementally
4. **Testing** - Validating functionality with demo users
5. **Refinement** - Improving based on feedback

### 3.2.2 Design Philosophy: Privacy by Design
The system adheres to Privacy by Design principles:
- Users have complete visibility into data collection
- Consent is explicit and granular
- Users can withdraw consent at any time
- Audit trails track all access
- Default settings prioritize privacy protection

## 3.3 System Architecture

### 3.3.1 High-Level Architecture
```
┌─────────────────────────────────────────────────────┐
│                   Presentation Layer                 │
│        (Web UI - Flask Templates, Bootstrap)         │
├─────────────────────────────────────────────────────┤
│                  Application Layer                   │
│        (Flask Application & Business Logic)          │
├─────────────────────────────────────────────────────┤
│                  Data Access Layer                   │
│      (SQLAlchemy ORM & Database Models)             │
├─────────────────────────────────────────────────────┤
│                   Data Layer                         │
│           (SQLite Database - privacy.db)             │
└─────────────────────────────────────────────────────┘
```

### 3.3.2 Component Description

**Presentation Layer:**
- Bootstrap 5 responsive templates
- User-friendly dashboard interface
- Real-time feedback and validation
- Accessible design (WCAG compliance)

**Application Layer:**
- Flask web framework handles HTTP requests
- Business logic for privacy score calculation
- Consent management logic
- Audit logging functionality

**Data Access Layer:**
- SQLAlchemy ORM for database abstraction
- Data validation and sanitization
- Query optimization

**Data Layer:**
- SQLite relational database
- Persistent storage of user data

## 3.4 Database Design

### 3.4.1 Entity-Relationship Diagram
```
User (1) ──────────── (M) DataSource
  │
  ├─── (M) Consent
  ├─── (M) AuditLog
  ├─── (M) SubjectAccessRequest
  ├─── (M) CCPAOptOut
  └─── (1) UserPreference

Organisation (1) ──────────── (M) DataSource
Organisation (1) ──────────── (M) Consent

DataSource (1) ──────────── (M) DataItem
```

### 3.4.2 Database Schema

**Users Table:**
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Organisations Table:**
```sql
CREATE TABLE organisation (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    logo VARCHAR(5) -- emoji
);
```

**Data Sources Table:**
```sql
CREATE TABLE data_source (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    organisation_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    connected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (organisation_id) REFERENCES organisation(id)
);
```

**Data Items Table:**
```sql
CREATE TABLE data_item (
    id INTEGER PRIMARY KEY,
    data_source_id INTEGER NOT NULL,
    category VARCHAR(50),
    name VARCHAR(100),
    value VARCHAR(500),
    purpose VARCHAR(200),
    FOREIGN KEY (data_source_id) REFERENCES data_source(id)
);
```

**Consents Table:**
```sql
CREATE TABLE consent (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    organisation_id INTEGER NOT NULL,
    purpose VARCHAR(100),
    consent_type VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active',
    granted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    withdrawn_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (organisation_id) REFERENCES organisation(id)
);
```

**Audit Logs Table:**
```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(100),
    resource_type VARCHAR(50),
    resource_id INTEGER,
    details VARCHAR(500),
    ip_address VARCHAR(50),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'success'
);
```

**Subject Access Requests Table:**
```sql
CREATE TABLE subject_access_request (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    data_format VARCHAR(20) DEFAULT 'json',
    completed_at DATETIME,
    rejection_reason VARCHAR(500),
    description VARCHAR(500),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

**Privacy Preferences Table:**
```sql
CREATE TABLE user_preference (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    language VARCHAR(10) DEFAULT 'en',
    theme VARCHAR(20) DEFAULT 'light',
    newsletter BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### 3.4.3 Data Relationships
- **User-DataSource:** One user can have data from multiple organizations
- **Organisation-DataSource:** One organization can be connected by multiple users
- **DataSource-DataItem:** One data source contains multiple data items
- **User-Consent:** One user can grant consents to multiple organizations
- **User-AuditLog:** All user actions are tracked
- **User-SubjectAccessRequest:** Users can request multiple data extracts

## 3.5 System Features and Workflows

### 3.5.1 Authentication and User Management
**Registration Workflow:**
1. User enters username, email, password
2. System validates input (email format, password strength)
3. Password is hashed using bcrypt
4. User account is created
5. User is redirected to login

**Login Workflow:**
1. User enters credentials
2. System verifies against database
3. Session cookie is created (HTTP-only, secure)
4. User is redirected to dashboard

### 3.5.2 Consent Management Workflow
**Granting Consent:**
1. User navigates to Manage Consents page
2. System displays organizations with collected data
3. User reviews consent purposes
4. User grants/withholds consent
5. Action is logged in audit trail
6. Privacy score is recalculated

**Withdrawing Consent:**
1. User selects active consent
2. User confirms withdrawal
3. Consent status is updated to 'withdrawn'
4. Timestamp recorded
5. Audit log entry created
6. Privacy score updated

### 3.5.3 Data Request Workflow (GDPR Article 15 - Subject Access Request)
1. User navigates to Data Requests page
2. User submits data request
3. System aggregates all personal data
4. Data is formatted (JSON/CSV)
5. User can download exported data
6. Request is logged for compliance

### 3.5.4 Privacy Preference Management
**User Can Configure:**
- Language preference (English, Spanish, French, German)
- Theme (Light/Dark mode)
- Newsletter preferences
- CCPA/Privacy opt-out preferences

## 3.6 User Interface Design

### 3.6.1 Dashboard Components
**Navigation Bar:**
- Dashboard link
- My Data link
- Manage Consents link
- More menu (Data Requests, Audit Logs, Privacy Preferences)
- Logout button

**Dashboard Main Panel:**
- Privacy Health Score (0-100%)
- Quick statistics (organizations, data items, consents)
- Privacy recommendations
- Quick action buttons

**My Data Page:**
- Organization cards with collected data
- Data categorization (Personal, Financial, Location)
- Sensitivity indicators (color-coded)
- Manage consents button for each organization

**Consents Page:**
- List of organizations with consent status
- Consent grant/withdraw buttons
- Purposes of data collection
- Active/withdrawn status indicators

**Data Flow Visualization:**
- SVG diagram showing data ecosystem
- User at center
- Organizations connected to user
- Data flow arrows
- Privacy recommendations

### 3.6.2 Color Scheme and Accessibility
**Color Palette:**
- Primary: Blue (#0d6efd) - Trust and security
- Success: Green (#198754) - Positive actions
- Warning: Yellow (#ffc107) - Sensitive data
- Danger: Red (#dc3545) - High-risk data
- Dark backgrounds for Dark mode

**Accessibility Features:**
- High contrast ratios (WCAG AA compliant)
- Semantic HTML structure
- ARIA labels for screen readers
- Keyboard navigation support
- Responsive design for mobile

## 3.7 Security Considerations

### 3.7.1 Authentication Security
- Passwords hashed with bcrypt (not stored in plain text)
- Session cookies are HTTP-only (prevent XSS theft)
- Session cookies use SameSite=Lax (prevent CSRF)
- Login rate limiting (prevent brute force attacks)

### 3.7.2 Data Protection
- All database queries use parameterized statements (prevent SQL injection)
- User input sanitization and validation
- CSRF tokens for state-changing operations
- Secure headers (Content-Security-Policy, X-Frame-Options)

### 3.7.3 Audit Trail
- All user actions logged with timestamp and IP address
- Immutable audit logs (cannot be modified after creation)
- Searchable logs for compliance investigations
- 7-year retention policy

## 3.8 Technology Stack

### 3.8.1 Backend
- **Framework:** Flask (Python web framework)
- **ORM:** SQLAlchemy (database abstraction)
- **Authentication:** Flask-Login (session management)
- **Password Hashing:** bcrypt (cryptographic hashing)
- **Database:** SQLite (file-based relational database)

### 3.8.2 Frontend
- **HTML5:** Semantic markup
- **CSS3:** Bootstrap 5 framework
- **JavaScript:** Vanilla JS (no heavy dependencies)
- **Icons:** Font Awesome

### 3.8.3 Deployment
- **Server:** Flask development server (can be deployed to Gunicorn)
- **Platform:** macOS/Linux/Windows compatible
- **Port:** Configurable (default 5001)

## 3.9 System Requirements

### 3.9.1 Hardware Requirements
- **Processor:** Any modern CPU
- **RAM:** 512 MB minimum
- **Storage:** 100 MB for database
- **Network:** Internet connection for development

### 3.9.2 Software Requirements
- **OS:** macOS, Linux, or Windows
- **Python:** 3.8 or higher
- **Database:** SQLite3 (included with Python)
- **Browser:** Modern browser (Chrome, Firefox, Safari, Edge)

## 3.10 Summary
This chapter outlined:

1. **Development Approach** - Iterative, Privacy-by-Design methodology
2. **System Architecture** - 4-layer architecture (Presentation, Application, Data Access, Data)
3. **Database Design** - Normalized schema with 8 tables managing users, organizations, data, and compliance
4. **User Workflows** - Authentication, consent management, data requests, preferences
5. **UI Design** - Bootstrap-based responsive design with accessibility features
6. **Security** - Password hashing, SQL injection prevention, audit logging
7. **Technology Stack** - Flask, SQLAlchemy, SQLite, Bootstrap 5

The modular design allows for future expansion with real API integrations, mobile apps, and additional features.
