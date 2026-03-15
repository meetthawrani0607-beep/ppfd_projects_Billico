# BILLICO - SETUP & DEPLOYMENT GUIDE

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, Linux, or macOS
- **Python**: 3.8 or higher
- **MySQL**: 5.7 or higher
- **Tesseract OCR**: Latest version
- **Memory**: At least 4GB RAM
- **Storage**: At least 2GB free space

### Software to Install

#### 1. Python 3.8+
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt-get install python3 python3-pip`
- **macOS**: `brew install python3`

#### 2. MySQL Server
- **Windows**: Download from [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
- **Linux**: `sudo apt-get install mysql-server`
- **macOS**: `brew install mysql`

#### 3. Tesseract OCR

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer
3. Default installation path: `C:\Program Files\Tesseract-OCR`
4. Add to System PATH:
   - Right-click "This PC" → Properties → Advanced System Settings
   - Environment Variables → System Variables → Path → Edit
   - Add: `C:\Program Files\Tesseract-OCR`
   - Click OK

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
```

**macOS:**
```bash
brew install tesseract
```

**Verify Installation:**
```bash
tesseract --version
```

---

## Installation Steps

### Step 1: Clone or Navigate to Project

```bash
cd d:/Billico
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If you encounter any errors, try installing packages individually:
```bash
pip install Flask==2.3.3
pip install Flask-SQLAlchemy==3.0.5
pip install Flask-Login==0.6.2
pip install Flask-Bcrypt==1.0.1
pip install PyMySQL==1.1.0
pip install pytesseract==0.3.10
pip install opencv-python==4.8.0.76
pip install Pillow==10.0.0
pip install python-dotenv==1.0.0
```

---

## Configuration

### Step 1: Create Environment File

Copy the example environment file:
```bash
copy .env.example .env     # Windows
cp .env.example .env       # Linux/macOS
```

### Step 2: Edit Configuration

Open `.env` file and update the following:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development        # Use 'production' in production
SECRET_KEY=your-super-secret-key-change-this-in-production

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=billico
DB_USER=root
DB_PASSWORD=your_mysql_password_here

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_FILE_SIZE=16777216

# Tesseract OCR Configuration (Windows)
TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe

# Tesseract OCR Configuration (Linux/macOS)
# TESSERACT_PATH=/usr/bin/tesseract
```

### Important Configuration Notes:

1. **SECRET_KEY**: Generate a strong random key:
   ```python
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the output and paste it as SECRET_KEY value.

2. **DB_PASSWORD**: Replace with your actual MySQL root password.

3. **TESSERACT_PATH**: 
   - Windows: Usually `C:\\Program Files\\Tesseract-OCR\\tesseract.exe`
   - Linux: Usually `/usr/bin/tesseract`
   - macOS: Usually `/usr/local/bin/tesseract`

---

## Database Setup

### Step 1: Start MySQL Server

**Windows:**
- MySQL should auto-start. If not, start via Services or:
  ```bash
  net start MySQL80
  ```

**Linux:**
```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

**macOS:**
```bash
brew services start mysql
```

### Step 2: Create Database

Login to MySQL:
```bash
mysql -u root -p
```

Enter your MySQL root password, then run:
```sql
CREATE DATABASE billico CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### Step 3: Import Schema

**Option A: Using MySQL Command Line**
```bash
mysql -u root -p billico < database/schema.sql
```

**Option B: Using Flask CLI** (Recommended)
```bash
# Make sure virtual environment is activated
flask db-init
```

This will:
- Create all necessary tables
- Set up foreign keys and indexes
- Create default categories
- Set up triggers

### Step 4: Verify Database

Login to MySQL and verify:
```bash
mysql -u root -p billico
```

```sql
SHOW TABLES;
```

You should see 8 tables:
- users
- categories
- suppliers
- inventory_items
- stock_transactions
- upload_logs
- alerts

---

## Running the Application

### Step 1: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### Step 2: Run the Application

**Development Server:**
```bash
python app.py
```

**Or using Flask CLI:**
```bash
flask run
```

The application will start on: **http://localhost:5000**

### Step 3: Access the Application

1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. You'll be redirected to the login page
4. Click "Sign up now" to create an account

### Step 4: Create First User

**Option A: Through Web Interface**
1. Go to `http://localhost:5000/auth/register`
2. Fill in the registration form
3. Click "Create Account"
4. Login with your credentials

**Option B: Using CLI**
```bash
flask create-admin
```

Enter the required information when prompted.

---

## Testing the Application

### 1. User Registration & Login
- Register a new account
- Login with the account
- Verify redirect to dashboard

