"""
Helper Functions
General utility functions
"""
from functools import wraps
from flask import jsonify, flash
from datetime import datetime, timedelta
import os
import uuid


def generate_unique_filename(original_filename):
    """
    Generate a unique filename while preserving extension
    
    Args:
        original_filename: Original file name
        
    Returns:
        Unique filename
    """
    # Get file extension
    ext = ''
    if '.' in original_filename:
        ext = '.' + original_filename.rsplit('.', 1)[1].lower()
    
    # Generate unique name using UUID and timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:8]
    
    return f"{timestamp}_{unique_id}{ext}"


def format_currency(amount, currency_symbol='₹'):
    """
    Format amount as currency
    
    Args:
        amount: Numeric amount
        currency_symbol: Currency symbol
        
    Returns:
        Formatted string
    """
    try:
        return f"{currency_symbol}{amount:,.2f}"
    except:
        return f"{currency_symbol}0.00"


def format_date(date_obj, format_str='%d %b %Y'):
    """
    Format date object
    
    Args:
        date_obj: Date or datetime object
        format_str: Format string
        
    Returns:
        Formatted date string
    """
    if not date_obj:
        return ''
    
    try:
        if isinstance(date_obj, str):
            # Try to parse string to date
            date_obj = datetime.fromisoformat(date_obj)
        
        return date_obj.strftime(format_str)
    except:
        return str(date_obj)


def format_datetime(dt_obj, format_str='%d %b %Y %H:%M'):
    """
    Format datetime object
    
    Args:
        dt_obj: Datetime object
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    return format_date(dt_obj, format_str)


def time_ago(dt):
    """
    Get human-readable time difference
    
    Args:
        dt: Datetime object
        
    Returns:
        String like "2 hours ago"
    """
    if not dt:
        return ''
    
    now = datetime.utcnow()
    
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except:
            return str(dt)
    
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return 'just now'
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f'{days} day{"s" if days > 1 else ""} ago'
    else:
        return format_date(dt)


def calculate_percentage(part, whole):
    """
    Calculate percentage
    
    Args:
        part: Part value
        whole: Whole value
        
    Returns:
        Percentage as float
    """
    if whole == 0:
        return 0
    
    return round((part / whole) * 100, 2)


def paginate_query(query, page=1, per_page=20):
    """
    Paginate SQLAlchemy query
    
    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        per_page: Items per page
        
    Returns:
        Dictionary with pagination info
    """
    total = query.count()
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page,
        'has_prev': page > 1,
        'has_next': page * per_page < total
    }


def make_dir_if_not_exists(directory):
    """
    Create directory if it doesn't exist
    
    Args:
        directory: Directory path
        
    Returns:
        True if created or exists
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except:
        return False


def get_file_size_mb(file_path):
    """
    Get file size in MB
    
    Args:
        file_path: Path to file
        
    Returns:
        Size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)
    except:
        return 0


def safe_int(value, default=0):
    """
    Safely convert value to int
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Integer value
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default=0.0):
    """
    Safely convert value to float
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Float value
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
