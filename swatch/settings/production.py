from .base import *

# Error reporting
ADMINS = ast.literal_eval(get_env_variable('ADMINS'))
MANAGERS = ast.literal_eval(get_env_variable('MANAGERS'))
SERVER_MAIL = get_env_variable('SERVER_MAIL')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Django SMTP Email settings
EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_PORT = get_env_variable('EMAIL_PORT')
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = get_env_variable('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = get_env_variable('DEFAULT_FROM_EMAIL')

# To use write-through cache for session data storage
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)