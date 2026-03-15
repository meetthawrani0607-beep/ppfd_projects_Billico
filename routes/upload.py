"""
Upload Routes
Handle bill/receipt uploads and OCR processing
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models import db
from models.upload_log import UploadLog
from models.inventory import InventoryItem
from models.supplier import Supplier
from services.ocr_service import OCRService
from services.ai_parser import AIParser
from utils.validators import is_allowed_file, sanitize_filename
from utils.helpers import generate_unique_filename, make_dir_if_not_exists
from datetime import datetime

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')


@upload_bp.route('/')
@login_required
def index():
    """Upload page"""
    return render_template('upload/bill_upload.html')


@upload_bp.route('/process', methods=['POST'])
@login_required
def process():
    """Process uploaded bill/receipt"""
    
    # Check if file was uploaded
    if 'bill_file' not in request.files:
        flash('No file uploaded', 'danger')
        return redirect(url_for('upload.index'))
    
    file = request.files['bill_file']
    
    # Check if file is selected
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('upload.index'))
    
    # Validate file extension
    if not is_allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        flash('Invalid file type. Allowed types: PNG, JPG, JPEG, PDF', 'danger')
        return redirect(url_for('upload.index'))
    
    try:
        # Create upload directory if not exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        make_dir_if_not_exists(upload_folder)
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        file_path = os.path.join(upload_folder, unique_filename)
        
        # Save file
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        # Create upload log
        upload_log = UploadLog(
            user_id=current_user.id,
            filename=unique_filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file.content_type
        )
        
        db.session.add(upload_log)
        db.session.commit()
        
        # Process with OCR
        upload_log.mark_processing()
        
        # Initialize OCR service
        ocr_service = OCRService(tesseract_path=current_app.config['TESSERACT_PATH'])
        
        # Check if Tesseract is available
        if not ocr_service.is_tesseract_available():
            upload_log.mark_failed("Tesseract OCR is not properly configured")
            flash('OCR service is not available. Please contact administrator.', 'danger')
            return redirect(url_for('upload.history'))
        
        # Extract text from image
        ocr_result = ocr_service.extract_text(file_path, preprocess=True)
        
        if not ocr_result['success']:
            upload_log.mark_failed(ocr_result.get('error', 'OCR failed'))
            flash('Failed to extract text from image. Please try with a clearer image.', 'danger')
            return redirect(url_for('upload.history'))
        
        # Save OCR text and confidence
        upload_log.ocr_text = ocr_result['text']
        upload_log.ocr_confidence = ocr_result['confidence']
        
        # Parse extracted text
        parser = AIParser()
        parsed_data = parser.parse_bill(ocr_result['text'])
        
        # Validate and enrich items
        items = parser.validate_and_enrich_items(parsed_data.get('items', []))
        
        if not items:
            upload_log.mark_failed("No items could be extracted from the bill")
            flash('Could not extract any items from the bill. Please try manual entry.', 'warning')
            return redirect(url_for('upload.review', upload_id=upload_log.id))
        
        # Update parsed data with enriched items
        parsed_data['items'] = items
        
        # Save parsed data
        upload_log.set_extracted_data(parsed_data)
        upload_log.bill_number = parsed_data.get('bill_number')
        upload_log.bill_date = parsed_data.get('bill_date')
        upload_log.supplier_name = parsed_data.get('supplier_name')
        upload_log.total_amount = parsed_data.get('total_amount')
        
        upload_log.mark_completed()
        
        flash(f'Successfully extracted {len(items)} items from the bill!', 'success')
        return redirect(url_for('upload.review', upload_id=upload_log.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while processing the file: {str(e)}', 'danger')
        print(f"Upload error: {str(e)}")
        return redirect(url_for('upload.index'))


@upload_bp.route('/review/<int:upload_id>')
@login_required
def review(upload_id):
    """Review extracted data before adding to inventory"""
    
    # Get upload log
    upload_log = UploadLog.query.get_or_404(upload_id)
    
    # Check ownership
    if upload_log.user_id != current_user.id:
        flash('You do not have permission to view this upload.', 'danger')
        return redirect(url_for('upload.history'))
    
    # Get extracted data
    extracted_data = upload_log.get_extracted_data()
    
    # Get categories and suppliers for dropdowns
    from models.category import Category
    categories = Category.query.all()
    suppliers = Supplier.query.all()
    
    return render_template('upload/review.html',
                         upload_log=upload_log,
                         extracted_data=extracted_data,
                         categories=categories,
                         suppliers=suppliers)


@upload_bp.route('/confirm/<int:upload_id>', methods=['POST'])
@login_required
def confirm(upload_id):
    """Confirm and add extracted items to inventory"""
    
    # Get upload log
    upload_log = UploadLog.query.get_or_404(upload_id)
    
    # Check ownership
    if upload_log.user_id != current_user.id:
        flash('You do not have permission to confirm this upload.', 'danger')
        return redirect(url_for('upload.history'))
    
    try:
        # Get form data (items to add)
        items_data = request.form.getlist('items')
        
        if not items_data:
            flash('No items selected to add', 'warning')
            return redirect(url_for('upload.review', upload_id=upload_id))
        
        items_added = 0
        
        # Get extracted data
        extracted_data = upload_log.get_extracted_data()
        extracted_items = extracted_data.get('items', [])
        
        # Process each selected item
        for item_index in items_data:
            idx = int(item_index)
            
            if idx < 0 or idx >= len(extracted_items):
                continue
            
            item_data = extracted_items[idx]
            
            # Get item details from form
            item_name = request.form.get(f'item_name_{idx}', item_data.get('item_name', ''))
            quantity = int(request.form.get(f'quantity_{idx}', item_data.get('quantity', 1)))
            unit_price = float(request.form.get(f'unit_price_{idx}', item_data.get('unit_price', 0)))
            category_id = request.form.get(f'category_{idx}')
            supplier_id = request.form.get(f'supplier_{idx}')
            
            if not item_name:
                continue
            
            # Check if item already exists (by name)
            existing_item = InventoryItem.query.filter(
                InventoryItem.created_by == current_user.id,
                InventoryItem.item_name.ilike(item_name)
            ).first()
            
            if existing_item:
                # Update existing item (add stock)
                existing_item.add_stock(
                    quantity=quantity,
                    unit_price=unit_price,
                    created_by=current_user.id,
                    reference=upload_log.bill_number,
                    notes=f'Added from bill upload: {upload_log.original_filename}'
                )
            else:
                # Create new item
                new_item = InventoryItem(
                    item_name=item_name,
                    quantity=quantity,
                    unit_price=unit_price,
                    category_id=int(category_id) if category_id else None,
                    supplier_id=int(supplier_id) if supplier_id else None
                )
                new_item.created_by = current_user.id
                new_item.updated_by = current_user.id
                
                db.session.add(new_item)
            
            items_added += 1
        
        # Update upload log
        upload_log.items_added = items_added
        
        db.session.commit()
        
        flash(f'Successfully added/updated {items_added} items to inventory!', 'success')
        return redirect(url_for('dashboard.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while adding items: {str(e)}', 'danger')
        print(f"Confirm error: {str(e)}")
        return redirect(url_for('upload.review', upload_id=upload_id))


@upload_bp.route('/history')
@login_required
def history():
    """View upload history"""
    
    # Get all uploads for current user
    uploads = UploadLog.query.filter_by(
        user_id=current_user.id
    ).order_by(UploadLog.upload_time.desc()).all()
    
    return render_template('upload/history.html', uploads=uploads)
