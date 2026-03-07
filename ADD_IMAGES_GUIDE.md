# How to Add Product Images

## Option 1: Through Django Admin Panel (Recommended)

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access Admin Panel:**
   - Go to: http://127.0.0.1:8000/admin/
   - Login with your superuser credentials

3. **Add Images to Products:**
   - Navigate to **Grocery** → **Products**
   - Click on any product you want to add an image to
   - Scroll down to the **Image** field
   - Click **Choose File** and select an image from your computer
   - Click **Save**

## Option 2: Using Python Script

You can also use the Django shell to add images programmatically:

```python
python manage.py shell
```

Then in the shell:
```python
from grocery.models import Product
from django.core.files import File

# Example: Add image to a product
product = Product.objects.get(slug='fresh-apples')
with open('path/to/your/image.jpg', 'rb') as f:
    product.image.save('apples.jpg', File(f), save=True)
```

## Image Requirements

- **Recommended formats:** JPG, PNG, WebP
- **Recommended size:** 800x800 pixels or larger (square images work best)
- **File size:** Keep under 5MB for better performance
- **Aspect ratio:** 1:1 (square) is ideal for product images

## Free Image Resources

You can download free product images from:
- **Unsplash:** https://unsplash.com/s/photos/grocery
- **Pexels:** https://www.pexels.com/search/grocery/
- **Pixabay:** https://pixabay.com/images/search/grocery/

## Quick Image Download Script

You can use this Python script to download sample images (requires `requests` and `Pillow`):

```python
import requests
from grocery.models import Product

# Example: Download and add image
product = Product.objects.get(slug='fresh-apples')
image_url = 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800'

response = requests.get(image_url)
if response.status_code == 200:
    from django.core.files.base import ContentFile
    product.image.save('apples.jpg', ContentFile(response.content), save=True)
    print(f"Image added to {product.name}")
```

## Bulk Image Upload

For bulk image uploads, you can create a management command or use the admin's bulk actions feature.

## Current Products Created

The following products have been created (without images):
- 5 Fruits (Apples, Bananas, Oranges, Grapes, Strawberries)
- 6 Vegetables (Tomatoes, Potatoes, Onions, Carrots, Broccoli, Spinach)
- 5 Dairy products (Milk, Butter, Cheese, Yogurt, Paneer)
- 4 Bakery items (White Bread, Brown Bread, Croissants, Donuts)
- 4 Beverages (Orange Juice, Apple Juice, Coca Cola, Mineral Water)
- 4 Snacks (Potato Chips, Cookies, Chocolate Bar, Nuts Mix)
- 3 Meat & Seafood items (Chicken Breast, Fish Fillet, Prawns)
- 3 Frozen Foods (Frozen Peas, Ice Cream, Frozen Pizza)

**Total: 34 products across 8 categories**

## Tips

1. **Consistent sizing:** Try to use images of similar dimensions for a uniform look
2. **Good lighting:** Use well-lit product photos
3. **Clean background:** White or neutral backgrounds work best
4. **High quality:** Use high-resolution images for better display
5. **File naming:** Use descriptive filenames (e.g., `fresh-apples.jpg`)

