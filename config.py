import os
from datetime import datetime

# Base directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mafadza-dev-key-2024-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'mafadza_repairs.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
 # Admin credentials (CHANGE THESE IN PRODUCTION!)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@mafadzatechsolutions.com')
    ADMIN_PASSWORD = os.environ.get('DIGIMARK', 'Khalifonia@21')  # CHANGE THIS!

   # Create default admin? Set to False in production
    CREATE_DEFAULT_ADMIN = os.environ.get('CREATE_DEFAULT_ADMIN', 'True') == 'True' 
    
    # Application settings
    SITE_NAME = 'MafadzaTechSolutions'
    SITE_TAGLINE = 'Professional Device Repair Services'
    
    # Repair settings
    STATUS_OPTIONS = [
        'Received',
        'Diagnosing',
        'Waiting for Parts',
        'Repairing',
        'Testing',
        'Completed',
        'Ready for Pickup'
    ]
    
    # Device types
    DEVICE_TYPES = ['Laptop', 'Phone', 'Tablet', 'Desktop', 'Other']
    
    # Brands
    PHONE_BRANDS = ['Apple', 'Samsung', 'Google', 'Huawei', 'Xiaomi', 'Other']
    LAPTOP_BRANDS = ['Dell', 'HP', 'Lenovo', 'Apple', 'Asus', 'Acer', 'Other']
    
    # Business info
    BUSINESS_INFO = {
        'name': 'MafadzaTechSolutions',
        'phone': '+27715991599',
        'email': 'mafadza2000@gmail.com',
        'address': 'Maniini ,Thohoyandou , South Africa',
        'working_hours': 'Mon-Fri: 8AM-6PM, Sat: 8AM-6PM'
    }