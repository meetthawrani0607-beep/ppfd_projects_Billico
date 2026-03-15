"""
Category Model
Product categories for inventory organization
"""
from models import db
from datetime import datetime


class Category(db.Model):
    """Product category model"""
    
    __tablename__ = 'categories'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Category information
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    inventory_items = db.relationship('InventoryItem', backref='category', lazy='dynamic')
    
    def __init__(self, name, description=None):
        """Initialize category"""
        self.name = name
        self.description = description
    
    def get_item_count(self):
        """Get number of items in this category"""
        return self.inventory_items.count()
    
    def get_total_value(self):
        """Get total value of items in this category"""
        total = 0
        for item in self.inventory_items:
            total += item.quantity * item.unit_price
        return total
    
    def to_dict(self):
        """Convert category to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'item_count': self.get_item_count(),
            'total_value': float(self.get_total_value()),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'
