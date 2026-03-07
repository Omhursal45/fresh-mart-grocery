# Grocery Delivery App - Setup Guide

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation

#### 1. Navigate to Project Directory
```bash
cd DjangoPract
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Create Admin Superuser
```bash
python manage.py createsuperuser
```
Enter username, email (optional), and password when prompted.

#### 6. Create Static Files Directory (if needed)
```bash
mkdir static
mkdir media
```

#### 7. Run Development Server
```bash
python manage.py runserver
```

#### 8. Access the Application
- **Web App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Initial Setup in Admin Panel

After logging into the admin panel, you should:

1. **Create Categories**
   - Go to Categories
   - Add categories like: Fruits, Vegetables, Dairy, Bakery, etc.

2. **Add Products**
   - Go to Products
   - Add products with images, prices, stock, and assign categories

3. **Create Coupons (Optional)**
   - Go to Coupons
   - Create discount coupons with codes, discount types, and validity dates

4. **Set Up Delivery Slots**
   - Go to Delivery Slots
   - Create available delivery time slots
   - *Alternatively* you can run the helper command used for seeding demo data:
     ```bash
     python manage.py populate_products
     ```
     which will also create slots for the next 7 days.
   - The application now automatically generates a fresh batch of slots when a
     customer reaches checkout and no active slots exist, so this step is only
     required once or when you want to customise the times.

## Testing the Application

1. **Sign Up**: Create a new user account
2. **Browse Products**: View products by category or search
3. **Add to Cart**: Add products to shopping cart
4. **Add Address**: Go to Profile and add a delivery address
5. **Checkout**: Complete an order with address and delivery slot selection
6. **View Orders**: Check order history and tracking

## API Testing

You can test the REST API using:
- Browser (for GET requests)
- Postman
- curl commands
- JavaScript fetch API

### Example API Calls

```bash
# Search products
GET http://127.0.0.1:8000/api/search/?q=rice

# Get cart
GET http://127.0.0.1:8000/api/cart/
(Requires authentication)

# Add to cart
POST http://127.0.0.1:8000/api/cart/
{
    "product_id": 1,
    "quantity": 2
}

# Get order status
GET http://127.0.0.1:8000/api/orders/1/status/

# Validate coupon
POST http://127.0.0.1:8000/api/coupons/validate/
{
    "code": "SAVE10",
    "cart_total": 1000
}
```

## Troubleshooting

### Issue: "No module named 'django'"
**Solution**: Make sure virtual environment is activated and dependencies are installed.

### Issue: "Table doesn't exist"
**Solution**: Run migrations: `python manage.py migrate`

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic` (for production) or ensure DEBUG=True in settings.

### Issue: Images not displaying
**Solution**: 
- Ensure `media/` directory exists
- Check MEDIA_URL and MEDIA_ROOT in settings.py
- Verify image files are uploaded correctly

### Issue: CSRF token errors
**Solution**: Ensure CSRF middleware is enabled and forms include `{% csrf_token %}`

## Production Deployment Notes

Before deploying to production:

1. Change `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Configure proper database (PostgreSQL recommended)
4. Set up proper static file serving
5. Configure ALLOWED_HOSTS
6. Use environment variables for sensitive data
7. Set up SSL/HTTPS
8. Configure proper media file storage

## Project Structure

```
DjangoPract/
├── manage.py
├── requirements.txt
├── README.md
├── SETUP.md
├── grocery_delivery/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── grocery/                   # Main app
│   ├── models.py             # Database models
│   ├── views.py              # Web views
│   ├── api_views.py          # REST API views
│   ├── serializers.py        # DRF serializers
│   ├── urls.py               # Web URLs
│   ├── api_urls.py           # API URLs
│   └── admin.py              # Admin configuration
├── templates/                # HTML templates
│   ├── base.html
│   └── grocery/
├── static/                    # Static files (CSS, JS, images)
└── media/                    # User uploaded files
```

## Support

For issues or questions, refer to:
- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Bootstrap Documentation: https://getbootstrap.com/docs/5.3/

