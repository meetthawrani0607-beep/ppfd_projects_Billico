"""
Authentication Routes
Handle user registration, login, and logout
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from models import db
from models.user import User
from utils.validators import is_valid_email, is_valid_username, is_valid_password, clean_text

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        # Get form data
        username = clean_text(request.form.get('username', ''))
        email = clean_text(request.form.get('email', ''))
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        full_name = clean_text(request.form.get('full_name', ''))
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required')
        elif not is_valid_username(username):
            errors.append('Username must be 3-80 characters and contain only letters, numbers, and underscores')
        
        if not email:
            errors.append('Email is required')
        elif not is_valid_email(email):
            errors.append('Please enter a valid email address')
        
        if not password:
            errors.append('Password is required')
        else:
            is_valid, msg = is_valid_password(password)
            if not is_valid:
                errors.append(msg)
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        # If errors, show them
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')
        
        # Create new user
        try:
            user = User(
                username=username,
                email=email,
                password=password,
                full_name=full_name if full_name else None
            )
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            print(f"Registration error: {str(e)}")
    
    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        # Get form data
        username_or_email = clean_text(request.form.get('username', ''))
        password = request.form.get('password', '')
        remember = request.form.get('remember', False) == 'on'
        
        # Validation
        if not username_or_email or not password:
            flash('Please enter both username/email and password', 'danger')
            return render_template('auth/login.html')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | 
            (User.email == username_or_email)
        ).first()
        
        # Check credentials
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account is inactive. Please contact support.', 'danger')
                return render_template('auth/login.html')
            
            # Login user
            login_user(user, remember=remember)
            user.update_last_login()
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username/email or password', 'danger')
    
    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('auth.login'))
