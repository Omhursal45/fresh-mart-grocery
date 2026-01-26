from django.urls import path

from grocery.views.api import (
    add_to_wishlist,
    cart_count_api,
    remove_cart_item,
    update_cart_quantity,
    cart_total_api,
)

urlpatterns = [
    path('wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('cart-count/', cart_count_api, name='cart_count_api'),
    path('cart/<int:item_id>/remove/', remove_cart_item, name='remove_cart_item'),
    path('cart/<int:item_id>/update_quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('cart/total/', cart_total_api, name='cart_total_api'),
    path("cart/update/<int:item_id>/", update_cart_quantity, name="cart_update"),
    path("cart/remove/<int:item_id>/", remove_cart_item, name="cart_remove"),
]
