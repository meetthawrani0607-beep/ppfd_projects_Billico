# 🚀 BILLICO - QUICK START GUIDE

## ⚡ Get Started in 5 Minutes

### Step 1: Install Tesseract OCR (2 minutes)

**Windows:**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (default location: C:\Program Files\Tesseract-OCR)
3. ✅ Done!

**Linux:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

---

### Step 2: Setup MySQL Database (1 minute)

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE billico;
EXIT;
```

---

### Step 3: Configure Environment (1 minute)

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env    # Windows
   ```

2. Edit `.env` and update your MySQL password:
   ```env
   DB_PASSWORD=your_mysql_password_here
   ```

3. **Windows users**: Verify Tesseract path is correct:
   ```env
   TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe
   ```

---

### Step 4: Install and Run (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
flask db-init

# Run the application
python app.py
```

---

### Step 5: Access Application (30 seconds)

1. Open browser
2. Go to: **http://localhost:5000**
3. Click "Sign up now"
4. Create your account
5. 🎉 **You're in!**

---

## ✅ VERIFICATION CHECKLIST

After setup, verify everything works:

- [ ] Can access http://localhost:5000
- [ ] Can register a new account
- [ ] Can login successfully
- [ ] Dashboard loads correctly
- [  ] Can add an inventory item manually
- [ ] Can upload a bill image
- [ ] OCR processes the image
- [ ] Charts display correctly

---

## 📝 TEST WITH SAMPLE DATA

### Add Your First Item Manually:
1. Go to **Inventory** → **Add Item**
2. Fill in:
   - Item Name: Rice
   - Quantity: 100
   - Unit Price: 50
   - Category: Groceries
3. Click **Submit**

### Upload Your First Bill:
1. Create a simple bill image with your phone or use this text:
   ```
   SAMPLE STORE
   Invoice: INV-001
   Date: 15/01/2026
   
   Rice         10    50.00    500.00
   Sugar        5     45.00    225.00
   
   Total: 725.00
   ```
2. Take a screenshot or photo of this
3. Go to **Upload Bill**
4. Upload the image
5. Wait for processing
6. Review extracted data
7. Click **Confirm & Add to Inventory**

---

## 🆘 COMMON ISSUES & QUICK FIXES

### Issue: "Tesseract not found"
**Fix:** Update TESSERACT_PATH in `.env` file

### Issue: "Can't connect to MySQL"
**Fix:** 
1. Check MySQL is running
2. Verify DB_PASSWORD in `.env`
3. Ensure database 'billico' exists

### Issue: "Module not found"
**Fix:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate    # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Fix:**
```bash
# Use different port
flask run --port 5001
```

---

## 📚 NEXT STEPS

Once running:

1. **Explore the Dashboard** - See your inventory stats
2. **Add Items** - Manually or via bill upload
3. **Check Analytics** - View your charts
4. **Test OCR** - Upload different bill formats
5. **Manage Inventory** - Edit, delete, search items

---

## 📖 FULL DOCUMENTATION

- **Complete Setup**: See `SETUP_GUIDE.md`
- **API Reference**: See `API_DOCUMENTATION.md`
- **Project Details**: See `README.md`
- **Full Summary**: See `PROJECT_SUMMARY.md`

---

## 🎯 DEFAULT CREDENTIALS

After first installation, create your own account at:
**http://localhost:5000/auth/register**

Or use Flask CLI to create admin:
```bash
flask create-admin
```

---

## 🎉 YOU'RE READY!

If you can:
✅ See the dashboard  
✅ Add an item  
✅ Upload a bill  
✅ See charts  

**Congratulations! Billico is working perfectly!** 🚀

---

**Need Help?** Check `SETUP_GUIDE.md` for detailed troubleshooting.

---

*Built for efficiency. Designed for simplicity.*
