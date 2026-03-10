from django.contrib import admin
from .models import (
    Category, SubCategory, Product,
    Cart, CartItem,
    Wishlist,
    Coupon,
    Address,
    DeliverySlot,
    Order, OrderItem,
    Review,
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('name',)


from django.db.models import Count

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory','review_count', 'price', 'stock', 'is_active', 'created_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(review_total=Count('reviews'))

    def review_count(self, obj):
        return obj.review_total
    
    


class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ('total_price',)
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]



@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('added_at',)



@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'is_active', 'created_at')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('code', 'description')
    readonly_fields = ('created_at',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'city', 'state', 'is_default', 'created_at')
    list_filter = ('city', 'state', 'is_default')
    search_fields = ('user__username', 'name', 'address_line1', 'city', 'state')
    readonly_fields = ('created_at',)



@admin.register(DeliverySlot)
class DeliverySlotAdmin(admin.ModelAdmin):
    list_display = ('delivery_date', 'slot_type', 'start_time', 'end_time', 'is_available', 'current_orders')
    list_filter = ('slot_type', 'delivery_date', 'is_available')
    ordering = ('delivery_date', 'start_time')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product_name', 'product_price', 'quantity', 'total')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'current_status', 'total', 'created_at')
    list_filter = ('current_status', 'created_at')
    search_fields = ('order_number', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def rating_stars(self, obj):
        return "⭐" * obj.rating
    
