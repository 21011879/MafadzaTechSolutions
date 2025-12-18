from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model, UserMixin):
    """
    Admin user model for dashboard access
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    repairs_updated = db.relationship('Repair', backref='admin_updater', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class Customer(db.Model):
    """
    Customer information model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    repairs = db.relationship('Repair', backref='customer', lazy=True)
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class Repair(db.Model):
    """
    Main repair tracking model
    """
    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Customer and device info
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    device_type = db.Column(db.String(20), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    serial_number = db.Column(db.String(100))
    problem_description = db.Column(db.Text, nullable=False)
    
    # Repair details
    status = db.Column(db.String(30), default='Received')
    internal_notes = db.Column(db.Text)
    estimated_cost = db.Column(db.Float, default=0.0)
    actual_cost = db.Column(db.Float, default=0.0)
    deposit_paid = db.Column(db.Float, default=0.0)
    is_paid = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Admin who last updated
    updated_by = db.Column(db.Integer, db.ForeignKey('admin.id'))
    
    # Relationships
    payments = db.relationship('Payment', backref='repair', lazy=True)
    
    def __repr__(self):
        return f'<Repair {self.tracking_id}>'
    
    def get_status_color(self):
        """Return Bootstrap color class based on status"""
        status_colors = {
            'Received': 'primary',
            'Diagnosing': 'info',
            'Waiting for Parts': 'warning',
            'Repairing': 'secondary',
            'Testing': 'info',
            'Completed': 'success',
            'Ready for Pickup': 'success'
        }
        return status_colors.get(self.status, 'secondary')

class Payment(db.Model):
    """
    Payment tracking model
    """
    id = db.Column(db.Integer, primary_key=True)
    repair_id = db.Column(db.Integer, db.ForeignKey('repair.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20))  # Cash, Ecocash, Bank Transfer, etc.
    reference = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment ${self.amount} for Repair {self.repair_id}>'

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))