
# -*- coding: utf-8 -*-
import os.path



BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#根据环境定义数据库连接参数

mysql_name = 'z_db'
mysql_user = 'root'
mysql_pass = '888888'
mysql_host = ''
mysql_host_s = ''
mysql_port = ''


DEBUG = True
TEMPLATE_DEBUG = True


ALLOWED_HOSTS = []

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': mysql_name,                      # Or path to database file if using sqlite3.
        'USER': mysql_user,                      # Not used with sqlite3.
        'PASSWORD': mysql_pass,                  # Not used with sqlite3.
        'HOST': mysql_host,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': mysql_port,                      # Set to empty string for default. Not used with sqlite3.
    },

    'slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': mysql_name,                      # Or path to database file if using sqlite3.
        'USER': mysql_user,                      # Not used with sqlite3.
        'PASSWORD': mysql_pass,                  # Not used with sqlite3.
        'HOST': mysql_host_s,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': mysql_port,                      # Set to empty string for default. Not used with sqlite3.
    }
}

DATABASE_ROUTERS = ['zjblog.masterslaverouter.MasterSlaveRouter']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'#设置django界面语言

#SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = ''

#STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "static"),
        #'/var/www/static/',
)
STATICFILES_FINDERS = (
	"django.contrib.staticfiles.finders.FileSystemFinder",
	"django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'app!kn5fj5zlat%3gs)cu73be#mc3y+%$me5$dw6s2$(%i*tps'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',

)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.flatpages.middleware.flatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'mysite.urls'
WSGI_APPLICATION = 'mysite.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join('BASE_DIR','templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'mptt',#django-mptt
    'zjblog',
    'taggit',
    'captcha',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    
    
)



