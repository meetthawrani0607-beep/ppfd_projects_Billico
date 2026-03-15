"""
Decorators
Custom decorators for routes
"""
from functools import wraps
from flask import jsonify, flash, redirect, url_for
from flask_login import current_user


def login_required_api(f):
    """
    Decorator for API endpoints that require authentication
    Returns JSON error if not authenticated
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorator for routes that require admin access
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('auth.login'))
        
        # You can add admin check here if you implement roles
        # if not current_user.is_admin:
        #    flash('Admin access required.', 'danger')
        #    return redirect(url_for('dashboard.index'))
        
        return f(*args, **kwargs)
    return decorated_function


def json_response(f):
    """
    Decorator to automatically wrap return values in JSON response
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            
            if isinstance(result, tuple):
                # (data, status_code)
                return jsonify(result[0]), result[1]
            else:
                # Just data
                return jsonify(result)
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
            
    return decorated_function