### 2. Manual Inventory Entry
- Go to Inventory → Add Item
- Fill in item details
- Submit and verify in inventory list

### 3. Bill Upload & OCR
- Prepare a clear bill/receipt image (JPG or PNG)
- Go to Upload Bill
- Upload the image
- Wait for processing
- Review extracted data
- Confirm and add to inventory

### 4. Dashboard & Analytics
- View dashboard statistics
- Check low stock alerts
- View analytics charts
- Verify data accuracy

### 5. Test OCR with Sample Bill

Create a sample bill image with this text:
```
ABC STORE
Invoice #: INV-001
Date: 15/01/2026

Item Name        Qty    Price    Total
Rice             10     50.00    500.00
Sugar            5      45.00    225.00
Oil              2      150.00   300.00

Total Amount: 1025.00
```

---

## Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production` in `.env`
- [ ] Generate strong `SECRET_KEY`
- [ ] Use production database (not development)
- [ ] Set up MySQL user with limited privileges
- [ ] Configure firewall rules
- [ ] Set up HTTPS/SSL
- [ ] Configure proper logging
- [ ] Set up backup system
- [ ] Configure max file upload size
- [ ] Set up monitoring and alerts

### Deployment Options

#### 1. **Heroku** (Easy)
```bash
# Install Heroku CLI
heroku login
heroku create billico-app
git push heroku main
```

#### 2. **AWS EC2** (Full Control)
- Launch EC2 instance (Ubuntu)
- Install dependencies
- Configure Nginx/Apache
- Set up Gunicorn
- Configure SSL with Let's Encrypt

#### 3. **DigitalOcean** (Simple)
- Create a Droplet
- Follow deployment guide
- Use App Platform for easier deployment

#### 4. **PythonAnywhere** (Beginner-Friendly)
- Upload files
- Configure MySQL database
- Set up WSGI file
- Configure static files

### Using Gunicorn (Production Server)

Install Gunicorn:
```bash
pip install gunicorn
```

Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Troubleshooting

### Issue: Tesseract Not Found

**Error:** `TesseractNotFoundError: tesseract is not installed`

**Solution:**
1. Verify Tesseract is installed: `tesseract --version`
2. Check TESSERACT_PATH in `.env` is correct
3. On Windows, ensure the path uses double backslashes: `C:\\Program Files\\Tesseract-OCR\\tesseract.exe`

### Issue: MySQL Connection Failed

**Error:** `Can't connect to MySQL server`

**Solution:**
1. Verify MySQL is running
2. Check DB_HOST, DB_PORT, DB_USER, DB_PASSWORD in `.env`
3. Ensure database `billico` exists
4. Check MySQL user has proper permissions

### Issue: Import Errors

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
1. Activate virtual environment
2. Reinstall requirements: `pip install -r requirements.txt`

### Issue: OCR Not Extracting Text

**Possible Causes:**
1. Image quality is poor
2. Image is too large or small
3. Text is not clear

**Solutions:**
1. Use clear, high-resolution images
2. Ensure good lighting when taking photo
3. Avoid shadows and glare
4. Keep text straight (not tilted)

### Issue: Database Migration Errors

**Solution:**
```bash
# Drop and recreate database
mysql -u root -p -e "DROP DATABASE billico; CREATE DATABASE billico;"
flask db-init
```

### Issue: Port 5000 Already in Use

**Solution:**
```bash
# Run on different port
flask run --port 5001
```

Or in `app.py`, change:
```python
app.run(port=5001)
```

---

## Additional Resources

### Useful Commands

```bash
# Create admin user
flask create-admin

# Reset database
flask db-init

# Run with debug mode
flask run --debug

# Check Python version
python --version

# Check pip packages
pip list

# Freeze requirements
pip freeze > requirements.txt
```

### File Permissions

Ensure the `static/uploads` directory is writable:

**Linux/macOS:**
```bash
chmod 755 static/uploads
```

**Windows:** (Usually not needed)

### Database Backup

```bash
# Backup database
mysqldump -u root -p billico > backup.sql

# Restore database
mysql -u root -p billico < backup.sql
```

---

## Need Help?

If you encounter any issues:

1. Check this troubleshooting guide
2. Review error messages carefully
3. Check the console/terminal logs
4. Verify all prerequisites are installed
5. Ensure configuration is correct

---

## Success! 🎉

If you can:
- ✅ Access the application at http://localhost:5000
- ✅ Register and login
- ✅ Add inventory items
- ✅ Upload and process bills
- ✅ View dashboard and analytics

**Your Billico installation is complete and working!**

---

**Built with ❤️ for efficient inventory management**
