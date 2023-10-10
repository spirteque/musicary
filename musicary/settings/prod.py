from .base import *

DEBUG = False

ADMINS = (
    ('spirteque', 'musicary23@gmail.com'),
)

ALLOWED_HOSTS =['127.0.0.1', 'localhost']


STATIC_ROOT= "/var/www/musicary/static/"
MEDIA_ROOT = "/var/www/musicary/media/"


SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_SECONDS=3600
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True