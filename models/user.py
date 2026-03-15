"""
User Model
Handles user authentication and account management
"""
from models import db
from flask_login import UserMixin
import bcrypt
from datetime import datetime


class User(UserMixin, db.Model):
    """User account model"""
    
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User credentials
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # User information
    full_name = db.Column(db.String(150))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    inventory_items = db.relationship('InventoryItem', backref='creator', lazy='dynamic', 
                                     foreign_keys='InventoryItem.created_by')
    transactions = db.relationship('StockTransaction', backref='user', lazy='dynamic')
    upload_logs = db.relationship('UploadLog', backref='user', lazy='dynamic')
    alerts = db.relationship('Alert', backref='user', lazy='dynamic')
    
    def __init__(self, username, email, password, full_name=None):
        """Initialize user"""
        self.username = username
        self.email = email
        self.set_password(password)
        self.full_name = full_name
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check if password is correct"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def get_stats(self):
        """Get user statistics"""
        return {
            'total_items': self.inventory_items.count(),
            'total_uploads': self.upload_logs.count(),
            'unread_alerts': self.alerts.filter_by(is_read=False).count()
        }
    
    def unread_alerts_count(self):
        """Get count of unread alerts"""
        return self.alerts.filter_by(is_read=False).count()
    
    def get_recent_alerts(self, limit=5):
        """Get recent alerts for user"""
        from models.alert import Alert
        return self.alerts.order_by(Alert.created_at.desc()).limit(limit).all()
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
