"""
Models Package
Initialize database and import all models
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'info'


def init_app(app):
    """Initialize database and login manager with app"""
    db.init_app(app)
    login_manager.init_app(app)
    
    # Import models here to avoid circular imports
    from models.user import User
    from models.inventory import InventoryItem
    from models.supplier import Supplier
    from models.transaction import StockTransaction
    from models.upload_log import UploadLog
    from models.category import Category
    from models.alert import Alert
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return db
