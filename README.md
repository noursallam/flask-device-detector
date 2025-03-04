# Flask Device-Specific Authentication System

## Overview

This is a Flask-based web application that implements a unique device-specific authentication system. The application allows user registration and login while ensuring that users can only log in from the device they originally registered with.

## Features

- User registration with device-specific UUID
- Login authentication with device validation
- SQLite database for user storage
- Device identification using:
  - MAC address
  - IP address
  - System information
  - Unique SHA-256 hash generation

## Prerequisites

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install required dependencies:
```bash
pip install flask flask-sqlalchemy flask-migrate
```

## Database Setup

Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Running the Application

```bash
python app.py
```

The application will be available at `http://192.168.1.5:8000`

## Endpoints

- `/`: Displays the current device's UUID
- `/register`: User registration page
- `/login`: User login page

## Security Notes

- Passwords are currently stored in plain text (not recommended for production)
- Device validation is based on a combination of system and network attributes
- Consider implementing additional security measures for production use

## Customization

- Change database URI in `app.config['SQLALCHEMY_DATABASE_URI']`
- Modify host and port in `app.run()` method
- Enhance device identification logic in `get_device_uuid()` function

## Potential Improvements

- Implement password hashing
- Add password complexity requirements
- Implement more robust device fingerprinting
- Add error handling and validation
- Create logout functionality

