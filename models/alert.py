"""
Alert Model
System notifications and alerts
"""
from models import db
from datetime import datetime


class Alert(db.Model):
    """Alert/notification model"""
    
    __tablename__ = 'alerts'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    
    # Alert details
    alert_type = db.Column(db.Enum('low_stock', 'out_of_stock', 'high_value', 'system',
                                  name='alert_type_enum'),
                          nullable=False, index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'))
    
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    severity = db.Column(db.Enum('info', 'warning', 'critical', 
                               name='alert_severity_enum'), 
                        default='info')
    
    # Status
    is_read = db.Column(db.Boolean, default=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    read_at = db.Column(db.DateTime)
    
    def __init__(self, user_id, alert_type, title, message, 
                 item_id=None, severity='info'):
        """Initialize alert"""
        self.user_id = user_id
        self.alert_type = alert_type
        self.title = title
        self.message = message
        self.item_id = item_id
        self.severity = severity
    
    def mark_as_read(self):
        """Mark alert as read"""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()
    
    def get_severity_class(self):
        """Get Bootstrap alert class for severity"""
        severity_classes = {
            'info': 'info',
            'warning': 'warning',
            'critical': 'danger'
        }
        return severity_classes.get(self.severity, 'secondary')
    
    def get_icon(self):
        """Get icon for alert type"""
        icons = {
            'low_stock': 'exclamation-triangle',
            'out_of_stock': 'times-circle',
            'high_value': 'dollar-sign',
            'system': 'info-circle'
        }
        return icons.get(self.alert_type, 'bell')
    
    def to_dict(self):
        """Convert alert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'alert_type': self.alert_type,
            'item_id': self.item_id,
            'item_name': self.item.item_name if self.item else None,
            'title': self.title,
            'message': self.message,
            'severity': self.severity,
            'severity_class': self.get_severity_class(),
            'icon': self.get_icon(),
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
    
    @staticmethod
    def create_low_stock_alert(user_id, item):
        """Create a low stock alert"""
        alert = Alert(
            user_id=user_id,
            alert_type='low_stock',
            item_id=item.id,
            title=f'Low Stock: {item.item_name}',
            message=f'{item.item_name} is running low (Current: {item.quantity}, Reorder Level: {item.reorder_level})',
            severity='warning'
        )
        db.session.add(alert)
        return alert
    
    @staticmethod
    def create_out_of_stock_alert(user_id, item):
        """Create an out of stock alert"""
        alert = Alert(
            user_id=user_id,
            alert_type='out_of_stock',
            item_id=item.id,
            title=f'Out of Stock: {item.item_name}',
            message=f'{item.item_name} is out of stock. Please reorder immediately.',
            severity='critical'
        )
        db.session.add(alert)
        return alert
    
    def __repr__(self):
        return f'<Alert {self.alert_type} - {self.title}>'
