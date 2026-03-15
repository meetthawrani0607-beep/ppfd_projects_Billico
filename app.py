"""
Billico - Smart Inventory Automation Platform
Main Application File
"""
from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS
from config import get_config
import os

# Import models
from models import db, init_app as init_models

# Import routes
from routes.auth import auth
from routes.dashboard import dashboard
from routes.inventory import inventory_bp
from routes.upload import upload_bp
from routes.api import api


def create_app(config_name=None):
    """Application factory"""
    
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app.config.from_object(get_config())
    
    # Initialize CORS
    CORS(app)
    
    # Initialize database and login manager
    init_models(app)
    
    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(api)
    
    # Register template filters
    register_template_filters(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    # Root route
    @app.route('/')
    def index():
        """Home page - redirect to dashboard or login"""
        from flask_login import current_user
        
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    
    return app


def register_template_filters(app):
    """Register custom Jinja2 filters"""
    
    from utils.helpers import format_currency, format_date, format_datetime, time_ago
    
    app.jinja_env.filters['currency'] = format_currency
    app.jinja_env.filters['date'] = format_date
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['timeago'] = time_ago


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403


def register_cli_commands(app):
    """Register Flask CLI commands"""
    
    @app.cli.command('db-init')
    def init_db():
        """Initialize the database"""
        
        with app.app_context():
            # Create all tables
            db.create_all()
            
            # Create default categories
            from models.category import Category
            
            categories = [
                ('Electronics', 'Electronic items and devices'),
                ('Groceries', 'Food and grocery items'),
                ('Stationery', 'Office and school supplies'),
                ('Hardware', 'Hardware and tools'),
                ('Clothing', 'Apparel and accessories'),
                ('Furniture', 'Furniture items'),
                ('Other', 'Miscellaneous items')
            ]
            
            for name, description in categories:
                if not Category.query.filter_by(name=name).first():
                    category = Category(name=name, description=description)
                    db.session.add(category)
            
            db.session.commit()
            
            print("✓ Database initialized successfully!")
            print("✓ Default categories created")
    
    @app.cli.command('create-admin')
    def create_admin():
        """Create an admin user"""
        
        from models.user import User
        
        with app.app_context():
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            full_name = input("Enter full name (optional): ")
            
            # Check if user exists
            if User.query.filter_by(username=username).first():
                print(f"✗ User '{username}' already exists!")
                return
            
            if User.query.filter_by(email=email).first():
                print(f"✗ Email '{email}' already registered!")
                return
            
            # Create user
            user = User(
                username=username,
                email=email,
                password=password,
                full_name=full_name if full_name else None
            )
            
            db.session.add(user)
            db.session.commit()
            
            print(f"✓ User '{username}' created successfully!")


# Create application instance
app = create_app()


if __name__ == '__main__':
    # Ensure upload directory exists
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
