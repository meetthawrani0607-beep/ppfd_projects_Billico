"""
Dashboard Routes
Main dashboard and analytics views
"""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models import db
from models.inventory import InventoryItem
from models.transaction import StockTransaction
from models.upload_log import UploadLog
from models.alert import Alert
from sqlalchemy import func, desc
from datetime import datetime, timedelta

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
@login_required
def index():
    """Main dashboard page"""
    
    # Get statistics
    total_items = InventoryItem.query.filter_by(created_by=current_user.id).count()
    
    total_quantity = db.session.query(func.sum(InventoryItem.quantity)).filter_by(
        created_by=current_user.id
    ).scalar() or 0
    
    total_value = db.session.query(
        func.sum(InventoryItem.quantity * InventoryItem.unit_price)
    ).filter_by(created_by=current_user.id).scalar() or 0
    
    low_stock_count = InventoryItem.query.filter_by(
        created_by=current_user.id,
        stock_status='low'
    ).count()
    
    out_of_stock_count = InventoryItem.query.filter_by(
        created_by=current_user.id,
        stock_status='out_of_stock'
    ).count()
    
    # Get recent items (last 5 updated)
    recent_items = InventoryItem.query.filter_by(
        created_by=current_user.id
    ).order_by(desc(InventoryItem.updated_at)).limit(5).all()
    
    # Get low stock items
    low_stock_items = InventoryItem.query.filter(
        InventoryItem.created_by == current_user.id,
        InventoryItem.stock_status.in_(['low', 'out_of_stock'])
    ).order_by(InventoryItem.quantity).limit(5).all()
    
    # Get recent uploads
    recent_uploads = UploadLog.query.filter_by(
        user_id=current_user.id
    ).order_by(desc(UploadLog.upload_time)).limit(5).all()
    
    # Get unread alerts
    unread_alerts = Alert.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).order_by(desc(Alert.created_at)).limit(5).all()
    
    return render_template('dashboard/index.html',
                         total_items=total_items,
                         total_quantity=int(total_quantity),
                         total_value=float(total_value),
                         low_stock_count=low_stock_count,
                         out_of_stock_count=out_of_stock_count,
                         recent_items=recent_items,
                         low_stock_items=low_stock_items,
                         recent_uploads=recent_uploads,
                         unread_alerts=unread_alerts)


@dashboard.route('/analytics')
@login_required
def analytics():
    """Analytics page with charts"""
    return render_template('dashboard/analytics.html')


@dashboard.route('/profile')
@login_required
def profile():
    """User profile page"""
    # Get recent inventory items
    from models.inventory import InventoryItem
    recent_items = InventoryItem.query.filter_by(
        created_by=current_user.id
    ).order_by(InventoryItem.updated_at.desc()).limit(5).all()
    
    return render_template('dashboard/profile.html', user=current_user, recent_items=recent_items)


@dashboard.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    from flask import request, flash, redirect, url_for
    from utils.validators import clean_text
    
    if request.method == 'POST':
        # Get form data
        full_name = clean_text(request.form.get('full_name', ''))
        email = clean_text(request.form.get('email', ''))
        
        # Validation
        errors = []
        
        if email and email != current_user.email:
            # Check if email already exists
            from models.user import User
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                errors.append('Email already in use by another account')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('dashboard/profile_edit.html', user=current_user)
        
        # Update user
        try:
            if full_name:
                current_user.full_name = full_name
            if email:
                current_user.email = email
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('dashboard.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'danger')
            print(f"Profile update error: {str(e)}")
    
    return render_template('dashboard/profile_edit.html', user=current_user)


@dashboard.route('/settings')
@login_required
def settings():
    """Application settings page"""
    return render_template('dashboard/settings.html', user=current_user)
