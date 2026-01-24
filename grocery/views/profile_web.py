from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Profile, Address, Order
from django.contrib import messages

@login_required
def profile_view(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'addresses': addresses,
        'orders': orders,
    }
    return render(request, 'grocery/profile.html', context)


@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("profile")
    return render(request, "grocery/edit_profile.html", {"user": user})


@login_required
def fresh_mart_wallet(request):
    return render(request, "grocery/freshmart_wallet.html")