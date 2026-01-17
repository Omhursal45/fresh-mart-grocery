from django.db.models import Sum
from .models import CartItem, Category


def cart_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(cart__user=request.user).aggregate(
            total_quantity=Sum('quantity')
        )['total_quantity'] or 0
    else:
        count = 0
    return {'cart_count': count}


def categories(request):
    return {
        'categories': Category.objects.all()
    }
