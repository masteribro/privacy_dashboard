# Privacy-First Personal Data Dashboard

A user-centric Personal Data Dashboard that gives individuals full visibility and control over their personal data. Built with Flask, SQLite, and Bootstrap 5.

## Features

- Privacy Health Score with real-time calculation
- My Data — view what organisations hold about you
- Consent Management — grant and withdraw purpose-level consents
- Subject Access Requests (GDPR Article 15)
- CCPA Privacy Preferences and opt-out controls
- Audit Logs — full activity trail
- Data Flow Visualisation
- JSON data export
- CSRF protection, bcrypt password hashing, and security headers

---

## Requirements

- Python 3.10 or higher
- pip
- Git

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/masteribro/privacy_dashboard.git
cd privacy_dashboard
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

> On Windows use: `venv\Scripts\activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables (optional)

No `.env` file is required to run the app locally — all defaults are pre-configured.

If you want to override any settings, create a `.env` file in the project root:

```
SECRET_KEY=your-strong-secret-key-here
FLASK_PORT=5001
```

> `SECRET_KEY` defaults to a built-in dev key. Always set a strong custom key in production.  
> `FLASK_PORT` defaults to `5001`.

### 5. Run the app

```bash
python app.py
```

You should see:

```
==================================================
Privacy Dashboard Running!
URL: http://localhost:5001
==================================================
```

### 6. Open in your browser

```
http://localhost:5001
```

---

## Demo Account

A demo account is created automatically on first run:

| Field    | Value     |
|----------|-----------|
| Username | `demo`    |
| Password | `demo123` |

Or click the **Try Demo** button on the homepage.

---

## Project Structure

```
privacy_dashboard/
├── app.py               # Main Flask application and routes
├── database.py          # SQLAlchemy database models
├── requirements.txt     # Python dependencies
├── migrate_db.py        # Database migration utility
├── reset_db.py          # Reset database to fresh state
├── static/
│   └── style.css        # Custom styles
└── templates/           # Jinja2 HTML templates
    ├── base.html
    ├── dashboard.html
    ├── mydata.html
    ├── consents.html
    ├── audit_logs.html
    └── ...
```

---

## Stopping the App

Press `Ctrl + C` in the terminal.

To deactivate the virtual environment:

```bash
deactivate
```

---

## Resetting the Database

If you need a fresh database with demo data:

```bash
python reset_db.py
```

---

## Tech Stack

| Component      | Technology                        |
|----------------|-----------------------------------|
| Backend        | Python, Flask 2.3.3               |
| Database       | SQLite via Flask-SQLAlchemy 3.0.5 |
| Authentication | Flask-Login 0.6.2                 |
| Password Hashing | bcrypt (12 rounds)              |
| CSRF Protection | Flask-WTF 1.3.0                  |
| Frontend       | Bootstrap 5.3, Font Awesome 6.0   |
| Templating     | Jinja2                            |
