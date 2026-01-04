from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from ..models import Cart, CartItem, Product
import json
from django.views.decorators.http import require_POST
from django.db.models import Sum

from django.db.models import Sum

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')

    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    subtotal_items = cart_items.aggregate(total=Sum('quantity'))['total'] or 0

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'subtotal_items': subtotal_items,
    }
    return render(request, 'grocery/cart.html', context)



@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    cart_count = CartItem.objects.filter(
        cart__user=request.user
    ).aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({
        "status": "success",
        "cart_count": cart_count
    })




def cart_count_api(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(
            cart__user=request.user
        ).aggregate(total=Sum('quantity'))['total'] or 0
    else:
        count = 0

    return JsonResponse({'cart_count': count})



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
    try:
        data = json.loads(request.body)
        quantity = int(data.get("quantity", 1))

        item = CartItem.objects.get(
            id=item_id,
            cart__user=request.user
        )

        if quantity < 1:
            item.delete()
        else:
            if quantity > item.product.stock:
                return JsonResponse({"error": "Not enough stock"}, status=400)

            item.quantity = quantity
            item.save()

        cart_count = CartItem.objects.filter(
            cart__user=request.user
        ).aggregate(total=Sum('quantity'))['total'] or 0

        item_total = (
            float(item.product.price * item.quantity)
            if quantity > 0 else 0
        )

        return JsonResponse({
            "success": True,
            "quantity": item.quantity if quantity > 0 else 0,
            "total_price": item_total,
            "cart_count": cart_count
        })

    except CartItem.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)

