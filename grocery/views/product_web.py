from django.views.generic import ListView, DetailView
from django.db.models import Q
from ..models import Product, Category, CartItem
from django.http import JsonResponse
from ..models import Product 


class HomeView(ListView):
    model = Product
    template_name = 'grocery/home.html'
    context_object_name = 'products'
    paginate_by = 100

    def get_queryset(self):
        return Product.objects.filter(is_active=True, stock__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_order = [
            "Fruits & Vegetables",
            "Masala & Dry Fruits",
            "Breakfast & Sauces",
            "Dairy, Breads & Eggs",
            "Packaged Food",
            "Atta, Rice & Dal",
            "Tea, Coffee & More",
            "Ice Cream & More",
            "Cold Drinks & Juices",
            "Sweets Cravings"
        ]
        categories = Category.objects.all().order_by('order')
        categories_dict = {cat.name: cat for cat in categories}
        sorted_categories = [categories_dict[name] for name in category_order if name in categories_dict]
        remaining_categories = [cat for cat in categories if cat.name not in category_order]
        sorted_categories.extend(remaining_categories)

        context['categories'] = sorted_categories
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'grocery/product_list.html'
    context_object_name = 'products'
    paginate_by = 100

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_slug = self.request.GET.get('category')

        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')

        if category_slug:
            context['current_category'] = Category.objects.get(slug=category_slug)
        else:
            context['current_category'] = None

        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'grocery/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        if self.request.user.is_authenticated:
            try:
                cart_item = CartItem.objects.get(cart__user=self.request.user, product=self.object)
                context['cart_quantity'] = cart_item.quantity
            except CartItem.DoesNotExist:
                context['cart_quantity'] = 0
        else:
            context['cart_quantity'] = 0
        return context
    

def search_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = []
    if len(query) > 1:
        # Fetch top 5 matching products
        results = Product.objects.filter(name__icontains=query)[:5]
        suggestions = [{'id': p.id, 'name': p.name} for p in results]
    
    return JsonResponse({'suggestions': suggestions})