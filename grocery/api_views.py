from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal

from .models import (
    Product, Category, Cart, Order, OrderItem, Address,
    Coupon, DeliverySlot
)
from .serializers import (
    ProductSerializer, CategorySerializer, CartSerializer,
    OrderSerializer, AddressSerializer, CouponSerializer,
    DeliverySlotSerializer
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('q')

        if category:
            queryset = queryset.filter(category__slug=category)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def search_api(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return Response(
            {'error': 'Query parameter "q" is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query),
        is_active=True
    )
    return Response(ProductSerializer(products, many=True).data)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id, is_active=True)

        if quantity < 1:
            return Response({'error': 'Quantity must be at least 1'}, status=400)

        if quantity > product.stock:
            return Response({'error': 'Insufficient stock'}, status=400)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            if cart_item.quantity + quantity > product.stock:
                return Response({'error': 'Insufficient stock'}, status=400)
            cart_item.quantity += quantity
            cart_item.save()

        return Response(self.get_serializer(cart_item).data, status=201)

    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        cart_item = self.get_object()
        quantity = int(request.data.get('quantity', 1))

        if quantity < 1 or quantity > cart_item.product.stock:
            return Response({'error': 'Invalid quantity'}, status=400)

        cart_item.quantity = quantity
        cart_item.save()
        return Response(self.get_serializer(cart_item).data)

    @action(detail=False, methods=['get'])
    def total(self, request):
        total = sum(item.total_price for item in self.get_queryset())
        return Response({'total': float(total)})


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        order = self.get_object()
        return Response({
            'order_number': order.order_number,
            'current_status': order.current_status
        })

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coupon.objects.filter(is_active=True)
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'])
    def validate(self, request):
        code = request.data.get('code', '').strip()
        cart_total = Decimal(str(request.data.get('cart_total', 0)))

        coupon = get_object_or_404(Coupon, code=code, is_active=True)
        is_valid, message = coupon.is_valid(request.user, cart_total)

        if not is_valid:
            return Response({'error': message}, status=400)

        discount = coupon.calculate_discount(cart_total)
        return Response({
            'valid': True,
            'discount': float(discount),
            'type': coupon.discount_type
        })

class DeliverySlotViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DeliverySlotSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return DeliverySlot.objects.filter(
            delivery_date__gte=timezone.now().date(),
            is_available=True
        ).order_by('delivery_date', 'start_time')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_api(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')

    if not cart_items.exists():
        return Response({'error': 'Cart is empty'}, status=400)

    address = get_object_or_404(Address, id=request.data.get('address_id'), user=request.user)

    subtotal = sum(item.total_price for item in cart_items)
    discount = Decimal('0')
    coupon = None

    code = request.data.get('coupon_code', '').strip()
    if code:
        coupon = get_object_or_404(Coupon, code=code, is_active=True)
        valid, msg = coupon.is_valid(request.user, subtotal)
        if not valid:
            return Response({'error': msg}, status=400)
        discount = coupon.calculate_discount(subtotal)

    order = Order.objects.create(
        user=request.user,
        address=address,
        subtotal=subtotal,
        discount=discount,
        total=subtotal - discount
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            product_price=item.product.price,
            quantity=item.quantity,
            total=item.total_price
        )
        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()
    order.update_status('placed', 'Order placed successfully')

    return Response(OrderSerializer(order).data, status=201)
