from django.db import models
from django.contrib.auth.models import User
from .address import Address
from .delivery import DeliverySlot
from .coupon import Coupon
from .product import Product
import datetime
import uuid

class Order(models.Model):
    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('packed', 'Packed'),
        ('out_for_delivery', 'Out for delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, editable=False)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    delivery_slot = models.ForeignKey(DeliverySlot, on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    PAYMENT_CHOICES = [
    ('cod', 'Cash on Delivery'),
    ('upi', 'UPI'),
    ('card', 'Card'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cod'
    )


    current_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='placed'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            date_part = datetime.date.today().strftime('%Y%m%d')
            random_part = uuid.uuid4().hex[:6].upper()  # safer
            self.order_number = f"FM-{date_part}-{random_part}"
        super().save(*args, **kwargs)

    def update_status(self, new_status):
        self.current_status = new_status
        self.save(update_fields=['current_status'])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
