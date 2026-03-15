"""
Validators
Input validation utilities
"""
import re
from email.utils import parseaddr


def is_valid_email(email):
    """
    Validate email address
    
    Args:
        email: Email string to validate
        
    Returns:
        Boolean indicating validity
    """
    if not email:
        return False
    
    # Basic email pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(pattern, email))


def is_valid_username(username):
    """
    Validate username
    
    Args:
        username: Username string to validate
        
    Returns:
        Boolean indicating validity
    """
    if not username:
        return False
    
    # Username: 3-80 characters, alphanumeric and underscore
    if len(username) < 3 or len(username) > 80:
        return False
    
    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, username))


def is_valid_password(password):
    """
    Validate password strength
    
    Args:
        password: Password string to validate
        
    Returns:
        Tuple (is_valid, message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if len(password) > 128:
        return False, "Password is too long"
    
    # Check for at least one letter and one number (optional)
    # has_letter = bool(re.search(r'[a-zA-Z]', password))
    # has_number = bool(re.search(r'\d', password))
    
    # if not (has_letter and has_number):
    #     return False, "Password must contain both letters and numbers"
    
    return True, "Password is strong"


def sanitize_filename(filename):
    """
    Sanitize filename to prevent security issues
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Remove or replace dangerous characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')
    
    return filename


def is_allowed_file(filename, allowed_extensions):
    """
    Check if file extension is allowed
    
    Args:
        filename: Filename to check
        allowed_extensions: Set of allowed extensions
        
    Returns:
        Boolean indicating if allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def validate_number(value, min_value=None, max_value=None):
    """
    Validate numeric value
    
    Args:
        value: Value to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        Tuple (is_valid, message)
    """
    try:
        num = float(value)
        
        if min_value is not None and num < min_value:
            return False, f"Value must be at least {min_value}"
        
        if max_value is not None and num > max_value:
            return False, f"Value must not exceed {max_value}"
        
        return True, "Valid number"
        
    except (ValueError, TypeError):
        return False, "Invalid number format"


def validate_quantity(quantity):
    """
    Validate quantity (must be positive integer)
    
    Args:
        quantity: Quantity to validate
        
    Returns:
        Tuple (is_valid, message)
    """
    try:
        qty = int(quantity)
        
        if qty < 0:
            return False, "Quantity cannot be negative"
        
        return True, "Valid quantity"
        
    except (ValueError, TypeError):
        return False, "Quantity must be a whole number"


def validate_price(price):
    """
    Validate price (must be non-negative decimal)
    
    Args:
        price: Price to validate
        
    Returns:
        Tuple (is_valid, message)
    """
    try:
        p = float(price)
        
        if p < 0:
            return False, "Price cannot be negative"
        
        return True, "Valid price"
        
    except (ValueError, TypeError):
        return False, "Price must be a valid number"


def clean_text(text, max_length=None):
    """
    Clean and sanitize text input
    
    Args:
        text: Text to clean
        max_length: Maximum allowed length
        
    Returns:
        Cleaned text
    """
    if not text:
        return ''
    
    # Strip whitespace
    text = text.strip()
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Limit length
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text
