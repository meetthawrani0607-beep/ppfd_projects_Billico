# Billico - Smart Inventory Automation Platform

![Billico Logo](static/images/logo.png)

## 📋 Overview

Billico is a production-ready inventory management web application that automates stock handling using bill/receipt image uploads, OCR, and AI. It converts physical bills into structured digital inventory automatically and provides insights through a modern analytics dashboard.

## 🎯 Problem Statement

Manual inventory management is time-consuming, error-prone, and inefficient for small and large businesses. Paper bills are hard to track and stock levels are often mismanaged.

## ✨ Solution

A smart inventory system that converts physical bills into structured digital inventory automatically and displays insights through a modern dashboard.

---

## 🛠️ Tech Stack

### Frontend
- **HTML5** - Structure
- **Bootstrap 5** - Responsive UI framework
- **Custom CSS** - Premium styling
- **Vanilla JavaScript** - Interactive functionality
- **Chart.js** - Analytics visualization

### Backend
- **Python 3.8+** - Core language
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM
- **Flask-Login** - Authentication
- **Flask-Bcrypt** - Password hashing
- **Flask-CORS** - Cross-origin support

### Database
- **MySQL** - Relational database
- **Properly indexed schema**
- **Normalized structure**

### OCR & AI
- **Tesseract OCR** - Text extraction
- **OpenCV** - Image preprocessing
- **Pillow** - Image handling
- **Custom AI logic** - Data parsing and mapping

---

## 🎨 Core Features

### 1. **Authentication System**
- User registration with validation
- Secure login/logout
- Password hashing (bcrypt)
- Session-based authentication
- Protected routes

### 2. **Bill/Receipt Upload**
- Multi-format support (JPG, PNG, PDF)
- Image preview before upload
- Secure file handling
- OCR processing pipeline:
  - Image cleanup and preprocessing
  - Text extraction with Tesseract
  - Intelligent data parsing
  - Structured data extraction

### 3. **Auto Data Extraction**
Extracts and structures:
- Item name
- Quantity
- Unit price
- Total amount
- Supplier name
- Bill date
- Bill number

### 4. **Inventory Logic**
- Auto-update stock if item exists
- Insert new items automatically
- Handle duplicate items intelligently
- Maintain complete stock history
- Transaction logging

### 5. **Dashboard**
- Total inventory items count
- Current stock levels overview
- Low stock alerts (color-coded)
- Items needing refill
- Recently updated items
- Quick statistics cards

### 6. **Analytics & Graphs**
- **Stock trend line chart** - Track inventory over time
- **Category-wise bar chart** - Stock distribution
- **Stock health pie chart** - Low vs healthy stock
- **Interactive charts** using Chart.js
- Real-time data updates

### 7. **Inventory Management**
- Add items manually
- Edit existing items
- Delete items with confirmation
- Set reorder threshold per item
- Search functionality
- Filter by category/status
- Sort by various fields
- Bulk operations

### 8. **Alerts & Status**
Color-coded stock status:
- 🔴 **Red**: Low stock (below threshold)
- 🟡 **Yellow**: Medium stock (near threshold)
- 🟢 **Green**: Healthy stock (above threshold)
- Visual alerts on dashboard
- Badge indicators

---

## 📂 Project Structure

```
Billico/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── models/
│   ├── __init__.py
│   ├── user.py                 # User model
│   ├── inventory.py            # Inventory item model
│   ├── supplier.py             # Supplier model
│   ├── transaction.py          # Stock transaction model
│   └── upload_log.py           # Upload log model
│
├── routes/
│   ├── __init__.py
│   ├── auth.py                 # Authentication routes
│   ├── dashboard.py            # Dashboard routes
│   ├── inventory.py            # Inventory management routes
│   ├── upload.py               # Bill upload routes
│   └── api.py                  # RESTful API endpoints
│
├── services/
│   ├── __init__.py
│   ├── ocr_service.py          # OCR processing logic
│   ├── image_service.py        # Image preprocessing
│   └── ai_parser.py            # AI data parsing logic
│
├── utils/
│   ├── __init__.py
│   ├── validators.py           # Input validation
│   ├── helpers.py              # Helper functions
│   └── decorators.py           # Custom decorators
│
├── static/
│   ├── css/
│   │   ├── main.css            # Main stylesheet
│   │   ├── dashboard.css       # Dashboard styles
│   │   └── auth.css            # Auth pages styles
│   ├── js/
│   │   ├── main.js             # Main JavaScript
│   │   ├── dashboard.js        # Dashboard functionality
│   │   ├── charts.js           # Chart configurations
│   │   └── upload.js           # Upload functionality
│   ├── images/
│   │   └── logo.png            # Logo and assets
│   └── uploads/                # Uploaded bills storage
│
├── templates/
│   ├── base.html               # Base template
│   ├── auth/
│   │   ├── login.html          # Login page
│   │   └── register.html       # Registration page
│   ├── dashboard/
│   │   ├── index.html          # Main dashboard
│   │   ├── analytics.html      # Analytics page
│   │   └── inventory.html      # Inventory management
│   ├── upload/
│   │   └── bill_upload.html    # Bill upload page
│   └── components/
│       ├── navbar.html         # Navigation bar
│       ├── sidebar.html        # Sidebar navigation
│       └── alerts.html         # Alert components
│
├── database/
│   └── schema.sql              # Database schema
│
└── tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_ocr.py
    └── test_inventory.py
```

