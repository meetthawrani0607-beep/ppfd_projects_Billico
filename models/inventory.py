"""
Inventory Item Model
Core inventory management model
"""
from models import db
from datetime import datetime


class InventoryItem(db.Model):
    """Inventory item model"""
    
    __tablename__ = 'inventory_items'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Item information
    item_name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    sku = db.Column(db.String(100), unique=True, index=True)
    
    # Quantity and pricing
    quantity = db.Column(db.Integer, nullable=False, default=0, index=True)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    reorder_level = db.Column(db.Integer, default=10)
    
    # Location
    location = db.Column(db.String(100))
    
    # Stock status (managed by database trigger)
    stock_status = db.Column(db.Enum('healthy', 'medium', 'low', 'out_of_stock', 
                                    name='stock_status_enum'), 
                             default='healthy', index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_restocked = db.Column(db.DateTime)
    
    # Foreign keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    transactions = db.relationship('StockTransaction', backref='item', lazy='dynamic',
                                  cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='item', lazy='dynamic',
                           cascade='all, delete-orphan')
    
    def __init__(self, item_name, quantity=0, unit_price=0.00, reorder_level=10,
                 description=None, sku=None, category_id=None, supplier_id=None):
        """Initialize inventory item"""
        self.item_name = item_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.reorder_level = reorder_level
        self.description = description
        self.sku = sku
        self.category_id = category_id
        self.supplier_id = supplier_id
        self.update_stock_status()
    
    def update_stock_status(self):
        """Update stock status based on quantity"""
        if self.quantity == 0:
            self.stock_status = 'out_of_stock'
        elif self.quantity <= self.reorder_level:
            self.stock_status = 'low'
        elif self.quantity <= (self.reorder_level * 2):
            self.stock_status = 'medium'
        else:
            self.stock_status = 'healthy'
    
    def add_stock(self, quantity, unit_price=None, created_by=None, reference=None, notes=None):
        """Add stock to inventory"""
        from models.transaction import StockTransaction
        
        if unit_price:
            self.unit_price = unit_price
        
        quantity_before = self.quantity
        self.quantity += quantity
        self.last_restocked = datetime.utcnow()
        self.update_stock_status()
        
        # Create transaction record
        transaction = StockTransaction(
            item_id=self.id,
            transaction_type='purchase',
            quantity_change=quantity,
            quantity_before=quantity_before,
            quantity_after=self.quantity,
            unit_price=self.unit_price,
            total_amount=quantity * self.unit_price,
            reference_number=reference,
            notes=notes,
            created_by=created_by
        )
        db.session.add(transaction)
        return transaction
    
    def remove_stock(self, quantity, created_by=None, reference=None, notes=None, transaction_type='sale'):
        """Remove stock from inventory"""
        from models.transaction import StockTransaction
        
        if quantity > self.quantity:
            raise ValueError(f"Insufficient stock. Available: {self.quantity}, Requested: {quantity}")
        
        quantity_before = self.quantity
        self.quantity -= quantity
        self.update_stock_status()
        
        # Create transaction record
        transaction = StockTransaction(
            item_id=self.id,
            transaction_type=transaction_type,
            quantity_change=-quantity,
            quantity_before=quantity_before,
            quantity_after=self.quantity,
            unit_price=self.unit_price,
            total_amount=quantity * self.unit_price,
            reference_number=reference,
            notes=notes,
            created_by=created_by
        )
        db.session.add(transaction)
        return transaction
    
    def adjust_stock(self, new_quantity, created_by=None, notes=None):
        """Adjust stock to specific quantity"""
        from models.transaction import StockTransaction
        
        quantity_before = self.quantity
        quantity_change = new_quantity - quantity_before
        self.quantity = new_quantity
        self.update_stock_status()
        
        # Create transaction record
        transaction = StockTransaction(
            item_id=self.id,
            transaction_type='adjustment',
            quantity_change=quantity_change,
            quantity_before=quantity_before,
            quantity_after=self.quantity,
            unit_price=self.unit_price,
            notes=notes,
            created_by=created_by
        )
        db.session.add(transaction)
        return transaction
    
    def get_total_value(self):
        """Get total value of current stock"""
        return float(self.quantity * self.unit_price)
    
    def needs_reorder(self):
        """Check if item needs reordering"""
        return self.quantity <= self.reorder_level
    
    def get_status_badge_class(self):
        """Get Bootstrap badge class for status"""
        status_classes = {
            'healthy': 'success',
            'medium': 'warning',
            'low': 'danger',
            'out_of_stock': 'dark'
        }
        return status_classes.get(self.stock_status, 'secondary')
    
    def to_dict(self):
        """Convert item to dictionary"""
        return {
            'id': self.id,
            'item_name': self.item_name,
            'description': self.description,
            'sku': self.sku,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'total_value': self.get_total_value(),
            'reorder_level': self.reorder_level,
            'stock_status': self.stock_status,
            'status_badge_class': self.get_status_badge_class(),
            'needs_reorder': self.needs_reorder(),
            'location': self.location,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier.name if self.supplier else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_restocked': self.last_restocked.isoformat() if self.last_restocked else None
        }
    
    def __repr__(self):
        return f'<InventoryItem {self.item_name} (Qty: {self.quantity})>'
