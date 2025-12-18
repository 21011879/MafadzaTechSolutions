from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    """
    Application factory function to create and configure the Flask app
    """
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'admin.login'
    login_manager.login_message_category = 'info'
    
    # Import and register blueprints
    from app.routes import main_bp, admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Context processors - ADD THEM HERE
    @app.context_processor
    def inject_now():
        """Inject current datetime into all templates"""
        return {'now': datetime.utcnow()}
    
    @app.context_processor
    def inject_config():
        """Inject config into all templates"""
        return {'config': app.config}
    
    
    
    # Create database tables
    with app.app_context():
        db.create_all()

        # Add context processors using lambda functions
    @app.context_processor
    def inject_variables():
        from datetime import datetime
        return {
            'now': datetime.utcnow(),
            'config': app.config
        }
    

        # Create default admin user if not exists
        if app.config.get('CREATE_DEFAULT_ADMIN', False):
           from app.models import Admin
           from werkzeug.security import generate_password_hash
        
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            default_admin = Admin(
                username=app.config['ADMIN_USERNAME'],
                email=app.config['ADMIN_EMAIL'],
                password_hash=generate_password_hash(app.config['ADMIN_PASSWORD'])
            )
            db.session.add(default_admin)
            db.session.commit()
            print("✓ Default admin user created!")
            print(f"  Username: {app.config['ADMIN_USERNAME']}")
            print(f"  Password: {app.config['ADMIN_PASSWORD']}")
            print("  ⚠️  Change this password after first login!")
    
    return app