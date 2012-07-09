from settings import *
INSTALLED_APPS.append('base')

ROOT_URLCONF = 'base.api.urls'
MEDIA_URL = 'http://localhost:8000/media/'

#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': True,
#    'handlers': {
#        'simple': {
#            'level': 'ERROR',
#            'class': 'base.utils.SimpleHandler',
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['simple'],
#            'level': 'ERROR',
#            'propagate': False,
#        },
#    }
#}
#
