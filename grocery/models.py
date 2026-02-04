# from django.db import models
# from django.contrib.auth.models import User
# from django.core.validators import MinValueValidator
# from decimal import Decimal
# import uuid
# import datetime

# # ===================== CATEGORY =====================
# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     slug = models.SlugField(unique=True)
#     image = models.ImageField(upload_to='categories/', blank=True, null=True)
#     order = models.PositiveIntegerField(default=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['order']
#         verbose_name_plural = "Categories"

#     def __str__(self):
#         return self.name


# # ===================== SUBCATEGORY =====================
# class SubCategory(models.Model):
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE,
#         related_name="subcategories"
#     )
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=100)

#     class Meta:
#         unique_together = ('category', 'slug')
#         ordering = ['name']

#     def __str__(self):
#         return f"{self.category.name} → {self.name}"


# # ===================== PRODUCT =====================
# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, unique=True)
#     description = models.TextField()
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         validators=[MinValueValidator(Decimal('0.01'))]
#     )
#     image = models.ImageField(upload_to='products/', blank=True, null=True)
#     stock = models.PositiveIntegerField(default=0)

#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE,
#         related_name='products'
#     )
#     subcategory = models.ForeignKey(
#         SubCategory,
#         on_delete=models.CASCADE,
#         related_name='products',
#         null=True,
#         blank=True
#     )

#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.name

#     @property
#     def in_stock(self):
#         return self.stock > 0


# # ===================== CART =====================
# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     @property
#     def subtotal(self):
#         return sum(item.total_price for item in self.items.all())

#     def __str__(self):
#         return f"{self.user.username}'s Cart"


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def total_price(self):
#         return self.product.price * self.quantity

#     total_price.short_description = "Total Price"


# # ===================== WISHLIST =====================
# class Wishlist(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="wishlist"
#     )
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name="wishlisted_by"
#     )
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'product')

#     def __str__(self):
#         return f"{self.user.username} - {self.product.name}"


# # ===================== COUPON =====================
# class Coupon(models.Model):
#     code = models.CharField(max_length=50, unique=True)
#     description = models.TextField(blank=True)
#     discount_type = models.CharField(
#         max_length=10,
#         choices=[
#             ('percentage', 'Percentage'),
#             ('fixed', 'Fixed Amount'),
#         ],
#         default='percentage'
#     )
#     discount_value = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         validators=[MinValueValidator(Decimal('0.01'))]
#     )
#     min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()
#     is_active = models.BooleanField(default=True)
#     usage_limit = models.PositiveIntegerField(null=True, blank=True)
#     used_count = models.PositiveIntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.code


# # ===================== ADDRESS =====================
# class Address(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20)
#     address_line1 = models.CharField(max_length=200)
#     address_line2 = models.CharField(max_length=200, blank=True)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=20)
#     country = models.CharField(max_length=100, default='India')
#     is_default = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-is_default', '-created_at']

#     def __str__(self):
#         return f"{self.name} - {self.city}"


# # ===================== DELIVERY SLOT =====================
# class DeliverySlot(models.Model):
#     slot_type = models.CharField(
#         max_length=20,
#         choices=[
#             ('morning', 'Morning (9 AM - 12 PM)'),
#             ('evening', 'Evening (5 PM - 8 PM)'),
#         ]
#     )
#     delivery_date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     max_orders = models.PositiveIntegerField(default=50)
#     current_orders = models.PositiveIntegerField(default=0)
#     is_available = models.BooleanField(default=True)


#     class Meta:
#         ordering = ['delivery_date', 'start_time']

#     @property
#     def is_full(self):
#         return self.current_orders >= self.max_orders

#     def __str__(self):
#         return f"{self.slot_type.capitalize()} - {self.delivery_date}"


# # ===================== ORDER =====================
# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('placed', 'Placed'),
#         ('packed', 'Packed'),
#         ('out_for_delivery', 'Out for delivery'),
#         ('delivered', 'Delivered'),
#         ('cancelled', 'Cancelled'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     order_number = models.CharField(max_length=50, unique=True, editable=False)
#     address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
#     delivery_slot = models.ForeignKey(DeliverySlot, on_delete=models.SET_NULL, null=True, blank=True)
#     coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

#     subtotal = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#     current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Order {self.order_number}"

#     def save(self, *args, **kwargs):
#         """Generates a unique Zepto-style order number on first save."""
#         if not self.order_number:
#             date_part = datetime.date.today().strftime('%Y%m%d')
#             random_part = uuid.uuid4().hex[:4].upper()
#             self.order_number = f"ZEP-{date_part}-{random_part}"
#         super().save(*args, **kwargs)

#     def update_status(self, new_status, notes=None):
#         self.current_status = new_status
#         self.save()


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     product_name = models.CharField(max_length=200)
#     product_price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField()
#     total = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.product_name} x {self.quantity}"


# # ===================== PROFILE =====================
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     image = models.ImageField(upload_to='profile_pics/', default='default.png', null=True, blank=True)

#     def __str__(self):
#         return f'{self.user.username} Profile'
