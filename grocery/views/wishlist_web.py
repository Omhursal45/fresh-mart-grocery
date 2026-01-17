from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Wishlist


@login_required
def wishlist_view(request):
    wishlist_items = (
        Wishlist.objects
        .filter(user=request.user)
        .select_related("product")
    )

    return render(
        request,
        "wishlist.html",
        {"wishlist_items": wishlist_items}
    )
