import random
from datetime import datetime
from flask import current_app

def generate_tracking_id():
    """
    Generate unique tracking ID in format: MFZYYYYMMDDXXXX
    Example: MFZ202412250015
    """
    today = datetime.now()
    base_id = f"MFZ{today.strftime('%Y%m%d')}"
    
    # Generate random 4-digit number
    random_suffix = str(random.randint(0, 9999)).zfill(4)
    
    return f"{base_id}{random_suffix}"

def format_currency(amount):
    """Format amount as currency"""
    if amount is None:
        return "$0.00"
    return f"${amount:,.2f}"

def format_date(date):
    """Format datetime to readable string"""
    if date:
        return date.strftime('%d %b %Y, %I:%M %p')
    return ""

def get_device_brands(device_type):
    """Return appropriate brand list based on device type"""
    if device_type == 'Phone':
        return current_app.config['PHONE_BRANDS']
    elif device_type == 'Laptop':
        return current_app.config['LAPTOP_BRANDS']
    else:
        return ['Apple', 'Samsung', 'Dell', 'HP', 'Lenovo', 'Other']

def calculate_stats(repairs):
    """Calculate repair statistics"""
    stats = {
        'total': len(repairs),
        'completed': 0,
        'in_progress': 0,
        'waiting_parts': 0,
        'revenue': 0
    }
    
    for repair in repairs:
        if repair.status in ['Completed', 'Ready for Pickup']:
            stats['completed'] += 1
        elif repair.status == 'Waiting for Parts':
            stats['waiting_parts'] += 1
        else:
            stats['in_progress'] += 1
        
        stats['revenue'] += repair.actual_cost or 0
    
    return stats