from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from ..models import Wishlist, Product 



@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "wishlist.html", {"wishlist_items": wishlist_items})


@login_required
def add_to_wishlist(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        obj, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        return JsonResponse({"added": created})

    return JsonResponse({"error": "Invalid request"}, status=400)
