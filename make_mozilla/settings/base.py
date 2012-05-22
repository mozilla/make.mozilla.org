# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import *

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'make_devices': (
            'css/ext/normalize.css',
            'css/base.less',
        ),
        'make_desktop': (
            'css/desktop.less',
        ),
    },
    'js': {
        'jquery': (
            'js/jquery-1.7.2.min.js',
            'js/jquery-ui-1.8.20.date.autocomplete.min.js',
        ),
        'core_js': (
            'js/core.js',
        ),
        'maps_js': (
            'js/map.js',
            'js/map.infobox.js',
        ),
        'example_js': (
            'js/examples/libs/jquery-1.4.4.min.js',
            'js/examples/libs/jquery.cookie.js',
            'js/examples/init.js',
        ),
    }
}

# Defines the views served for root URLs.
ROOT_URLCONF = 'make_mozilla.urls'

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'django.contrib.admin',
    'django.contrib.gis',
    # Application base, containing global templates.
    'make_mozilla.base',
    # Events and Venues
    'make_mozilla.events',
    # Tools
    'make_mozilla.tools',
    # UserProfiles
    'make_mozilla.users',
    # extra lib stuff
    'south',
    'django_browserid',  # Load after auth to monkey-patch it.
    'cronjobs',
    'waffle',
]

class Setting(object):
    def __init__(self, *args, **kwargs):
        vars(self).update(kwargs)

    @property
    def dict(self):
        return vars(self)


# Go! Go! Gadget Bleach!
BLEACH = Setting(
    allowed_tags = (
        'h1', 'h2', 'a', 'b', 'em', 'i', 'strong',
        'ol', 'ul', 'li', 'blockquote', 'p',
        'span', 'pre', 'code', 'img'
    ),
    allowed_attrs = {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title'],
    }
)


# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = [
    'gis',
    'admin',
]

# Browser ID
BROWSERID_CREATE_USER = True
BROWSERID_VERIFICATION_URL = 'https://browserid.org/verify'
LOGIN_REDIRECT_URL = '/events/'
LOGIN_URL = '/users/login/'
SITE_URL = 'https://make-dev.mozillalabs.com'

AUTH_PROFILE_MODULE = 'users.Profile'

AUTHENTICATION_BACKENDS = (
    'django_browserid.auth.BrowserIDBackend',
    'django.contrib.auth.backends.ModelBackend'
)

TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS) + [
    'django_browserid.context_processors.browserid_form',
]

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES) + [
    'waffle.middleware.WaffleMiddleware',
]

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['lhtml'] = [
#    ('**/templates/**.lhtml',
#        'tower.management.commands.extract.extract_tower_template'),
# ]

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['javascript'] = [
#    # Make sure that this won't pull in strings from external libraries you
#    # may use.
#    ('media/js/**.js', 'javascript'),
# ]

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
BROWSERID_CREATE_USER = True

# needed to make CSRF function on anonymous forms
ANON_ALWAYS = True
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': ['localhost:11211',],
        'KEY_PREFIX': 'make_mozilla'
    }
}

## Log settings
SYSLOG_TAG = "make_mozilla"  # Make this unique to your project.
LOGGING = {
    'loggers': {
        'mk': {
            'level': logging.DEBUG,
            'handlers': ['syslog', 'console']
        },
    }
}

BSD_EVENT_JSON_FEED_URLS = (
    ('hack_jam', 'https://donate.mozilla.org/page/event/search_results?format=json&wrap=no&orderby[0]=date&orderby[1]=desc&event_type=2&mime=application/json&limit=10&country=*'),
    ('kitchen_table', 'https://donate.mozilla.org/page/event/search_results?format=json&wrap=no&orderby[0]=date&orderby[1]=desc&event_type=1&mime=application/json&limit=10&country=*'),
    ('pop_up', 'https://donate.mozilla.org/page/event/search_results?format=json&wrap=no&orderby[0]=date&orderby[1]=desc&event_type=3&mime=application/json&limit=10&country=*'),
)

# Common Event Format logging parameters
#CEF_PRODUCT = 'Playdoh'
#CEF_VENDOR = 'Mozilla'

# Potentially sensitive or machine-specific values in the below should be overridden in make_mozilla/settings/local.py
UPLOADED_IMAGES = {
    'location': '/var/webapps/make.mozilla.org/shared/partner_media',
    'base_url': '/media/partner_media/'
}

BSD_API_DETAILS = {}

DATABASES = {
    'default': {
        'ENGINE': 'make_mozilla.postgis',
        'NAME': 'make_mozilla',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
        },
        'TEST_CHARSET': 'utf8',
    },
    # 'slave': {
    #     ...
    # },
}
SOUTH_DATABASE_ADAPTERS = {
    'default': "south.db.postgresql_psycopg2"
}

# Uncomment this and set to all slave DBs in use on the site.
# SLAVE_DATABASES = ['slave']

# CELERY_ALWAYS_EAGER = False  # required to activate celeryd
BROKER_URL = "redis://localhost:6379/0"
SITE_URL = 'http://localhost:8000'
