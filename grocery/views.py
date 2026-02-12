# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib import messages
# from django.views.generic import ListView, DetailView
# from django.db.models import Q
# from django.utils import timezone
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# from django.db import transaction
# from django.db.models import Sum, F, DecimalField, ExpressionWrapper

# from decimal import Decimal
# import json

# from .models import (
#     Product, Category, Cart, CartItem, Order, OrderItem, Address,
#     Coupon, DeliverySlot, Wishlist
# )
# from .serializers import ProductSerializer, CartSerializer
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status


# def signup_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'grocery/signup.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, f'Welcome back, {username}!')
#             next_url = request.GET.get('next', None)
#             if next_url:
#                 return redirect(next_url)
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid username or password.')
#     return render(request, 'grocery/login.html')


# @login_required
# def logout_view(request):
#     logout(request)
#     messages.success(request, "Logged out successfully")
#     return redirect('login')

# class HomeView(ListView):
#     model = Product
#     template_name = 'grocery/home.html'
#     context_object_name = 'products'
#     paginate_by = 100

#     def get_queryset(self):
#         return Product.objects.filter(is_active=True, stock__gt=0)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         category_order = [
#             "Fruits & Vegetables",
#             "Masala & Dry Fruits",
#             "Breakfast & Sauces",
#             "Dairy, Breads & Eggs",
#             "Packaged Food",
#             "Atta, Rice & Dal",
#             "Tea, Coffee & More",
#             "Ice Cream & More",
#             "Cold Drinks & Juices",
#             "Sweets Cravings"
#         ]
#         categories = Category.objects.all().order_by('order')
#         categories_dict = {cat.name: cat for cat in categories}
#         sorted_categories = [categories_dict[name] for name in category_order if name in categories_dict]
#         remaining_categories = [cat for cat in categories if cat.name not in category_order]
#         sorted_categories.extend(remaining_categories)

#         context['categories'] = sorted_categories
#         return context

# from django.db.models import Q
# from .models import Category, Product

# class ProductListView(ListView):
#     model = Product
#     template_name = 'grocery/product_list.html'
#     context_object_name = 'products'
#     paginate_by = 100

#     def get_queryset(self):
#         queryset = Product.objects.filter(is_active=True)

#         category_slug = self.request.GET.get('category')
#         if category_slug:
#             queryset = queryset.filter(category__slug=category_slug)

#         search_query = self.request.GET.get('q')
#         if search_query:
#             queryset = queryset.filter(
#                 Q(name__icontains=search_query) |
#                 Q(description__icontains=search_query)
#             )

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         category_slug = self.request.GET.get('category')

#         context['categories'] = Category.objects.all()
#         context['search_query'] = self.request.GET.get('q', '')

#         if category_slug:
#             context['current_category'] = Category.objects.get(slug=category_slug)
#         else:
#             context['current_category'] = None

#         return context

# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'grocery/product_detail.html'
#     context_object_name = 'product'
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['related_products'] = Product.objects.filter(
#             category=self.object.category,
#             is_active=True
#         ).exclude(id=self.object.id)[:4]
#         if self.request.user.is_authenticated:
#             try:
#                 cart_item = CartItem.objects.get(cart__user=self.request.user, product=self.object)
#                 context['cart_quantity'] = cart_item.quantity
#             except CartItem.DoesNotExist:
#                 context['cart_quantity'] = 0
#         else:
#             context['cart_quantity'] = 0
#         return context

# @login_required
# def cart_view(request):
#     cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')
#     total = sum(item.product.price * item.quantity for item in cart_items)
#     context = {
#         'cart_items': cart_items,
#         'subtotal': total,
#         'total': total,
#     }
#     return render(request, 'grocery/cart.html', context)


# @login_required
# def add_to_cart(request, product_id):
#     if request.method == "POST":
#         product = get_object_or_404(Product, id=product_id)
#         cart, _ = Cart.objects.get_or_create(user=request.user)
#         item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#         if not created:
#             item.quantity += 1
#             item.save()
#         return JsonResponse({"status": "success", "message": "Product added"})


# @login_required
# def checkout_view(request):
#     cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')
    
#     if not cart_items.exists():
#         messages.warning(request, 'Your cart is empty.')
#         return redirect('cart')

#     addresses = Address.objects.filter(user=request.user)
#     delivery_slots = DeliverySlot.objects.filter(
#         delivery_date__gte=timezone.now().date(),
#         is_available=True
#     ).order_by('delivery_date', 'start_time')[:10]

#     subtotal = sum(item.product.price * item.quantity for item in cart_items)
#     handling_fee = 2
#     total = subtotal + handling_fee

#     if request.method == 'POST':
#         address_id = request.POST.get('address_id')
#         delivery_slot_id = request.POST.get('delivery_slot_id')

#         if not address_id or not delivery_slot_id:
#             messages.error(request, 'Please select both an address and a delivery slot.')
#         else:
#             try:
#                 with transaction.atomic():
#                     address = get_object_or_404(Address, id=address_id, user=request.user)
#                     delivery_slot = DeliverySlot.objects.get(id=delivery_slot_id)
#                     for item in cart_items:
#                         if item.quantity > item.product.stock:
#                             messages.error(request, f'Insufficient stock for {item.product.name}')
#                             return redirect('cart')
                        
#                     order = Order.objects.create(
#                         user=request.user,
#                         address=address,
#                         delivery_slot=delivery_slot,
#                         subtotal=subtotal,
#                         total=total,
#                         current_status='placed'
#                     )
#                     for item in cart_items:
#                         OrderItem.objects.create(
#                             order=order,
#                             product=item.product,
#                             product_name=item.product.name,
#                             product_price=item.product.price,
#                             quantity=item.quantity,
#                             total=item.product.price * item.quantity
#                         )
#                         item.product.stock -= item.quantity
#                         item.product.save()
#                     cart_items.delete()
#                     messages.success(request, f'Order placed successfully! ID: {order.id}')
#                     return redirect('order_detail', order_id=order.id)

#             except DeliverySlot.DoesNotExist:
#                 messages.error(request, 'The selected delivery slot is no longer available.')
#             except Exception as e:
#                 messages.error(request, f'An error occurred: {str(e)}')
#     context = {
#         'cart_items': cart_items,
#         'addresses': addresses,
#         'delivery_slots': delivery_slots,
#         'subtotal': subtotal,
#         'total': subtotal, 
#     }
#     return render(request, 'grocery/checkout.html', context)

# @login_required
# def order_list_view(request):
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'grocery/orders.html', {'orders': orders})


# @login_required
# def order_detail_view(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     return render(request, 'grocery/order_detail.html', {'order': order})


# @login_required
# def cancel_order(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     if order.current_status not in ['placed', 'packed']:
#         messages.error(request, "Order cannot be cancelled.")
#         return redirect('orders')
#     order.current_status = 'cancelled'
#     order.save()
#     messages.success(request, "Order cancelled successfully.")
#     return redirect('orders')



# @login_required
# def profile_view(request):
#     addresses = Address.objects.filter(user=request.user)
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
#     context = {
#         'addresses': addresses,
#         'orders': orders,
#     }
#     return render(request, 'grocery/profile.html', context)


# @login_required
# def edit_profile_view(request):
#     user = request.user
#     if request.method == "POST":
#         user.first_name = request.POST.get("first_name")
#         user.last_name = request.POST.get("last_name")
#         user.email = request.POST.get("email")
#         user.save()
#         messages.success(request, "Profile updated successfully")
#         return redirect("profile")
#     return render(request, "grocery/edit_profile.html", {"user": user})


# @login_required
# def address_create_view(request):
#     if request.method == 'POST':
#         Address.objects.create(
#             user=request.user,
#             name=request.POST.get('name'),
#             phone=request.POST.get('phone'),
#             address_line1=request.POST.get('address_line1'),
#             address_line2=request.POST.get('address_line2', ''),
#             city=request.POST.get('city'),
#             state=request.POST.get('state'),
#             postal_code=request.POST.get('postal_code'),
#             country=request.POST.get('country', 'India'),
#             is_default=request.POST.get('is_default') == 'on',
#         )
#         messages.success(request, 'Address added successfully!')
#         return redirect('profile')
#     return render(request, 'grocery/address_form.html', {'action': 'Add'})


