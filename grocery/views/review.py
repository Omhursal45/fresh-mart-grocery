
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Product, Review, OrderItem

@login_required
def add_review(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if Review.objects.filter(product=product, user=request.user).exist():
        messages.error(request, "You already reviewed this product.")
        return redirect('product_detail', product_id = product_id)
    
    has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        order__status="Delivered",
        product=product
    ).exists()

    if not has_purchased:
        messages.error(request, "You can only review products you have purchased.")
        return redirect("product_detail", product_id=product.id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

        messages.success(request, "Review added successfully!")
        return redirect("product_detail", product_id=product.id)

    return redirect("product_detail", product_id=product.id)