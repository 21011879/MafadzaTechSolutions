from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Admin, Customer, Repair, Payment
from app.utils import generate_tracking_id, calculate_stats
from datetime import datetime, timedelta
import json

# Create blueprints
main_bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__)

# ======================
# PUBLIC ROUTES
# ======================

@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main_bp.route('/book-repair', methods=['GET', 'POST'])
def book_repair():
    """Booking form for customers"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        device_type = request.form.get('device_type')
        brand = request.form.get('brand')
        model = request.form.get('model')
        problem = request.form.get('problem')
        deposit = request.form.get('deposit', 0.0)
        
        # Validate required fields
        if not all([name, phone, device_type, brand, model, problem]):
            flash('Please fill in all required fields', 'danger')
            return render_template('book_repair.html')
        
        try:
            # Create or find customer
            customer = Customer.query.filter_by(phone=phone).first()
            if not customer:
                customer = Customer(
                    name=name,
                    phone=phone,
                    email=email,
                    address=request.form.get('address', '')
                )
                db.session.add(customer)
                db.session.commit()
            
            # Create repair record
            repair = Repair(
                tracking_id=generate_tracking_id(),
                customer_id=customer.id,
                device_type=device_type,
                brand=brand,
                model=model,
                serial_number=request.form.get('serial_number', ''),
                problem_description=problem,
                deposit_paid=float(deposit) if deposit else 0.0,
                status='Received'
            )
            
            db.session.add(repair)
            db.session.commit()
            
            # If deposit was paid, create payment record
            if deposit and float(deposit) > 0:
                payment = Payment(
                    repair_id=repair.id,
                    amount=float(deposit),
                    payment_method=request.form.get('payment_method', 'Cash'),
                    reference=request.form.get('payment_reference', ''),
                    notes='Initial deposit'
                )
                db.session.add(payment)
                db.session.commit()
            
            flash(f'Repair booked successfully! Your Tracking ID: {repair.tracking_id}', 'success')
            return redirect(url_for('main.booking_success', tracking_id=repair.tracking_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('book_repair.html')

@main_bp.route('/booking-success/<tracking_id>')
def booking_success(tracking_id):
    """Display success page after booking"""
    repair = Repair.query.filter_by(tracking_id=tracking_id).first_or_404()
    return render_template('booking_success.html', repair=repair)

@main_bp.route('/track-repair', methods=['GET', 'POST'])
def track_repair():
    """Track repair status"""
    repair = None
    
    if request.method == 'POST':
        tracking_id = request.form.get('tracking_id', '').strip().upper()
        
        if tracking_id:
            repair = Repair.query.filter_by(tracking_id=tracking_id).first()
            if not repair:
                flash('Invalid tracking ID. Please check and try again.', 'danger')
        else:
            flash('Please enter a tracking ID', 'warning')
    
    return render_template('track_repair.html', repair=repair)

# ======================
# ADMIN ROUTES
# ======================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    """Admin logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    # Get recent repairs
    recent_repairs = Repair.query.order_by(Repair.created_at.desc()).limit(10).all()
    
    # Get all repairs for statistics
    all_repairs = Repair.query.all()
    
    # Calculate statistics
    stats = calculate_stats(all_repairs)
    
    # Get repairs by status
    status_counts = {}
    for status in ['Received', 'Diagnosing', 'Waiting for Parts', 'Repairing', 'Testing', 'Completed', 'Ready for Pickup']:
        status_counts[status] = Repair.query.filter_by(status=status).count()
    
    return render_template('admin/dashboard.html', 
                         repairs=recent_repairs, 
                         stats=stats,
                         status_counts=status_counts)

@admin_bp.route('/repairs')
@login_required
def repairs():
    """List all repairs with filtering"""
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('search', '')
    
    query = Repair.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if search_query:
        query = query.filter(
            (Repair.tracking_id.contains(search_query)) |
            (Repair.model.contains(search_query)) |
            (Repair.brand.contains(search_query))
        )
    
    repairs = query.order_by(Repair.created_at.desc()).all()
    
    return render_template('admin/repairs.html', repairs=repairs, status_filter=status_filter)

@admin_bp.route('/repair/<int:repair_id>', methods=['GET', 'POST'])
@login_required
def repair_detail(repair_id):
    """View and update repair details"""
    repair = Repair.query.get_or_404(repair_id)
    
    if request.method == 'POST':
        # Update repair details
        repair.status = request.form.get('status', repair.status)
        repair.internal_notes = request.form.get('internal_notes', repair.internal_notes)
        repair.estimated_cost = float(request.form.get('estimated_cost', 0) or 0)
        repair.actual_cost = float(request.form.get('actual_cost', 0) or 0)
        repair.is_paid = 'is_paid' in request.form
        
        if repair.status == 'Completed' and not repair.completed_at:
            repair.completed_at = datetime.utcnow()
        
        repair.updated_by = current_user.id
        repair.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Repair updated successfully!', 'success')
    
    return render_template('admin/repair_detail.html', repair=repair)

@admin_bp.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for statistics data"""
    # Get repairs from last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_repairs = Repair.query.filter(Repair.created_at >= thirty_days_ago).all()
    
    stats = calculate_stats(recent_repairs)
    
    return jsonify(stats)

@admin_bp.route('/reports')
@login_required
def reports():
    """Generate reports"""
    # Get date range from request or default to current month
    month = request.args.get('month', datetime.now().month)
    year = request.args.get('year', datetime.now().year)
    
    # Get repairs for the selected month
    repairs = Repair.query.filter(
        db.extract('month', Repair.created_at) == month,
        db.extract('year', Repair.created_at) == year
    ).all()
    
    stats = calculate_stats(repairs)
    
    return render_template('admin/reports.html', 
                         repairs=repairs, 
                         stats=stats,
                         month=month,
                         year=year)