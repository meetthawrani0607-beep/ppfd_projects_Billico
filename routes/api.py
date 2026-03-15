"""
API Routes
RESTful API endpoints
"""
from flask import Blueprint, jsonify, request
from flask_login import current_user
from models import db
from models.inventory import InventoryItem
from models.transaction import StockTransaction
from models.upload_log import UploadLog
from models.alert import Alert
from models.category import Category
from utils.decorators import login_required_api, json_response
from sqlalchemy import func, desc
from datetime import datetime, timedelta

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/inventory', methods=['GET'])
@login_required_api
def get_inventory():
    """Get all inventory items"""
    
    # Get items for current user
    items = InventoryItem.query.filter_by(created_by=current_user.id).all()
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in items]
    })


@api.route('/inventory/<int:item_id>', methods=['GET'])
@login_required_api
def get_inventory_item(item_id):
    """Get single inventory item"""
    
    item = InventoryItem.query.get_or_404(item_id)
    
    # Check ownership
    if item.created_by != current_user.id:
        return jsonify({
            'success': False,
            'error': 'Unauthorized'
        }), 403
    
    return jsonify({
        'success': True,
        'data': item.to_dict()
    })


@api.route('/analytics/stats', methods=['GET'])
@login_required_api
def get_stats():
    """Get dashboard statistics"""
    
    # Total items
    total_items = InventoryItem.query.filter_by(created_by=current_user.id).count()
    
    # Total quantity
    total_quantity = db.session.query(func.sum(InventoryItem.quantity)).filter_by(
        created_by=current_user.id
    ).scalar() or 0
    
    # Total value
    total_value = db.session.query(
        func.sum(InventoryItem.quantity * InventoryItem.unit_price)
    ).filter_by(created_by=current_user.id).scalar() or 0
    
    # Stock status counts
    stock_by_status = db.session.query(
        InventoryItem.stock_status,
        func.count(InventoryItem.id)
    ).filter_by(created_by=current_user.id).group_by(InventoryItem.stock_status).all()
    
    status_counts = {status: count for status, count in stock_by_status}
    
    # Recent uploads count
    recent_uploads = UploadLog.query.filter_by(user_id=current_user.id).count()
    
    return jsonify({
        'success': True,
        'data': {
            'total_items': total_items,
            'total_quantity': int(total_quantity),
            'total_value': float(total_value),
            'stock_status': status_counts,
            'recent_uploads': recent_uploads
        }
    })


@api.route('/analytics/trends', methods=['GET'])
@login_required_api
def get_trends():
    """Get stock trends for charts"""
    
    # Get last 30 days of transactions
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    transactions = db.session.query(
        func.date(StockTransaction.transaction_date).label('date'),
        func.count(StockTransaction.id).label('count'),
        func.sum(StockTransaction.quantity_change).label('total_change')
    ).join(InventoryItem).filter(
        InventoryItem.created_by == current_user.id,
        StockTransaction.transaction_date >= thirty_days_ago
    ).group_by(func.date(StockTransaction.transaction_date)).all()
    
    trend_data = [
        {
            'date': str(t.date),
            'count': t.count,
            'total_change': int(t.total_change) if t.total_change else 0
        }
        for t in transactions
    ]
    
    return jsonify({
        'success': True,
        'data': trend_data
    })


@api.route('/analytics/low-stock', methods=['GET'])
@login_required_api
def get_low_stock():
    """Get low stock items"""
    
    items = InventoryItem.query.filter(
        InventoryItem.created_by == current_user.id,
        InventoryItem.stock_status.in_(['low', 'out_of_stock'])
    ).order_by(InventoryItem.quantity).all()
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in items]
    })


@api.route('/analytics/category-distribution', methods=['GET'])
@login_required_api
def get_category_distribution():
    """Get inventory distribution by category"""
    
    distribution = db.session.query(
        Category.name,
        func.count(InventoryItem.id).label('count'),
        func.sum(InventoryItem.quantity).label('total_qty'),
        func.sum(InventoryItem.quantity * InventoryItem.unit_price).label('total_value')
    ).join(Category, Category.id == InventoryItem.category_id, isouter=True
    ).filter(
        InventoryItem.created_by == current_user.id
    ).group_by(Category.name).all()
    
    data = [
        {
            'category': d.name or 'Uncategorized',
            'count': d.count,
            'total_quantity': int(d.total_qty) if d.total_qty else 0,
            'total_value': float(d.total_value) if d.total_value else 0
        }
        for d in distribution
    ]
    
    return jsonify({
        'success': True,
        'data': data
    })


@api.route('/analytics/stock-health', methods=['GET'])
@login_required_api
def get_stock_health():
    """Get stock health distribution for pie chart"""
    
    stock_health = db.session.query(
        InventoryItem.stock_status,
        func.count(InventoryItem.id).label('count')
    ).filter_by(
        created_by=current_user.id
    ).group_by(InventoryItem.stock_status).all()
    
    data = [
        {
            'status': s.stock_status,
            'count': s.count
        }
        for s in stock_health
    ]
    
    return jsonify({
        'success': True,
        'data': data
    })


@api.route('/alerts', methods=['GET'])
@login_required_api
def get_alerts():
    """Get user alerts"""
    
    unread_only = request.args.get('unread', 'false').lower() == 'true'
    
    query = Alert.query.filter_by(user_id=current_user.id)
    
    if unread_only:
        query = query.filter_by(is_read=False)
    
    alerts = query.order_by(desc(Alert.created_at)).limit(50).all()
    
    return jsonify({
        'success': True,
        'data': [alert.to_dict() for alert in alerts]
    })


@api.route('/alerts/<int:alert_id>/read', methods=['POST'])
@login_required_api
def mark_alert_read(alert_id):
    """Mark alert as read"""
    
    alert = Alert.query.get_or_404(alert_id)
    
    # Check ownership
    if alert.user_id != current_user.id:
        return jsonify({
            'success': False,
            'error': 'Unauthorized'
        }), 403
    
    alert.mark_as_read()
    
    return jsonify({
        'success': True,
        'message': 'Alert marked as read'
    })


@api.route('/upload/status/<int:upload_id>', methods=['GET'])
@login_required_api
def get_upload_status(upload_id):
    """Get upload processing status"""
    
    upload = UploadLog.query.get_or_404(upload_id)
    
    # Check ownership
    if upload.user_id != current_user.id:
        return jsonify({
            'success': False,
            'error': 'Unauthorized'
        }), 403
    
    return jsonify({
        'success': True,
        'data': upload.to_dict()
    })
