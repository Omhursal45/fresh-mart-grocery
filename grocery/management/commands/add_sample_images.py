"""
Management command to add placeholder images to products.
Note: This requires actual image files or URLs to download from.
"""
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from grocery.models import Product
import requests
from io import BytesIO


class Command(BaseCommand):
    help = 'Add sample images to products from URLs (requires internet connection)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Base URL for images (optional)',
        )

    def handle(self, *args, **options):
        # Sample image URLs from Unsplash (free stock photos)
        # These are placeholder URLs - you can replace with actual product images
        image_urls = {
            'fresh-apples': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800',
            'bananas': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=800',
            'oranges': 'https://images.unsplash.com/photo-1580052614034-c55d20bfee3b?w=800',
            'grapes': 'https://images.unsplash.com/photo-1537640538966-79f369143a8f?w=800',
            'strawberries': 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=800',
            'tomatoes': 'https://images.unsplash.com/photo-1546095667-0c4e86b0c0e0?w=800',
            'potatoes': 'https://images.unsplash.com/photo-1518977822534-7049a61ee0c2?w=800',
            'onions': 'https://images.unsplash.com/photo-1618512496249-3e3b67d87444?w=800',
            'carrots': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=800',
            'broccoli': 'https://images.unsplash.com/photo-1584270354949-c26b0d5b4a0c?w=800',
            'spinach': 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=800',
            'fresh-milk': 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=800',
            'butter': 'https://images.unsplash.com/photo-1588168333986-5078d3ae3976?w=800',
            'cheese': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=800',
            'yogurt': 'https://images.unsplash.com/photo-1488477188016-7b7215f6d0ad?w=800',
            'paneer': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800',
            'white-bread': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800',
            'brown-bread': 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=800',
            'croissants': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=800',
            'donuts': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=800',
            'orange-juice': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=800',
            'apple-juice': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=800',
            'coca-cola': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=800',
            'mineral-water': 'https://images.unsplash.com/photo-1523362628745-0c100150b504?w=800',
            'potato-chips': 'https://images.unsplash.com/photo-1566474986481-edb31c5a2667?w=800',
            'cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800',
            'chocolate-bar': 'https://images.unsplash.com/photo-1606312619070-d48b4e0016a8?w=800',
            'nuts-mix': 'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=800',
            'chicken-breast': 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=800',
            'fish-fillet': 'https://images.unsplash.com/photo-1544943910-4c1dc44aab44?w=800',
            'prawns': 'https://images.unsplash.com/photo-1606914501446-0c5c0b2a0a0a?w=800',
            'frozen-peas': 'https://images.unsplash.com/photo-1593111774240-d529f1e0b8a2?w=800',
            'ice-cream': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800',
            'frozen-pizza': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800',
        }

        self.stdout.write(self.style.SUCCESS('Starting to add images to products...'))
        self.stdout.write(self.style.WARNING('Note: This requires internet connection to download images.'))

        success_count = 0
        error_count = 0

        for slug, url in image_urls.items():
            try:
                product = Product.objects.get(slug=slug)
                
                # Skip if product already has an image
                if product.image:
                    self.stdout.write(self.style.WARNING(f'Skipping {product.name} - already has an image'))
                    continue

                # Download image
                self.stdout.write(f'Downloading image for {product.name}...')
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    # Save image
                    image_name = f'{slug}.jpg'
                    product.image.save(
                        image_name,
                        ContentFile(response.content),
                        save=True
                    )
                    self.stdout.write(self.style.SUCCESS(f'Image added to {product.name}'))
                    success_count += 1
                else:
                    self.stdout.write(self.style.ERROR(f'Failed to download image for {product.name}'))
                    error_count += 1
                    
            except Product.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Product with slug {slug} not found'))
                error_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {slug}: {str(e)}'))
                error_count += 1

        self.stdout.write(self.style.SUCCESS(f'\nCompleted!'))
        self.stdout.write(self.style.SUCCESS(f'Successfully added images to {success_count} products'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'Failed to add images to {error_count} products'))

