import os
import logging

import django

# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'p64lp^$x%06_t86ze-x)rypuvf8w_fc1)tz6=j*1$=r%127&%)'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'http_debug.urls'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
)

# specify the base log file name
# this will be appended to by the name of the log
# to determine the log file names
LOG_FILE = os.path.join(SITE_ROOT, 'log') + '/application'

# choose level from logging.DEBUG, logging.INFO, logging.ERROR, logging.CRITICAL
LOG_LEVEL = logging.DEBUG

# maximum size of each individual log file
MAX_LOG_FILE_SIZE = 1000000

# you can define a number of different named logs here
# each will have it's own set of files 
LOGS = (
    'access',
    'error',
)

# we have log file rotation in place so we need to
# specify the number of files we should rotate between
NUMBER_LOG_FILES = 5

# we might want to filter out some patterns we don't care
# about. For instance if making requests from a browser you might
# want to filter out lots of requests for favicon.ico
REQUEST_EXCLUDES = (
    'favicon.ico',
)