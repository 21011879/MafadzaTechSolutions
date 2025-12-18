from app import create_app, db
from config import Config
from app.models import Admin
from werkzeug.security import generate_password_hash

app = create_app(Config)

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created!")
    
    # Create admin user if it doesn't exist
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(
            username='admin',
            email='admin@mafadzatechsolutions.com',
            password_hash=generate_password_hash('Admin123!')
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created:")
        print("  Username: admin")
        print("  Password: Admin123!")
    else:
        print("Admin user already exists")
    
    print("\nSetup complete! Run 'python run.py' to start the application.")