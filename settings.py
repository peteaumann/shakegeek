import os.path
# Django settings for shakegeek project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'shakegeekdb'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = "C:/Python25/PyPro/shakegeek/site_media/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://localhost:8000/audio/'
MEDIA_URL = "http://localhost:8000/site_media/"
	
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7+9l+wz+kc1mbl+e4(34i8=_n=7jv7lbi&p#z&d--v=pvr)6ep'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'shakegeek.urls'

TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(__file__), 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.comments',
    'shakegeek.geek',    
)

LOGIN_URL = '/login/'

SITE_HOST = '127.0.0.1:8000'

# NOT YET, PERHAPS ANOTHER DAY
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.webfaction.com'
#EMAIL_PORT = '25'
#EMAIL_HOST_USER = 'pete_aumann'
#EMAIL_HOST_PASSWORD = 'Chino2010'
#DEFAULT_FROM_EMAIL = 'pete.aumann@gmail.com'
#SERVER_EMAIL = 'pete.aumann@gmail.com'

# THIS SETUP WORKS DIRECTLY WITH GMAIL
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'pete.aumann@gmail.com'
EMAIL_HOST_PASSWORD = 'Chino2008'
EMAIL_PORT = 587
#WORKS DEFAULT_FROM_EMAIL = 'pete.aumann@gmail.com'
DEFAULT_FROM_EMAIL = 'pete_aumann@shakegeek.com'
#WORKS SERVER_EMAIL = 'pete.aumann@gmail.com'
SERVER_EMAIL = 'pete_aumann@shakegeek.com'

AUTHENTICATION_BACKENDS = (
    'shakegeek.email-auth.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
 )