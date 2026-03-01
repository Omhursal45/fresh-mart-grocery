from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Product, Category, Cart, Order, OrderItem,
    Address, Coupon, DeliverySlot
)
from rest_framework import serializers
from .models import CartItem, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description',
            'price', 'image', 'stock',
            'category', 'category_id',
            'is_active', 'in_stock', 'created_at'
        ]

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.FloatField(source='product.price', read_only=True)
    total_price = serializers.SerializerMethodField()

    # allow sending product by id
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'product_name', 'product_price', 'total_price']
        read_only_fields = ['product']

    def get_total_price(self, obj):
        return float(obj.product.price * obj.quantity)

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'subtotal']

    def get_subtotal(self, obj):
        return float(sum(item.product.price * item.quantity for item in obj.items.all()))
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'name', 'phone',
            'address_line1', 'address_line2',
            'city', 'state', 'postal_code',
            'country', 'is_default', 'created_at'
        ]

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'description',
            'discount_type', 'discount_value',
            'min_purchase', 'max_discount',
            'valid_from', 'valid_to', 'is_active'
        ]

class DeliverySlotSerializer(serializers.ModelSerializer):
    is_full = serializers.ReadOnlyField()

    class Meta:
        model = DeliverySlot
        fields = [
            'id', 'slot_type', 'delivery_date',
            'start_time', 'end_time',
            'max_orders', 'current_orders',
            'is_available', 'is_full'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product_name',
            'product_price', 'quantity', 'total'
        ]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    delivery_slot = DeliverySlotSerializer(read_only=True)
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number',
            'address', 'delivery_slot',
            'coupon', 'subtotal',
            'discount', 'total',
            'current_status',
            'created_at', 'updated_at',
            'items'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
