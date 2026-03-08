"""WSGI configuration for the MindLMS project.

Exposes the WSGI callable as the module-level variable ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application


# Set the default Django settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MindLMS.settings")


# Create the WSGI application used by production servers.
application = get_wsgi_application()