#!/usr/bin/env python3
"""
Automated test for MafadzaTechSolutions
"""

import os
import sys
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_home_page():
    """Test home page accessibility"""
    print("Testing home page...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✓ Home page accessible")
            return True
        else:
            print(f"✗ Home page returned {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Home page error: {e}")
        return False

def test_booking_page():
    """Test booking page"""
    print("\nTesting booking page...")
    try:
        response = requests.get(f"{BASE_URL}/book-repair")
        if response.status_code == 200:
            print("✓ Booking page accessible")
            return True
        else:
            print(f"✗ Booking page returned {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Booking page error: {e}")
        return False

def test_tracking_page():
    """Test tracking page"""
    print("\nTesting tracking page...")
    try:
        response = requests.get(f"{BASE_URL}/track-repair")
        if response.status_code == 200:
            print("✓ Tracking page accessible")
            return True
        else:
            print(f"✗ Tracking page returned {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Tracking page error: {e}")
        return False

def test_admin_login_page():
    """Test admin login page"""
    print("\nTesting admin login page...")
    try:
        response = requests.get(f"{BASE_URL}/admin/login")
        if response.status_code == 200:
            print("✓ Admin login page accessible")
            return True
        else:
            print(f"✗ Admin login page returned {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Admin login page error: {e}")
        return False

def check_templates():
    """Check if all templates exist"""
    print("\nChecking template files...")
    templates = [
        'app/templates/base.html',
        'app/templates/index.html',
        'app/templates/book_repair.html',
        'app/templates/booking_success.html',
        'app/templates/track_repair.html',
        'app/templates/admin/login.html',
        'app/templates/admin/dashboard.html',
        'app/templates/admin/repairs.html',
        'app/templates/admin/repair_detail.html',
        'app/templates/admin/reports.html'
    ]
    
    all_exist = True
    for template in templates:
        if os.path.exists(template):
            print(f"✓ {os.path.basename(template)}")
        else:
            print(f"✗ {os.path.basename(template)} - MISSING")
            all_exist = False
    
    return all_exist

def check_database():
    """Check if database exists and has data"""
    print("\nChecking database...")
    db_file = 'mafadza_repairs.db'
    if os.path.exists(db_file):
        print(f"✓ Database file exists ({os.path.getsize(db_file)} bytes)")
        
        # Check if we can import models
        try:
            sys.path.insert(0, '.')
            from app import create_app, db
            from config import Config
            
            app = create_app(Config)
            with app.app_context():
                from app.models import Repair
                count = Repair.query.count()
                print(f"✓ Database has {count} repair records")
                return True
        except Exception as e:
            print(f"✗ Database error: {e}")
            return False
    else:
        print("✗ Database file not found")
        return False

def main():
    print("=" * 60)
    print("MAFADZATECHSOLUTIONS - COMPREHENSIVE TEST")
    print("=" * 60)
    
    # Make sure app is running
    print("NOTE: Make sure the application is running (python run.py)")
    print(f"      Testing against: {BASE_URL}")
    print("-" * 60)
    
    results = []
    
    # Run tests
    results.append(test_home_page())
    results.append(test_booking_page())
    results.append(test_tracking_page())
    results.append(test_admin_login_page())
    results.append(check_templates())
    results.append(check_database())
    
    print("\n" + "=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("\nApplication is ready for use!")
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        print("\nSome tests failed. Please check the issues above.")
    
    print("\nMANUAL TESTS TO PERFORM:")
    print("1. Test booking a new repair")
    print("2. Test tracking with sample tracking IDs")
    print("3. Test admin login and dashboard")
    print("4. Test repair management")
    print("5. Test reports generation")
    print("=" * 60)

if __name__ == "__main__":
    main()