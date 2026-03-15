"""
Billico - Smart Inventory Automation Platform - DEMO MODE
Main Application File (Simplified for demo without OCR dependencies)
"""
from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS
from config_demo import get_config
import os

# Import models
from models import db, init_app as init_models

# Import routes (excluding upload for demo)
from routes.auth import auth
from routes.dashboard import dashboard
from routes.inventory import inventory_bp
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
    
    # Register blueprints (excluding upload for demo)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(api)
    
    # Register template filters
    register_template_filters(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Root route
    @app.route('/')
    def index():
        """Home page - redirect to dashboard or login"""
        from flask_login import current_user
        
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    
    # Demo upload route
    @app.route('/upload/')
    def upload_demo():
        return render_template('upload/bill_upload.html')
    
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


# Create application instance
app = create_app()


if __name__ == '__main__':
    # Ensure upload directory exists
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    # Initialize database with tables
    with app.app_context():
        db.create_all()
        
        # Create default categories if they don't exist
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
        
        try:
            db.session.commit()
        except:
            db.session.rollback()
    
    print("\n" + "="*60)
    print("🚀 BILLICO - Smart Inventory Automation Platform")
    print("📊 DEMO MODE - SQLite Database")
    print("="*60)
    print(f"🌐 Application starting at: http://localhost:5000")
    print(f"📝 Register at: http://localhost:5000/auth/register")
    print(f"💾 Database: billico_demo.db (SQLite)")
    print("="*60 + "\n")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
