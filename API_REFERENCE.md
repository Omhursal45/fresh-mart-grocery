# API Reference Guide

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
Most endpoints require authentication. Use session authentication for web requests or token authentication for API clients.

## Endpoints

### Products

#### List Products
```
GET /api/products/
```
**Query Parameters:**
- `category` (optional): Filter by category slug
- `q` (optional): Search query

**Response:**
```json
[
  {
    "id": 1,
    "name": "Product Name",
    "slug": "product-name",
    "description": "Product description",
    "price": "99.99",
    "image": "/media/products/image.jpg",
    "stock": 50,
    "category": {...},
    "is_active": true,
    "in_stock": true
  }
]
```

#### Get Product Details
```
GET /api/products/{id}/
```

#### Search Products
```
GET /api/search/?q={query}
```

### Categories

#### List Categories
```
GET /api/categories/
```

### Cart

#### Get Cart Items
```
GET /api/cart/
```
**Requires Authentication**

#### Add to Cart
```
POST /api/cart/
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```
**Requires Authentication**

#### Update Cart Item Quantity
```
POST /api/cart/{id}/update_quantity/
Content-Type: application/json

{
  "quantity": 3
}
```
**Requires Authentication**

#### Remove from Cart
```
DELETE /api/cart/{id}/
```
**Requires Authentication**

#### Get Cart Total
```
GET /api/cart/total/
```
**Requires Authentication**

**Response:**
```json
{
  "total": 199.98
}
```

### Orders

#### List User Orders
```
GET /api/orders/
```
**Requires Authentication**

#### Get Order Details
```
GET /api/orders/{id}/
```
**Requires Authentication**

#### Get Order Tracking Status
```
GET /api/orders/{id}/status/
```
**Requires Authentication**

**Response:**
```json
{
  "order_number": "ORD-ABC12345",
  "current_status": "packed",
  "status_history": [
    {
      "id": 1,
      "status": "placed",
      "timestamp": "2024-01-15T10:30:00Z",
      "notes": "Order has been placed successfully."
    },
    {
      "id": 2,
      "status": "packed",
      "timestamp": "2024-01-15T11:00:00Z",
      "notes": "Order has been packed."
    }
  ]
}
```

#### Checkout (Create Order)
```
POST /api/checkout/
Content-Type: application/json

{
  "address_id": 1,
  "delivery_slot_id": 1,
  "coupon_code": "SAVE10"
}
```
**Requires Authentication**

**Response:**
```json
{
  "id": 1,
  "order_number": "ORD-ABC12345",
  "total": 899.10,
  "current_status": "placed",
  ...
}
```

### Addresses

#### List User Addresses
```
GET /api/addresses/
```
**Requires Authentication**

#### Create Address
```
POST /api/addresses/
Content-Type: application/json

{
  "name": "John Doe",
  "phone": "1234567890",
  "address_line1": "123 Main St",
  "address_line2": "Apt 4B",
  "city": "Mumbai",
  "state": "Maharashtra",
  "postal_code": "400001",
  "country": "India",
  "is_default": true
}
```
**Requires Authentication**

#### Update Address
```
PUT /api/addresses/{id}/
Content-Type: application/json

{
  "name": "John Doe",
  ...
}
```
**Requires Authentication**

#### Delete Address
```
DELETE /api/addresses/{id}/
```
**Requires Authentication**

### Coupons

#### List Available Coupons
```
GET /api/coupons/
```

#### Validate Coupon
```
POST /api/coupons/validate/
Content-Type: application/json

{
  "code": "SAVE10",
  "cart_total": 1000.00
}
```

**Response (Valid):**
```json
{
  "valid": true,
  "discount": 100.00,
  "discount_type": "percentage",
  "message": "Coupon applied successfully"
}
```

**Response (Invalid):**
```json
{
  "valid": false,
  "message": "Coupon has expired"
}
```

### Delivery Slots

#### List Available Delivery Slots

> **Note:** slots that are marked unavailable or have reached their `max_orders` count
> will not be returned by the API.  When there are no slots left the server
> automatically generates the next 7 days of morning/evening slots.
```
GET /api/delivery-slots/
```

**Query Parameters:**
- `slot_type` (optional): Filter by slot type (morning, evening, custom)

**Response:**
```json
[
  {
    "id": 1,
    "slot_type": "morning",
    "delivery_date": "2024-01-16",
    "start_time": "09:00:00",
    "end_time": "12:00:00",
    "max_orders": 50,
    "current_orders": 10,
    "is_available": true,
    "is_full": false
  }
]
```

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Error Response Format

```json
{
  "error": "Error message description"
}
```

## Order Status Values

- `placed`: Order Placed
- `packed`: Packed
- `out_for_delivery`: Out For Delivery
- `delivered`: Delivered
- `cancelled`: Cancelled

## Delivery Slot Types

- `morning`: Morning (9 AM - 12 PM)
- `evening`: Evening (5 PM - 8 PM)
- `custom`: Custom Time

## Coupon Discount Types

- `percentage`: Percentage discount
- `fixed`: Fixed amount discount

