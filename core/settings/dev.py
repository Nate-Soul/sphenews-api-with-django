from .base import *

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#email set up
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_HOST_USER = '8fec1a1c408e93'
EMAIL_HOST_PASSWORD = 'eb06629eafe9e7'
DEFAULT_FROM_EMAIL = 'support@sphenews.com'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOWED_CREDENTIALS = True