# @login_required
# def address_update_view(request, address_id):
#     address = get_object_or_404(Address, id=address_id, user=request.user)
#     if request.method == 'POST':
#         address.name = request.POST.get('name')
#         address.phone = request.POST.get('phone')
#         address.address_line1 = request.POST.get('address_line1')
#         address.address_line2 = request.POST.get('address_line2', '')
#         address.city = request.POST.get('city')
#         address.state = request.POST.get('state')
#         address.postal_code = request.POST.get('postal_code')
#         address.country = request.POST.get('country', 'India')
#         address.is_default = request.POST.get('is_default') == 'on'
#         address.save()
#         messages.success(request, 'Address updated successfully!')
#         return redirect('profile')
#     return render(request, 'grocery/address_form.html', {'address': address, 'action': 'Edit'})


# @login_required
# def address_delete_view(request, address_id):
#     address = get_object_or_404(Address, id=address_id, user=request.user)
#     if request.method == 'POST':
#         address.delete()
#         messages.success(request, 'Address deleted successfully!')
#         return redirect('profile')
#     return render(request, 'grocery/address_delete.html', {'address': address})

# @csrf_exempt
# @login_required
# def add_to_wishlist(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             product_id = data.get("product_id")
#             product = Product.objects.get(id=product_id)
#             wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
#             if created:
#                 return JsonResponse({"status": "success", "message": "Added to Wishlist"})
#             else:
#                 return JsonResponse({"status": "info", "message": "Already in Wishlist"})
#         except Product.DoesNotExist:
#             return JsonResponse({"status": "error", "message": "Product not found"})
#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)})
#     return JsonResponse({"status": "error", "message": "Invalid request"})


# @login_required
# def wishlist_view(request):
#     wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
#     return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

# from django.db.models import Sum
# def cart_count_api(request):
#     if request.user.is_authenticated:
#         count = CartItem.objects.filter(
#             cart__user=request.user
#         ).aggregate(total=Sum('quantity'))['total'] or 0
#     else:
#         count = 0

#     return JsonResponse({'cart_count': count})

# from django.views.decorators.http import require_POST

# @require_POST
# @login_required
# def remove_cart_item(request, item_id):
#     item = get_object_or_404(
#         CartItem,
#         id=item_id,
#         cart__user=request.user
#     )
#     item.delete()
#     return JsonResponse({"success": True})

# @require_POST
# @login_required
# def update_cart_quantity(request, item_id):
#     try:
#         data = json.loads(request.body)
#         quantity = int(data.get("quantity", 1))

#         item = CartItem.objects.get(
#             id=item_id,
#             cart__user=request.user
#         )

#         if quantity < 1:
#             item.delete()
#             return JsonResponse({"quantity": 0, "total_price": 0, "success": True})
#         if quantity > item.product.stock:
#             return JsonResponse({"error": "Not enough stock"}, status=400)

#         item.quantity = quantity
#         item.save()
#         item_total = float(item.product.price * item.quantity)
        
#         return JsonResponse({
#             "success": True,
#             "quantity": item.quantity,
#             "total_price": item_total,
#         })

#     except CartItem.DoesNotExist:
#         return JsonResponse({"error": "Item not found"}, status=404)

# @login_required
# def cart_total_api(request):
#     cart_items = CartItem.objects.filter(cart__user=request.user)
#     total = sum(item.product.price * item.quantity for item in cart_items)
    
#     return JsonResponse({
#         "total": float(total)
#     })


# @login_required
# def cart_total_api(request):
#     total = (
#         CartItem.objects
#         .filter(cart__user=request.user)
#         .aggregate(
#             total=Sum(
#                 ExpressionWrapper(
#                     F('quantity') * F('product__price'),
#                     output_field=DecimalField(max_digits=10, decimal_places=2)
#                 )
#             )
#         )['total']
#         or Decimal('0.00')
#     )

#     return JsonResponse({
#         "total": float(total)
#     })

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Profile

# @login_required
# def edit_profile_view(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         request.user.username = request.POST.get('username')
#         request.user.email = request.POST.get('email')
#         request.user.save()
#         if 'image' in request.FILES:
#             profile.image = request.FILES['image']
#             profile.save()
            
#         return redirect('profile')

#     return render(request, "grocery/edit_profile.html", {"user": request.user})

