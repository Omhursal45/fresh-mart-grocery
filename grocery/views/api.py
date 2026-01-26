from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from decimal import Decimal
import json

from ..models import CartItem, Product, Wishlist


@require_POST
@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )
    item.delete()

    cart_count = CartItem.objects.filter(
        cart__user=request.user
    ).aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({
        "success": True,
        "cart_count": cart_count
    })



@require_POST
@login_required
def update_cart_quantity(request, item_id):
    data = json.loads(request.body)
    quantity = int(data.get("quantity", 1))

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if quantity < 1:
        item.delete()
    else:
        item.quantity = quantity
        item.save()

    cart_count = CartItem.objects.filter(cart__user=request.user)\
                    .aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({
        "success": True,
        "quantity": quantity,
        "total_price": float(item.product.price * quantity) if quantity > 0 else 0,
        "cart_count": cart_count
    })




@login_required
def cart_total_api(request):
    total = (
        CartItem.objects
        .filter(cart__user=request.user)
        .aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('quantity') * F('product__price'),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            )
        )['total']
        or Decimal('0.00')
    )

    return JsonResponse({"total": float(total)})


@login_required
def cart_count_api(request):
    count = CartItem.objects.filter(
        cart__user=request.user
    ).aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({'cart_count': count})

@require_POST
@login_required
def add_to_wishlist(request):
    data = json.loads(request.body)
    product = get_object_or_404(Product, id=data.get("product_id"))

    _, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return JsonResponse({
        "success": True,
        "created": created
    })
