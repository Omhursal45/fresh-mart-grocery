# Fresh Mart 🥬

Fresh Mart is a **grocery delivery web application** built with Django. It provides a complete
online shopping experience where users can browse products, add items to cart, checkout with
coupons and delivery slot selection, and track orders — all through a modern responsive UI and
well‑documented REST API.

> 🚧 This project is actively maintained. New features and enhancements are added frequently.

---

## 🚀 Key Features

- **Product Catalog** – 34 products across 8 categories with images, pricing, and stock details.
- **Search & Filtering** – Search by keywords and view products by category.
- **Shopping Cart** – Add/remove items, update quantities, view real‑time totals.
- **User Accounts** – Registration, login, profile editing (including avatar upload).
- **Wishlist** – Save products for later and move them to cart with one click.
- **Checkout Flow** – Address management, delivery slot selection (morning/evening), coupon
  validation, and order creation.
- **Order Tracking** – View order history with status updates (placed, packed, out for delivery,
  delivered, cancelled).
- **Coupons & Discounts** – Percentage and fixed‑amount coupons with validation logic.
- **Delivery Slots** – Automatic generation of slots for the next 7 days with availability
  limits.
- **REST API** – Fully functional API for products, cart, orders, addresses, coupons, delivery
  slots, and wishlist (see `API_REFERENCE.md`).

## 🛠 Tech Stack

- **Backend:** Django, Django REST Framework, SQLite (development), compatible with PostgreSQL
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (jQuery for interactivity)
- **Deployment:** WSGI, static/media handling with Django settings

## 📁 Project Structure

```
FreshMart/
├── grocery/                      # main Django app
│   ├── models/                   # data models (category, product, cart, etc.)
│   ├── views/                    # web view logic
│   ├── api_views.py             # REST API endpoints
│   ├── serializers.py           # DRF serializers
│   ├── urls/                    # URL routing (separate web/api)
│   ├── migrations/              # database migrations
│   └── management/commands/     # custom Django commands
│
├── grocery_delivery/            # project configuration (settings, urls, wsgi)
├── templates/                   # HTML templates
├── static/                      # CSS, JS, images
├── media/                       # uploaded files (product images, profiles)
├── manage.py
├── requirements.txt
├── README.md                    # this file
├── SETUP.md                     # setup instructions
├── API_REFERENCE.md             # detailed API docs
├── ADD_IMAGES_GUIDE.md          # guide for adding product images
└── PRODUCTS_SUMMARY.md          # summary of products and categories
```

## 🛠 Getting Started

1. **Clone repository** and navigate into the project directory.
2. **Create a virtual environment** and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   # or `source venv/bin/activate` on Mac/Linux
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create a superuser** for admin access:
   ```bash
   python manage.py createsuperuser
   ```
6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```
7. **Access the app** at http://127.0.0.1:8000/ and the admin at
   http://127.0.0.1:8000/admin/.

See `SETUP.md` for more detailed configuration and deployment notes.

## 📘 Documentation

- API documentation: see [`API_REFERENCE.md`](API_REFERENCE.md).
- Product management: refer to [`ADD_IMAGES_GUIDE.md`](ADD_IMAGES_GUIDE.md) to upload images.
- Current product/catalog status: [`PRODUCTS_SUMMARY.md`](PRODUCTS_SUMMARY.md).

## 🧩 How to Contribute

1. Fork the repository and create a feature branch.
2. Add tests for new functionality.
3. Submit a pull request with clear description of changes.

## 📄 License

[MIT License](LICENSE) – feel free to use and modify the code.

---

Thanks for checking out FreshMart! Happy coding 😊

