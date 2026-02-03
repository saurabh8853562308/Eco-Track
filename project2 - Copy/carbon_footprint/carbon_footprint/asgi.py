"""
ASGI config for carbon_footprint project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_footprint.settings')

application = get_asgi_application()
