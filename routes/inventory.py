"""
Inventory Routes
Inventory management views
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.inventory import InventoryItem
from models.category import Category
from models.supplier import Supplier
from models.transaction import StockTransaction
from utils.validators import clean_text, validate_quantity, validate_price
from utils.helpers import safe_int, safe_float

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')


@inventory_bp.route('/')
@login_required
def index():
    """Inventory list page"""
    
    # Get filters from query params
    search = request.args.get('search', '')
    category_id = request.args.get('category')
    status = request.args.get('status')
    sort_by = request.args.get('sort', 'updated_at')
    
    # Base query
    query = InventoryItem.query.filter_by(created_by=current_user.id)
    
    # Apply search
    if search:
        query = query.filter(
            (InventoryItem.item_name.ilike(f'%{search}%')) |
            (InventoryItem.sku.ilike(f'%{search}%')) |
            (InventoryItem.description.ilike(f'%{search}%'))
        )
    
    # Apply category filter
    if category_id:
        query = query.filter_by(category_id=safe_int(category_id))
    
    # Apply status filter
    if status:
        query = query.filter_by(stock_status=status)
    
    # Apply sorting
    if sort_by == 'name':
        query = query.order_by(InventoryItem.item_name)
    elif sort_by == 'quantity':
        query = query.order_by(InventoryItem.quantity.desc())
    elif sort_by == 'price':
        query = query.order_by(InventoryItem.unit_price.desc())
    else:  # updated_at
        query = query.order_by(InventoryItem.updated_at.desc())
    
    # Get items
    items = query.all()
    
    # Get categories for filter dropdown
    categories = Category.query.all()
    
    return render_template('dashboard/inventory.html',
                         items=items,
                         categories=categories,
                         search=search,
                         selected_category=category_id,
                         selected_status=status,
                         sort_by=sort_by)


@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new inventory item"""
    
    if request.method == 'POST':
        # Get form data
        item_name = clean_text(request.form.get('item_name', ''))
        description = clean_text(request.form.get('description', ''))
        sku = clean_text(request.form.get('sku', ''))
        quantity = request.form.get('quantity', 0)
        unit_price = request.form.get('unit_price', 0)
        reorder_level = request.form.get('reorder_level', 10)
        category_id = request.form.get('category_id')
        supplier_id = request.form.get('supplier_id')
        location = clean_text(request.form.get('location', ''))
        
        # Validation
        errors = []
        
        if not item_name:
            errors.append('Item name is required')
        
        # Validate quantity
        is_valid, msg = validate_quantity(quantity)
        if not is_valid:
            errors.append(msg)
        
        # Validate price
        is_valid, msg = validate_price(unit_price)
        if not is_valid:
            errors.append(msg)
        
        # Check if SKU already exists
        if sku and InventoryItem.query.filter_by(sku=sku).first():
            errors.append('SKU already exists')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            categories = Category.query.all()
            suppliers = Supplier.query.all()
            return render_template('dashboard/inventory_add.html',
                                 categories=categories,
                                 suppliers=suppliers,
                                 form_data=request.form)
        
        # Create item
        try:
            item = InventoryItem(
                item_name=item_name,
                description=description if description else None,
                sku=sku if sku else None,
                quantity=safe_int(quantity),
                unit_price=safe_float(unit_price),
                reorder_level=safe_int(reorder_level, 10),
                category_id=safe_int(category_id) if category_id else None,
                supplier_id=safe_int(supplier_id) if supplier_id else None
            )
            item.location = location if location else None
            item.created_by = current_user.id
            item.updated_by = current_user.id
            
            db.session.add(item)
            db.session.commit()
            
            flash(f'Item "{item_name}" added successfully!', 'success')
            return redirect(url_for('inventory.index'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the item. Please try again.', 'danger')
            print(f"Add item error: {str(e)}")
    
    # GET request - show form
    categories = Category.query.all()
    suppliers = Supplier.query.all()
    return render_template('dashboard/inventory_add.html',
                         categories=categories,
                         suppliers=suppliers)


@inventory_bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit(item_id):
    """Edit inventory item"""
    
    # Get item
    item = InventoryItem.query.get_or_404(item_id)
    
    # Check ownership
    if item.created_by != current_user.id:
        flash('You do not have permission to edit this item.', 'danger')
        return redirect(url_for('inventory.index'))
    
    if request.method == 'POST':
        # Get form data
        item_name = clean_text(request.form.get('item_name', ''))
        description = clean_text(request.form.get('description', ''))
        sku = clean_text(request.form.get('sku', ''))
        quantity = request.form.get('quantity', 0)
        unit_price = request.form.get('unit_price', 0)
        reorder_level = request.form.get('reorder_level', 10)
        category_id = request.form.get('category_id')
        supplier_id = request.form.get('supplier_id')
        location = clean_text(request.form.get('location', ''))
        
        # Validation
        errors = []
        
        if not item_name:
            errors.append('Item name is required')
        
        # Validate quantity
        is_valid, msg = validate_quantity(quantity)
        if not is_valid:
            errors.append(msg)
        
        # Validate price
        is_valid, msg = validate_price(unit_price)
        if not is_valid:
            errors.append(msg)
        
        # Check if SKU already exists (excluding current item)
        if sku:
            existing = InventoryItem.query.filter_by(sku=sku).first()
            if existing and existing.id != item.id:
                errors.append('SKU already exists')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            categories = Category.query.all()
            suppliers = Supplier.query.all()
            return render_template('dashboard/inventory_edit.html',
                                 item=item,
                                 categories=categories,
                                 suppliers=suppliers)
        
        # Update item
        try:
            item.item_name = item_name
            item.description = description if description else None
            item.sku = sku if sku else None
            item.quantity = safe_int(quantity)
            item.unit_price = safe_float(unit_price)
            item.reorder_level = safe_int(reorder_level, 10)
            item.category_id = safe_int(category_id) if category_id else None
            item.supplier_id = safe_int(supplier_id) if supplier_id else None
            item.location = location if location else None
            item.updated_by = current_user.id
            item.update_stock_status()
            
            db.session.commit()
            
            flash(f'Item "{item_name}" updated successfully!', 'success')
            return redirect(url_for('inventory.index'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the item. Please try again.', 'danger')
            print(f"Edit item error: {str(e)}")
    
    # GET request - show form
    categories = Category.query.all()
    suppliers = Supplier.query.all()
    return render_template('dashboard/inventory_edit.html',
                         item=item,
                         categories=categories,
                         suppliers=suppliers)


@inventory_bp.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete(item_id):
    """Delete inventory item"""
    
    # Get item
    item = InventoryItem.query.get_or_404(item_id)
    
    # Check ownership
    if item.created_by != current_user.id:
        flash('You do not have permission to delete this item.', 'danger')
        return redirect(url_for('inventory.index'))
    
    try:
        item_name = item.item_name
        db.session.delete(item)
        db.session.commit()
        
        flash(f'Item "{item_name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the item. Please try again.', 'danger')
        print(f"Delete item error: {str(e)}")
    
    return redirect(url_for('inventory.index'))


@inventory_bp.route('/view/<int:item_id>')
@login_required
def view(item_id):
    """View inventory item details"""
    
    # Get item
    item = InventoryItem.query.get_or_404(item_id)
    
    # Check ownership
    if item.created_by != current_user.id:
        flash('You do not have permission to view this item.', 'danger')
        return redirect(url_for('inventory.index'))
    
    # Get recent transactions
    transactions = StockTransaction.query.filter_by(
        item_id=item.id
    ).order_by(StockTransaction.transaction_date.desc()).limit(10).all()
    
    return render_template('dashboard/inventory_view.html',
                         item=item,
                         transactions=transactions)
