from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet, basename='product')
router.register(r'categories', api_views.CategoryViewSet, basename='category')
router.register(r'cart', api_views.CartViewSet, basename='cart')
router.register(r'orders', api_views.OrderViewSet, basename='order')
router.register(r'addresses', api_views.AddressViewSet, basename='address')
router.register(r'coupons', api_views.CouponViewSet, basename='coupon')
router.register(r'delivery-slots', api_views.DeliverySlotViewSet, basename='delivery-slots')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', api_views.search_api, name='search_api'),
    path('coupons/validate/', api_views.CouponViewSet.as_view({'post': 'validate'}), name='coupon_validate'),
    path('checkout/', api_views.checkout_api, name='checkout_api'),
]