---

## 🗄️ Database Schema

### Tables:
1. **users** - User accounts
2. **inventory_items** - Product inventory
3. **suppliers** - Supplier information
4. **stock_transactions** - Stock movement history
5. **upload_logs** - Bill upload tracking

See `database/schema.sql` for complete schema with:
- Primary keys
- Foreign keys
- Indexes
- Constraints
- Relationships

---

## 🔐 Security Features

- ✅ Password hashing with bcrypt
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Input validation and sanitization
- ✅ Secure session management
- ✅ CSRF protection
- ✅ File upload validation
- ✅ Error handling and logging
- ✅ Protected API endpoints

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/user` - Get current user

### Inventory
- `GET /api/inventory` - Get all items
- `GET /api/inventory/<id>` - Get single item
- `POST /api/inventory` - Create item
- `PUT /api/inventory/<id>` - Update item
- `DELETE /api/inventory/<id>` - Delete item

### Upload
- `POST /api/upload/bill` - Upload and process bill
- `GET /api/upload/history` - Get upload history
- `GET /api/upload/status/<id>` - Check processing status

### Analytics
- `GET /api/analytics/stats` - Dashboard statistics
- `GET /api/analytics/trends` - Stock trends
- `GET /api/analytics/low-stock` - Low stock items

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server 5.7 or higher
- Tesseract OCR installed on system

### Step 1: Install Tesseract OCR

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to `C:\Program Files\Tesseract-OCR`
3. Add to PATH: `C:\Program Files\Tesseract-OCR`

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract
```

### Step 2: Clone and Setup

```bash
# Navigate to project directory
cd d:/Billico

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Database Setup

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE billico;

# Import schema
mysql -u root -p billico < database/schema.sql

# Or use the Flask CLI
flask db-init
```

### Step 4: Configuration

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=billico
DB_USER=root
DB_PASSWORD=your-mysql-password

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_FILE_SIZE=16777216  # 16MB

# Tesseract Configuration
TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe  # Windows
# TESSERACT_PATH=/usr/bin/tesseract  # Linux/Mac
```

### Step 5: Run the Application

```bash
# Initialize database (first time only)
flask db-init

# Run the development server
python app.py

# Or use Flask CLI
flask run
```

The application will be available at: **http://localhost:5000**

---

## 📖 Usage Guide

### 1. Registration & Login
1. Navigate to `/register`
2. Create an account with email and password
3. Login at `/login`

### 2. Upload a Bill
1. Go to **Upload Bill** page
2. Select an image (JPG, PNG) or PDF
3. Preview the image
4. Click **Upload & Process**
5. Wait for OCR processing
6. Review extracted data
7. Confirm or edit before saving

### 3. View Dashboard
- See total items, stock quantity, and alerts
- View recent updates
- Check low stock warnings
- Quick access to key metrics

### 4. Analytics
- View stock trends over time
- Category distribution
- Stock health status
- Interactive charts

### 5. Manage Inventory
- Search and filter items
- Add/edit/delete manually
- Set reorder thresholds
- Bulk operations

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=./ --cov-report=html
```

---

## 📦 Deployment

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up logging
- [ ] Enable error monitoring
- [ ] Configure file upload limits
- [ ] Set up backup system
- [ ] Configure firewall rules

### Deployment Options
- **Heroku** - Easy deployment
- **AWS EC2** - Full control
- **DigitalOcean** - Simple setup
- **Google Cloud Platform** - Scalable
- **Azure** - Enterprise ready

---

## 🎯 Future Enhancements

- [ ] Multi-user roles (Admin, Manager, User)
- [ ] Export reports (PDF, Excel)
- [ ] Email notifications for low stock
- [ ] Barcode scanning support
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Supplier portal
- [ ] Purchase order management
- [ ] Integration with accounting software
- [ ] Advanced AI predictions
- [ ] Real-time collaboration
- [ ] API rate limiting
- [ ] Webhook support

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Billico Development Team**
- Built as a production-ready SaaS MVP
- Designed for scalability and maintainability

---

## 📞 Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Email: support@billico.app (placeholder)

---

## 🙏 Acknowledgments

- Tesseract OCR Team
- Flask Community
- Bootstrap Team
- Chart.js Maintainers

---

**Built with ❤️ for efficient inventory management**
