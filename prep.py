#!/usr/bin/env python3
"""
Deployment Preparation Script
Prepares the application for production deployment
"""

import os
import sys
import secrets

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_hex(32)

def create_production_config():
    """Create production configuration template"""
    config_content = '''"""
Production Configuration
Copy this to .env file for production
"""

# Flask Configuration
SECRET_KEY="{secret_key}"
FLASK_ENV=production
FLASK_DEBUG=0

# Database Configuration
DATABASE_URL=sqlite:///mafadza_repairs_prod.db
# For PostgreSQL (Render, Railway, etc.):
# DATABASE_URL=postgresql://username:password@host:port/database

# Admin Configuration (CHANGE THESE!)
ADMIN_USERNAME=your_production_admin
ADMIN_PASSWORD=your_secure_password_here
ADMIN_EMAIL=admin@yourdomain.com

# Application Settings
CREATE_DEFAULT_ADMIN=False  # Set to False in production
SESSION_COOKIE_SECURE=True
REMEMBER_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
REMEMBER_COOKIE_HTTPONLY=True

# For email notifications (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=repairs@yourdomain.com
'''.format(secret_key=generate_secret_key())
    
    return config_content

def create_requirements_prod():
    """Create production requirements file"""
    requirements = '''# Production Requirements
# Core Dependencies
Flask==3.0.0
Werkzeug==3.0.1
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
python-dotenv==1.0.0

# Production Server (choose one)
gunicorn==21.2.0  # For Render, Heroku, etc.
# waitress==2.1.2  # For Windows servers

# Database (if using PostgreSQL)
# psycopg2-binary==2.9.9

# Email (optional)
# Flask-Mail==0.9.1

# Security
# bcrypt==4.0.1  # For stronger password hashing
'''
    
    return requirements

def create_render_yaml():
    """Create Render.com deployment configuration"""
    render_yaml = '''services:
  - type: web
    name: mafadzatechsolutions
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
      - key: FLASK_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: mafadza_db
          property: connectionString
'''
    
    return render_yaml

def create_procfile():
    """Create Procfile for platform-as-a-service"""
    procfile = '''web: gunicorn run:app
worker: python worker.py  # If you add background tasks later
'''
    
    return procfile

def create_dockerfile():
    """Create Dockerfile for container deployment"""
    dockerfile = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
'''
    
    return dockerfile

def create_gitignore():
    """Create comprehensive .gitignore"""
    gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Database
*.db
*.sqlite3
*.db-journal

# Environment Variables
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp

# Backup files
*.bak
*.backup

# Production files
instance/
'''
    
    return gitignore

def main():
    print("=" * 60)
    print("DEPLOYMENT PREPARATION")
    print("=" * 60)
    
    # Create deployment directory
    deploy_dir = "deployment"
    if not os.path.exists(deploy_dir):
        os.makedirs(deploy_dir)
        print(f"✓ Created {deploy_dir}/ directory")
    
    # Generate files
    files_to_create = {
        ".env.example": create_production_config(),
        "requirements-prod.txt": create_requirements_prod(),
        "render.yaml": create_render_yaml(),
        "Procfile": create_procfile(),
        "Dockerfile": create_dockerfile(),
        ".gitignore": create_gitignore(),
    }
    
    for filename, content in files_to_create.items():
        filepath = os.path.join(deploy_dir, filename) if filename != ".gitignore" else filename
        
        if os.path.exists(filepath):
            overwrite = input(f"{filename} already exists. Overwrite? (yes/no): ").strip().lower()
            if overwrite != 'yes':
                continue
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Created {filename}")
    
    # Update config.py for production
    print("\n" + "=" * 60)
    print("UPDATING CONFIG.PY FOR PRODUCTION")
    print("=" * 60)
    
    config_path = "config.py"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        # Add production settings
        if "class ProductionConfig" not in config_content:
            prod_config = '''

class ProductionConfig(Config):
    """Production configuration"""
    # Use environment variables in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Security settings for production
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Don't create default admin in production
    CREATE_DEFAULT_ADMIN = False
    
    # Use environment variables for admin credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@mafadzatechsolutions.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '')
'''
            
            # Add after Config class
            lines = config_content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('class Config:'):
                    # Find where Config class ends
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip() and not lines[j].startswith(' ') and not lines[j].startswith('\t'):
                            lines.insert(j, prod_config)
                            break
                    break
            
            new_config = '\n'.join(lines)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(new_config)
            
            print("✓ Updated config.py with ProductionConfig class")
    
    print("\n" + "=" * 60)
    print("DEPLOYMENT CHECKLIST")
    print("=" * 60)
    print("✅ 1. Update admin credentials using update_admin.py")
    print("✅ 2. Review deployment files in deployment/ directory")
    print("✅ 3. Set up environment variables in production")
    print("✅ 4. Choose deployment platform:")
    print("   - Render.com: Use render.yaml")
    print("   - PythonAnywhere: Upload as Python/Flask app")
    print("   - Railway.app: Use Procfile")
    print("   - Docker: Use Dockerfile")
    print("✅ 5. Set up production database")
    print("✅ 6. Configure domain and SSL certificate")
    print("✅ 7. Test thoroughly before going live")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: python update_admin.py")
    print("2. Review files in deployment/")
    print("3. Follow platform-specific deployment guide")
    print("=" * 60)

if __name__ == "__main__":
    main()