from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from ..models import Order, OrderItem, CartItem, Address, DeliverySlot


@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    addresses = Address.objects.filter(user=request.user)
    delivery_slots = DeliverySlot.objects.filter(
        delivery_date__gte=timezone.now().date(),
        is_available=True
    ).order_by('delivery_date', 'start_time')[:10]

    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    handling_fee = 2
    total = subtotal + handling_fee

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        delivery_slot_id = request.POST.get('delivery_slot_id')
        payment_method = request.POST.get('payment_method')
        
        try:
            applied_discount = int(request.POST.get('applied_discount', 0) or 0)
        except (ValueError, TypeError):
            applied_discount = 0

        if not address_id or not delivery_slot_id or not payment_method:
            messages.error(request, 'Please select an address, slot, and payment method.')
        else:
            try:
                with transaction.atomic():
                    address = get_object_or_404(Address, id=address_id, user=request.user)
                    delivery_slot = DeliverySlot.objects.get(id=delivery_slot_id)
                    
                    for item in cart_items:
                        if item.quantity > item.product.stock:
                            messages.error(request, f'Insufficient stock for {item.product.name}')
                            return redirect('cart')

                    final_total = total - applied_discount

                    order = Order.objects.create(
                        user=request.user,
                        address=address,
                        delivery_slot=delivery_slot,
                        subtotal=subtotal,
                        total=final_total,
                        discount=applied_discount,
                        payment_method=payment_method,
                        current_status='placed'
                    )

                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            product_name=item.product.name,
                            product_price=item.product.price,
                            quantity=item.quantity,
                            total=item.product.price * item.quantity
                        )
                        item.product.stock -= item.quantity
                        item.product.save()

                    cart_items.delete()
                    messages.success(request, 'Order placed successfully!')
                    return redirect('orders')

            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    context = {
        'cart_items': cart_items,
        'addresses': addresses,
        'delivery_slots': delivery_slots,
        'subtotal': subtotal,
        'total': total,
    }
    return render(request, 'grocery/checkout.html', context)

@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'grocery/orders.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'grocery/order_detail.html', {'order': order})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.current_status not in ['placed', 'packed']:
        messages.error(request, "Order cannot be cancelled.")
        return redirect('orders')
    order.current_status = 'cancelled'
    order.save()
    messages.success(request, "Order cancelled successfully.")
    return redirect('orders')
