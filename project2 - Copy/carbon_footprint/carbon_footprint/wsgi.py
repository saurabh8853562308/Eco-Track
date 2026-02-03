"""
WSGI config for carbon_footprint project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_footprint.settings')

application = get_wsgi_application()
