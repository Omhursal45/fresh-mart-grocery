from django.urls import path
# from django.contrib.auth import views as auth_views

# from grocery.views.auth import signup_view, login_view
from grocery.views.product_web import HomeView, ProductListView, ProductDetailView, search_suggestions
# from grocery.views.cart_web import cart_view, add_to_cart
# from grocery.views.order_web import order_list_view, order_detail_view, cancel_order,checkout_view
# from grocery.views.profile_web import profile_view, edit_profile_view
# from grocery.views.address_web import (
#     address_create_view,
#     address_update_view,
#     address_delete_view,
# )
# from grocery.views.wishlist_web import wishlist_view

urlpatterns = [
    # Authentication
    # path('signup/', signup_view, name='signup'),
    # path('login/', login_view, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Home & Products
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),

#     # Cart
#     path('cart/', cart_view, name='cart'),
#     path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    

#     # Orders
#     path('orders/', order_list_view, name='orders'),
#     path('orders/<int:order_id>/', order_detail_view, name='order_detail'),
#     path('orders/<int:order_id>/cancel/', cancel_order, name='cancel_order'),
#     path('checkout/', checkout_view, name='checkout'),

#     # Profile & Address
#     path('profile/', profile_view, name='profile'),
#     path('profile/edit/', edit_profile_view, name='edit_profile'),
#     path('profile/address/add/', address_create_view, name='address_create'),
#     path('profile/address/<int:address_id>/edit/', address_update_view, name='address_update'),
#     path('profile/address/<int:address_id>/delete/', address_delete_view, name='address_delete'),

#     # Wishlist
#     path('wishlist/', wishlist_view, name='wishlist'),
    
#     path('search-suggestions/', search_suggestions, name='search_suggestions'),
]
