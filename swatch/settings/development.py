from .base import *

# DJANGO CRISPY FORMS
INSTALLED_APPS.append('crispy_forms')

# To not use cache in development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

REST_FRAMEWORK['TEST_REQUEST_DEFAULT_FORMAT'] = 'json'


# CELERY Settings
CELERY_BROKER_URL = 'pyamqp://admin:mypass@rabbit//'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

