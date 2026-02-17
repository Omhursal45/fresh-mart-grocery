from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from grocery.models import Category, Product, Coupon, DeliverySlot


class Command(BaseCommand):
    help = 'Populate database with sample categories, products, coupons, and delivery slots'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate database...'))

        # Create Categories
        categories_data = [
            {'name': 'Fruits', 'slug': 'fruits', 'description': 'Fresh and organic fruits'},
            {'name': 'Vegetables', 'slug': 'vegetables', 'description': 'Fresh vegetables'},
            {'name': 'Dairy', 'slug': 'dairy', 'description': 'Milk, cheese, and dairy products'},
            {'name': 'Bakery', 'slug': 'bakery', 'description': 'Fresh bread and baked goods'},
            {'name': 'Beverages', 'slug': 'beverages', 'description': 'Drinks and beverages'},
            {'name': 'Snacks', 'slug': 'snacks', 'description': 'Chips, cookies, and snacks'},
            {'name': 'Meat & Seafood', 'slug': 'meat-seafood', 'description': 'Fresh meat and seafood'},
            {'name': 'Frozen Foods', 'slug': 'frozen-foods', 'description': 'Frozen food items'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category.name}'))

        # Create Products
        products_data = [
            # Fruits
            {'name': 'Fresh Apples', 'slug': 'fresh-apples', 'description': 'Crisp and juicy red apples, perfect for snacking. Rich in fiber and vitamin C.', 'price': Decimal('120.00'), 'stock': 50, 'category': 'fruits'},
            {'name': 'Bananas', 'slug': 'bananas', 'description': 'Fresh yellow bananas, great source of potassium and energy.', 'price': Decimal('60.00'), 'stock': 100, 'category': 'fruits'},
            {'name': 'Oranges', 'slug': 'oranges', 'description': 'Sweet and tangy oranges, packed with vitamin C.', 'price': Decimal('80.00'), 'stock': 75, 'category': 'fruits'},
            {'name': 'Grapes', 'slug': 'grapes', 'description': 'Fresh seedless grapes, perfect for snacking or making juice.', 'price': Decimal('150.00'), 'stock': 40, 'category': 'fruits'},
            {'name': 'Strawberries', 'slug': 'strawberries', 'description': 'Fresh red strawberries, sweet and juicy.', 'price': Decimal('200.00'), 'stock': 30, 'category': 'fruits'},
            
            # Vegetables
            {'name': 'Tomatoes', 'slug': 'tomatoes', 'description': 'Fresh red tomatoes, perfect for salads and cooking.', 'price': Decimal('40.00'), 'stock': 80, 'category': 'vegetables'},
            {'name': 'Potatoes', 'slug': 'potatoes', 'description': 'Fresh potatoes, ideal for cooking various dishes.', 'price': Decimal('35.00'), 'stock': 100, 'category': 'vegetables'},
            {'name': 'Onions', 'slug': 'onions', 'description': 'Fresh onions, essential for cooking.', 'price': Decimal('30.00'), 'stock': 90, 'category': 'vegetables'},
            {'name': 'Carrots', 'slug': 'carrots', 'description': 'Fresh orange carrots, rich in beta-carotene.', 'price': Decimal('50.00'), 'stock': 70, 'category': 'vegetables'},
            {'name': 'Broccoli', 'slug': 'broccoli', 'description': 'Fresh green broccoli, packed with nutrients.', 'price': Decimal('80.00'), 'stock': 45, 'category': 'vegetables'},
            {'name': 'Spinach', 'slug': 'spinach', 'description': 'Fresh leafy spinach, great for salads and cooking.', 'price': Decimal('40.00'), 'stock': 60, 'category': 'vegetables'},
            
            # Dairy
            {'name': 'Fresh Milk', 'slug': 'fresh-milk', 'description': 'Pure fresh milk, 1 liter pack.', 'price': Decimal('60.00'), 'stock': 100, 'category': 'dairy'},
            {'name': 'Butter', 'slug': 'butter', 'description': 'Creamy butter, 250g pack.', 'price': Decimal('55.00'), 'stock': 80, 'category': 'dairy'},
            {'name': 'Cheese', 'slug': 'cheese', 'description': 'Fresh cheese, 200g pack.', 'price': Decimal('120.00'), 'stock': 50, 'category': 'dairy'},
            {'name': 'Yogurt', 'slug': 'yogurt', 'description': 'Fresh yogurt, 500g pack.', 'price': Decimal('45.00'), 'stock': 90, 'category': 'dairy'},
            {'name': 'Paneer', 'slug': 'paneer', 'description': 'Fresh cottage cheese, 250g pack.', 'price': Decimal('180.00'), 'stock': 40, 'category': 'dairy'},
            
            # Bakery
            {'name': 'White Bread', 'slug': 'white-bread', 'description': 'Fresh white bread loaf, 400g.', 'price': Decimal('35.00'), 'stock': 60, 'category': 'bakery'},
            {'name': 'Brown Bread', 'slug': 'brown-bread', 'description': 'Healthy brown bread loaf, 400g.', 'price': Decimal('40.00'), 'stock': 50, 'category': 'bakery'},
            {'name': 'Croissants', 'slug': 'croissants', 'description': 'Fresh buttery croissants, pack of 4.', 'price': Decimal('120.00'), 'stock': 30, 'category': 'bakery'},
            {'name': 'Donuts', 'slug': 'donuts', 'description': 'Sweet glazed donuts, pack of 6.', 'price': Decimal('150.00'), 'stock': 25, 'category': 'bakery'},
            
            # Beverages
            {'name': 'Orange Juice', 'slug': 'orange-juice', 'description': 'Fresh orange juice, 1 liter.', 'price': Decimal('90.00'), 'stock': 70, 'category': 'beverages'},
            {'name': 'Apple Juice', 'slug': 'apple-juice', 'description': 'Fresh apple juice, 1 liter.', 'price': Decimal('85.00'), 'stock': 65, 'category': 'beverages'},
            {'name': 'Coca Cola', 'slug': 'coca-cola', 'description': 'Cold drink, 1.5 liter.', 'price': Decimal('60.00'), 'stock': 100, 'category': 'beverages'},
            {'name': 'Mineral Water', 'slug': 'mineral-water', 'description': 'Pure mineral water, 1 liter.', 'price': Decimal('25.00'), 'stock': 150, 'category': 'beverages'},
            
            # Snacks
            {'name': 'Potato Chips', 'slug': 'potato-chips', 'description': 'Crispy potato chips, 150g pack.', 'price': Decimal('35.00'), 'stock': 80, 'category': 'snacks'},
            {'name': 'Cookies', 'slug': 'cookies', 'description': 'Sweet cookies, 200g pack.', 'price': Decimal('50.00'), 'stock': 70, 'category': 'snacks'},
            {'name': 'Chocolate Bar', 'slug': 'chocolate-bar', 'description': 'Milk chocolate bar, 100g.', 'price': Decimal('60.00'), 'stock': 90, 'category': 'snacks'},
            {'name': 'Nuts Mix', 'slug': 'nuts-mix', 'description': 'Mixed dry fruits and nuts, 250g.', 'price': Decimal('250.00'), 'stock': 40, 'category': 'snacks'},
            
            # Meat & Seafood
            {'name': 'Chicken Breast', 'slug': 'chicken-breast', 'description': 'Fresh chicken breast, 500g.', 'price': Decimal('200.00'), 'stock': 30, 'category': 'meat-seafood'},
            {'name': 'Fish Fillet', 'slug': 'fish-fillet', 'description': 'Fresh fish fillet, 500g.', 'price': Decimal('300.00'), 'stock': 25, 'category': 'meat-seafood'},
            {'name': 'Prawns', 'slug': 'prawns', 'description': 'Fresh prawns, 500g.', 'price': Decimal('400.00'), 'stock': 20, 'category': 'meat-seafood'},
            
            # Frozen Foods
            {'name': 'Frozen Peas', 'slug': 'frozen-peas', 'description': 'Frozen green peas, 500g pack.', 'price': Decimal('80.00'), 'stock': 50, 'category': 'frozen-foods'},
            {'name': 'Ice Cream', 'slug': 'ice-cream', 'description': 'Vanilla ice cream, 500ml.', 'price': Decimal('150.00'), 'stock': 40, 'category': 'frozen-foods'},
            {'name': 'Frozen Pizza', 'slug': 'frozen-pizza', 'description': 'Ready to cook pizza, 300g.', 'price': Decimal('180.00'), 'stock': 35, 'category': 'frozen-foods'},
        ]

        for prod_data in products_data:
            category = categories[prod_data.pop('category')]
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={
                    **prod_data,
                    'category': category
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))

        # Create Coupons
        coupons_data = [
            {
                'code': 'WELCOME10',
                'description': 'Welcome offer - 10% off on first order',
                'discount_type': 'percentage',
                'discount_value': Decimal('10.00'),
                'min_purchase': Decimal('500.00'),
                'max_discount': Decimal('200.00'),
                'valid_from': timezone.now(),
                'valid_to': timezone.now() + timedelta(days=30),
                'usage_limit': 100,
            },
            {
                'code': 'SAVE50',
                'description': 'Flat ₹50 off on orders above ₹1000',
                'discount_type': 'fixed',
                'discount_value': Decimal('50.00'),
                'min_purchase': Decimal('1000.00'),
                'valid_from': timezone.now(),
                'valid_to': timezone.now() + timedelta(days=60),
                'usage_limit': 200,
            },
            {
                'code': 'BIG20',
                'description': '20% off on orders above ₹2000',
                'discount_type': 'percentage',
                'discount_value': Decimal('20.00'),
                'min_purchase': Decimal('2000.00'),
                'max_discount': Decimal('500.00'),
                'valid_from': timezone.now(),
                'valid_to': timezone.now() + timedelta(days=90),
            },
        ]

        for coupon_data in coupons_data:
            coupon, created = Coupon.objects.get_or_create(
                code=coupon_data['code'],
                defaults=coupon_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created coupon: {coupon.code}'))
            else:
                self.stdout.write(self.style.WARNING(f'Coupon already exists: {coupon.code}'))

        # Create Delivery Slots
        from datetime import date, time
        today = date.today()
        
        delivery_slots_data = []
        for i in range(7):  # Next 7 days
            slot_date = today + timedelta(days=i+1)
            delivery_slots_data.extend([
                {
                    'slot_type': 'morning',
                    'delivery_date': slot_date,
                    'start_time': time(9, 0),
                    'end_time': time(12, 0),
                    'max_orders': 50,
                },
                {
                    'slot_type': 'evening',
                    'delivery_date': slot_date,
                    'start_time': time(17, 0),
                    'end_time': time(20, 0),
                    'max_orders': 50,
                },
            ])

        for slot_data in delivery_slots_data:
            slot, created = DeliverySlot.objects.get_or_create(
                delivery_date=slot_data['delivery_date'],
                slot_type=slot_data['slot_type'],
                start_time=slot_data['start_time'],
                defaults=slot_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created delivery slot: {slot}'))
            else:
                self.stdout.write(self.style.WARNING(f'Delivery slot already exists: {slot}'))

        self.stdout.write(self.style.SUCCESS('\nDatabase populated successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(products_data)} products'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(coupons_data)} coupons'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(delivery_slots_data)} delivery slots'))
        self.stdout.write(self.style.WARNING('\nNote: Product images need to be added manually through the admin panel.'))

