#!/usr/bin/env python3
"""
Update Admin Credentials Script
Run this to change the admin username and password
"""

import sys
import getpass
from werkzeug.security import generate_password_hash

# Add current directory to path
sys.path.insert(0, '.')

def update_admin_credentials():
    print("=" * 60)
    print("ADMIN CREDENTIALS UPDATE TOOL")
    print("=" * 60)
    
    # Get new credentials
    print("\nEnter new admin credentials:")
    print("-" * 40)
    
    new_username = input("New Username: ").strip()
    
    while True:
        new_password = getpass.getpass("New Password: ").strip()
        confirm_password = getpass.getpass("Confirm Password: ").strip()
        
        if new_password != confirm_password:
            print("❌ Passwords do not match. Please try again.\n")
        elif len(new_password) < 8:
            print("❌ Password must be at least 8 characters long.\n")
        else:
            break
    
    new_email = input("New Email (optional, press Enter to keep current): ").strip()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"New Username: {new_username}")
    print(f"New Email: {new_email if new_email else '(Keep current)'}")
    print("Password: ******** (Hidden for security)")
    print("-" * 40)
    
    confirm = input("\nAre you sure you want to update admin credentials? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Update cancelled.")
        return
    
    try:
        from app import create_app, db
        from config import Config
        from app.models import Admin
        
        app = create_app(Config)
        
        with app.app_context():
            # Get the current admin (assuming first admin user)
            admin = Admin.query.filter_by(username='admin').first()
            
            if not admin:
                print("❌ No admin user found with username 'admin'.")
                # Try to create new admin
                create_new = input("Create new admin user? (yes/no): ").strip().lower()
                if create_new == 'yes':
                    admin = Admin(
                        username=new_username,
                        email=new_email or 'admin@mafadzatechsolutions.com',
                        password_hash=generate_password_hash(new_password)
                    )
                    db.session.add(admin)
                    db.session.commit()
                    print("✅ New admin user created successfully!")
                else:
                    print("❌ No changes made.")
                    return
            
            else:
                # Update existing admin
                old_username = admin.username
                admin.username = new_username
                admin.password_hash = generate_password_hash(new_password)
                if new_email:
                    admin.email = new_email
                
                db.session.commit()
                print(f"✅ Admin credentials updated successfully!")
                print(f"   Old username: {old_username}")
                print(f"   New username: {new_username}")
            
            print("\n" + "=" * 60)
            print("IMPORTANT INSTRUCTIONS")
            print("=" * 60)
            print("1. The old password will no longer work")
            print("2. Update the following in config.py if needed:")
            print(f"   ADMIN_USERNAME = '{new_username}'")
            print(f"   ADMIN_EMAIL = '{new_email or admin.email}'")
            print("3. Keep the new password secure")
            print("4. Restart the application if it's running")
            print("=" * 60)
            
    except Exception as e:
        print(f"❌ Error updating admin credentials: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_admin_credentials()