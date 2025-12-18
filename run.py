#!/usr/bin/env python3
"""
MafadzaTechSolutions - Repair Booking & Tracking System
Main entry point for the application
"""

from app import create_app
from datetime import datetime

# Create Flask application
app = create_app()


if __name__ == '__main__':
    # Run the application
    print("=" * 60)
    print("MafadzaTechSolutions Repair System")
    print("=" * 60)
    print(f"Admin Login: http://127.0.0.1:5000/admin/login")
   # print(f"Username: {app.config['ADMIN_USERNAME']}")
   # print(f"Password: {app.config['ADMIN_PASSWORD']}")
    print("=" * 60)
  #   print("NOTE: Change the admin password after first login!")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)