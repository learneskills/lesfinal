"""
WSGI config for webproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import whitenoise.django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webproject.settings")

application = get_wsgi_application()


application = whitenoise.django.DjangoWhiteNoise(application)
