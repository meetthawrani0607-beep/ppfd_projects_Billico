# BILLICO - API DOCUMENTATION

## Base URL
```
http://localhost:5000/api
```

---

## Authentication
All API endpoints require authentication. Use session-based authentication (login via web interface).

---

## Endpoints

### Inventory

#### Get All Inventory Items
```http
GET /api/inventory
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "item_name": "Rice",
      "quantity": 100,
      "unit_price": 50.00,
      "stock_status": "healthy",
      "category_name": "Groceries",
      "supplier_name": "ABC Wholesale"
    }
  ]
}
```

#### Get Single Item
```http
GET /api/inventory/<item_id>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "item_name": "Rice",
    "quantity": 100,
    "unit_price": 50.00
  }
}
```

---

### Analytics

#### Get Dashboard Statistics
```http
GET /api/analytics/stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_items": 50,
    "total_quantity": 1500,
    "total_value": 75000.00,
    "stock_status": {
      "healthy": 30,
      "medium": 10,
      "low": 8,
      "out_of_stock": 2
    }
  }
}
```

#### Get Stock Trends
```http
GET /api/analytics/trends
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "date": "2026-01-10",
      "count": 5,
      "total_change": 50
    }
  ]
}
```

#### Get Low Stock Items
```http
GET /api/analytics/low-stock
```

#### Get Category Distribution
```http
GET /api/analytics/category-distribution
```

#### Get Stock Health
```http
GET /api/analytics/stock-health
```

---

### Alerts

#### Get Alerts
```http
GET /api/alerts?unread=true
```

**Query Parameters:**
- `unread` (optional): Filter unread alerts only

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Low Stock: Rice",
      "message": "Rice is running low",
      "severity": "warning",
      "is_read": false
    }
  ]
}
```

#### Mark Alert as Read
```http
POST /api/alerts/<alert_id>/read
```

---

### Upload

#### Get Upload Status
```http
GET /api/upload/status/<upload_id>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "filename": "bill.jpg",
    "ocr_status": "completed",
    "items_extracted": 5,
    "items_added": 5
  }
}
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message here"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `401` - Unauthorized (not logged in)
- `403` - Forbidden (no permission)
- `404` - Not Found
- `500` - Internal Server Error

---

## Usage Examples

### JavaScript (Fetch API)
```javascript
// Get inventory
const response = await fetch('/api/inventory');
const data = await response.json();

if (data.success) {
    console.log(data.data);
}
```

### Python (Requests)
```python
import requests

# Login first to get session
session = requests.Session()
session.post('http://localhost:5000/auth/login', data={
    'username': 'admin',
    'password': 'password'
})

# Get inventory
response = session.get('http://localhost:5000/api/inventory')
data = response.json()
print(data)
```

---

Built for Billico - Smart Inventory Automation Platform
