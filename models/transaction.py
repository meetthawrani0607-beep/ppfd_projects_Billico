"""
Stock Transaction Model
Track all inventory movements
"""
from models import db
from datetime import datetime


class StockTransaction(db.Model):
    """Stock transaction model for tracking inventory movements"""
    
    __tablename__ = 'stock_transactions'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Transaction details
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), 
                       nullable=False, index=True)
    transaction_type = db.Column(db.Enum('purchase', 'sale', 'adjustment', 'return', 'damage',
                                        name='transaction_type_enum'),
                                 nullable=False, index=True)
    
    # Quantities
    quantity_change = db.Column(db.Integer, nullable=False)
    quantity_before = db.Column(db.Integer, nullable=False)
    quantity_after = db.Column(db.Integer, nullable=False)
    
    # Pricing
    unit_price = db.Column(db.Numeric(10, 2))
    total_amount = db.Column(db.Numeric(10, 2))
    
    # Reference and notes
    reference_number = db.Column(db.String(100), index=True)
    notes = db.Column(db.Text)
    
    # Timestamp
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # User tracking
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self, item_id, transaction_type, quantity_change, 
                 quantity_before, quantity_after, unit_price=None, 
                 total_amount=None, reference_number=None, notes=None, created_by=None):
        """Initialize transaction"""
        self.item_id = item_id
        self.transaction_type = transaction_type
        self.quantity_change = quantity_change
        self.quantity_before = quantity_before
        self.quantity_after = quantity_after
        self.unit_price = unit_price
        self.total_amount = total_amount
        self.reference_number = reference_number
        self.notes = notes
        self.created_by = created_by
    
    def get_type_badge_class(self):
        """Get Bootstrap badge class for transaction type"""
        type_classes = {
            'purchase': 'success',
            'sale': 'primary',
            'adjustment': 'warning',
            'return': 'info',
            'damage': 'danger'
        }
        return type_classes.get(self.transaction_type, 'secondary')
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item_name': self.item.item_name if self.item else None,
            'transaction_type': self.transaction_type,
            'type_badge_class': self.get_type_badge_class(),
            'quantity_change': self.quantity_change,
            'quantity_before': self.quantity_before,
            'quantity_after': self.quantity_after,
            'unit_price': float(self.unit_price) if self.unit_price else None,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'reference_number': self.reference_number,
            'notes': self.notes,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'created_by': self.created_by,
            'user_name': self.user.username if self.user else None
        }
    
    def __repr__(self):
        return f'<Transaction {self.transaction_type} - Item:{self.item_id} - Qty:{self.quantity_change}>'
