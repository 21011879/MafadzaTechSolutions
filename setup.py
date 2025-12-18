#!/usr/bin/env python3
"""
Setup script for MafadzaTechSolutions Repair System
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print setup header"""
    print("=" * 60)
    print("MafadzaTechSolutions Repair System - Setup")
    print("=" * 60)

def check_python_version():
    """Check Python version"""
    print("1. Checking Python version...")
    if sys.version_info < (3, 7):
        print(f"ERROR: Python 3.7 or higher required. You have {sys.version}")
        sys.exit(1)
    print(f"✓ Python {sys.version} detected")

def create_virtual_env():
    """Create virtual environment"""
    print("\n2. Creating virtual environment...")
    
    if not os.path.exists("venv"):
        try:
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            print("✓ Virtual environment created")
        except subprocess.CalledProcessError:
            print("✗ Failed to create virtual environment")
            sys.exit(1)
    else:
        print("✓ Virtual environment already exists")

def activate_virtual_env():
    """Activate virtual environment"""
    print("\n3. Activating virtual environment...")
    
    # This is just for information - activation happens when you run the script
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
    else:  # Linux/Mac
        activate_script = "venv/bin/activate"
    
    print(f"To activate manually, run:")
    print(f"  Windows: venv\\Scripts\\activate")
    print(f"  Linux/Mac: source venv/bin/activate")

def install_requirements():
    """Install required packages"""
    print("\n4. Installing requirements...")
    
    # Determine pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Linux/Mac
        pip_path = "venv/bin/pip"
    
    try:
        # Upgrade pip first
        subprocess.check_call([pip_path, "install", "--upgrade", "pip"])
        
        # Install requirements
        if os.path.exists("requirements.txt"):
            subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
            print("✓ Requirements installed")
        else:
            print("✗ requirements.txt not found")
            create_requirements_file()
            subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
            print("✓ Requirements installed from generated file")
    except subprocess.CalledProcessError:
        print("✗ Failed to install requirements")
        sys.exit(1)

def create_requirements_file():
    """Create requirements.txt if it doesn't exist"""
    requirements = """Flask==3.0.0
Werkzeug==3.0.1
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
python-dotenv==1.0.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    print("✓ Created requirements.txt")

def initialize_database():
    """Initialize the database"""
    print("\n5. Initializing database...")
    
    # Run a Python script to initialize the database
    init_script = """
from app import create_app, db
from config import Config

