"""
Supplier Model
Vendor/supplier information management
"""
from models import db
from datetime import datetime


class Supplier(db.Model):
    """Supplier/vendor model"""
    
    __tablename__ = 'suppliers'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Supplier information
    name = db.Column(db.String(200), nullable=False, index=True)
    contact_person = db.Column(db.String(150))
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(20))
    
    # Address
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    inventory_items = db.relationship('InventoryItem', backref='supplier', lazy='dynamic')
    
    def __init__(self, name, contact_person=None, email=None, phone=None, 
                 address=None, city=None, state=None, country=None, postal_code=None):
        """Initialize supplier"""
        self.name = name
        self.contact_person = contact_person
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code
    
    def get_full_address(self):
        """Get formatted full address"""
        parts = [self.address, self.city, self.state, self.postal_code, self.country]
        return ', '.join([p for p in parts if p])
    
    def get_item_count(self):
        """Get number of items from this supplier"""
        return self.inventory_items.count()
    
    def to_dict(self):
        """Convert supplier to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'contact_person': self.contact_person,
            'email': self.email,
            'phone': self.phone,
            'address': self.get_full_address(),
            'is_active': self.is_active,
            'item_count': self.get_item_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Supplier {self.name}>'
