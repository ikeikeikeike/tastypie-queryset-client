import os

ADMINS = (
    ('test@example.com', 'Test User'),
)

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

MEDIA_ROOT = os.path.normpath(os.path.join(BASE_PATH, 'media'))

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'queryset_client.db'
TEST_DATABASE_NAME = 'queryset_client-test.db'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'TEST_NAME': TEST_DATABASE_NAME,
    }
}


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
#    'queryset_client',
]

DEBUG = True
TEMPLATE_DEBUG = DEBUG
CACHE_BACKEND = 'locmem://'
SECRET_KEY = 'verysecret'