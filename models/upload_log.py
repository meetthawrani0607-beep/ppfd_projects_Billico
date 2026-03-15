"""
Upload Log Model
Track bill/receipt uploads and OCR processing
"""
from models import db
from datetime import datetime
import json


class UploadLog(db.Model):
    """Upload log model for tracking bill uploads and OCR processing"""
    
    __tablename__ = 'upload_logs'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), 
                       nullable=False, index=True)
    
    # File information
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(50))
    
    # OCR processing status
    ocr_status = db.Column(db.Enum('pending', 'processing', 'completed', 'failed',
                                  name='ocr_status_enum'),
                          default='pending', index=True)
    ocr_text = db.Column(db.Text)
    ocr_confidence = db.Column(db.Numeric(5, 2))
    
    # Extracted data
    extracted_data = db.Column(db.JSON)
    items_extracted = db.Column(db.Integer, default=0)
    items_added = db.Column(db.Integer, default=0)
    
    # Bill information
    bill_number = db.Column(db.String(100), index=True)
    bill_date = db.Column(db.Date)
    supplier_name = db.Column(db.String(200))
    total_amount = db.Column(db.Numeric(10, 2))
    
    # Processing timestamps
    upload_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    processing_started = db.Column(db.DateTime)
    processing_completed = db.Column(db.DateTime)
    
    # Error handling
    error_message = db.Column(db.Text)
    
    def __init__(self, user_id, filename, original_filename, file_path, 
                 file_size=None, file_type=None):
        """Initialize upload log"""
        self.user_id = user_id
        self.filename = filename
        self.original_filename = original_filename
        self.file_path = file_path
        self.file_size = file_size
        self.file_type = file_type
    
    def set_extracted_data(self, data):
        """Set extracted data as JSON"""
        self.extracted_data = data
        if data and 'items' in data:
            self.items_extracted = len(data['items'])
    
    def get_extracted_data(self):
        """Get extracted data"""
        return self.extracted_data if self.extracted_data else {}
    
    def mark_processing(self):
        """Mark as processing"""
        self.ocr_status = 'processing'
        self.processing_started = datetime.utcnow()
        db.session.commit()
    
    def mark_completed(self):
        """Mark as completed"""
        self.ocr_status = 'completed'
        self.processing_completed = datetime.utcnow()
        db.session.commit()
    
    def mark_failed(self, error_message):
        """Mark as failed"""
        self.ocr_status = 'failed'
        self.error_message = error_message
        self.processing_completed = datetime.utcnow()
        db.session.commit()
    
    def get_processing_time(self):
        """Get processing time in seconds"""
        if self.processing_started and self.processing_completed:
            delta = self.processing_completed - self.processing_started
            return delta.total_seconds()
        return None
    
    def get_status_badge_class(self):
        """Get Bootstrap badge class for status"""
        status_classes = {
            'pending': 'secondary',
            'processing': 'info',
            'completed': 'success',
            'failed': 'danger'
        }
        return status_classes.get(self.ocr_status, 'secondary')
    
    def to_dict(self):
        """Convert upload log to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'ocr_status': self.ocr_status,
            'status_badge_class': self.get_status_badge_class(),
            'ocr_text': self.ocr_text,
            'ocr_confidence': float(self.ocr_confidence) if self.ocr_confidence else None,
            'extracted_data': self.get_extracted_data(),
            'items_extracted': self.items_extracted,
            'items_added': self.items_added,
            'bill_number': self.bill_number,
            'bill_date': self.bill_date.isoformat() if self.bill_date else None,
            'supplier_name': self.supplier_name,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'upload_time': self.upload_time.isoformat() if self.upload_time else None,
            'processing_time': self.get_processing_time(),
            'error_message': self.error_message
        }
    
    def __repr__(self):
        return f'<UploadLog {self.filename} - {self.ocr_status}>'
