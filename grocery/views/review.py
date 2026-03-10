
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Product, Review, OrderItem

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.error(request, "You already reviewed this product.")
        return redirect("product_detail", slug=product.slug)

    has_purchased = OrderItem.objects.filter(
        product=product,
        order__user=request.user,
        order__current_status='delivered'
    ).exists()
    
    print("HAS PURCHASED:", has_purchased)

    # if not has_purchased:
    #     messages.error(request, "You can only review products you have purchased.")
    #     return redirect("product_detail", slug=product.slug)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if not rating:
            messages.error(request, "Please select a rating.")
            return redirect("product_detail", slug=product.slug)

        rating = int(rating)

        if rating < 1 or rating > 5:
            messages.error(request, "Invalid rating value.")
            return redirect("product_detail", slug=product.slug)

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
        
        messages.success(request, "Review added successfully!")
        return redirect("product_detail", slug=product.slug)

    return redirect("product_detail", slug=product.slug)