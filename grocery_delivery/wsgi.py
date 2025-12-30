"""
WSGI config for grocery_delivery project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_delivery.settings')

application = get_wsgi_application()