app = create_app(Config)
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
    
    # Create admin user
    from app.models import Admin
    from werkzeug.security import generate_password_hash
    
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(
            username='admin',
            email='admin@mafadzatechsolutions.com',
            password_hash=generate_password_hash('Admin123!')
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created:")
        print("  Username: admin")
        print("  Password: Admin123!")
    else:
        print("Admin user already exists")
"""
    
    # Determine Python path based on OS
    if os.name == 'nt':  # Windows
        python_path = "venv\\Scripts\\python"
    else:  # Linux/Mac
        python_path = "venv/bin/python"
    
    try:
        # Write temporary script
        with open("temp_init.py", "w") as f:
            f.write(init_script)
        
        # Run the script
        subprocess.check_call([python_path, "temp_init.py"])
        
        # Clean up
        if os.path.exists("temp_init.py"):
            os.remove("temp_init.py")
            
        print("✓ Database initialized")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to initialize database: {e}")
        if os.path.exists("temp_init.py"):
            os.remove("temp_init.py")

def create_sample_data():
    """Create sample data for testing"""
    print("\n6. Creating sample data...")
    
    sample_script = """
from app import create_app, db
from config import Config
from app.models import Customer, Repair, Payment
from datetime import datetime, timedelta

app = create_app(Config)
with app.app_context():
    # Check if we already have data
    if Repair.query.count() > 0:
        print("Sample data already exists")
        exit(0)
    
    # Create sample customers
    customers = [
        Customer(
            name="John Smith",
            phone="+263771234567",
            email="john@example.com",
            address="123 Main St, Harare"
        ),
        Customer(
            name="Sarah Johnson",
            phone="+263772345678",
            email="sarah@example.com",
            address="456 Park Ave, Bulawayo"
        ),
        Customer(
            name="Robert Mugabe",
            phone="+263773456789",
            email="robert@example.com"
        )
    ]
    
    for customer in customers:
        db.session.add(customer)
    
    db.session.commit()
    
    # Create sample repairs
    repairs = [
        Repair(
            tracking_id="MFZ202412250001",
            customer_id=1,
            device_type="Laptop",
            brand="Dell",
            model="XPS 15",
            problem_description="Screen cracked after accidental drop",
            status="Repairing",
            estimated_cost=250.00,
            deposit_paid=50.00,
            created_at=datetime.utcnow() - timedelta(days=2)
        ),
        Repair(
            tracking_id="MFZ202412240002",
            customer_id=2,
            device_type="Phone",
            brand="Apple",
            model="iPhone 14 Pro",
            problem_description="Battery drains quickly, needs replacement",
            status="Waiting for Parts",
            estimated_cost=120.00,
            deposit_paid=30.00,
            created_at=datetime.utcnow() - timedelta(days=3)
        ),
        Repair(
            tracking_id="MFZ202412230003",
            customer_id=3,
            device_type="Phone",
            brand="Samsung",
            model="Galaxy S23",
            problem_description="Water damage, phone won't turn on",
            status="Diagnosing",
            estimated_cost=200.00,
            created_at=datetime.utcnow() - timedelta(days=5)
        ),
        Repair(
            tracking_id="MFZ202412200004",
            customer_id=1,
            device_type="Laptop",
            brand="HP",
            model="Pavilion",
            problem_description="Keyboard not working properly",
            status="Completed",
            actual_cost=80.00,
            is_paid=True,
            completed_at=datetime.utcnow() - timedelta(days=1),
            created_at=datetime.utcnow() - timedelta(days=7)
        )
    ]
    
    for repair in repairs:
        db.session.add(repair)
    
    db.session.commit()
    
    # Create sample payments
    payments = [
        Payment(
            repair_id=1,
            amount=50.00,
            payment_method="Ecocash",
            reference="ECO123456",
            notes="Initial deposit"
        ),
        Payment(
            repair_id=2,
            amount=30.00,
            payment_method="Cash",
            notes="Deposit paid at counter"
        ),
        Payment(
            repair_id=4,
            amount=80.00,
            payment_method="Bank Transfer",
            reference="TRF789012",
            notes="Final payment"
        )
    ]
    
    for payment in payments:
        db.session.add(payment)
    
    db.session.commit()
    print("✓ Sample data created successfully!")
    print("  - 3 customers")
    print("  - 4 repair orders")
    print("  - 3 payments")
"""
    
    # Determine Python path based on OS
    if os.name == 'nt':  # Windows
        python_path = "venv\\Scripts\\python"
    else:  # Linux/Mac
        python_path = "venv/bin/python"
    
    try:
        # Write temporary script
        with open("temp_sample.py", "w") as f:
            f.write(sample_script)
        
        # Run the script
        subprocess.check_call([python_path, "temp_sample.py"])
        
        # Clean up
        if os.path.exists("temp_sample.py"):
            os.remove("temp_sample.py")
    except subprocess.CalledProcessError:
        print("✗ Failed to create sample data (non-critical)")

def print_final_instructions():
    """Print final setup instructions"""
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    
    print("\nTO RUN THE APPLICATION:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Linux/Mac
        print("   source venv/bin/activate")
    
    print("2. Run the application:")
    print("   python run.py")
    
    print("\nACCESS THE APPLICATION:")
    print("  Website:      http://127.0.0.1:5000")
    print("  Admin Login:  http://127.0.0.1:5000/admin/login")
    print("  Username:     admin")
    print("  Password:     Admin123!")
    
    print("\n⚠️  IMPORTANT:")
    print("  • Change the admin password after first login!")
    print("  • Sample data has been created for testing")
    print("=" * 60)

def main():
    """Main setup function"""
    print_header()
    check_python_version()
    create_virtual_env()
    activate_virtual_env()
    install_requirements()
    initialize_database()
    create_sample_data()
    print_final_instructions()

if __name__ == "__main__":
    main()