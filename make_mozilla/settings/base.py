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
    'django.contrib.gis',
    # Application base, containing global templates.
    'make_mozilla.base',
    # Events and Venues
    'make_mozilla.events',
    # UserProfiles
    'make_mozilla.users',
    # extra lib stuff
    'south',
    'django_browserid',  # Load after auth to monkey-patch it.
]


# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = [
    'admin',
]

# Browser ID
BROWSERID_CREATE_USER = True
# LOGIN_URL = '/'
# LOGIN_REDIRECT = 'flicks.videos.upload'
# LOGIN_REDIRECT_FAILURE = 'flicks.base.home'

AUTHENTICATION_BACKENDS = (
    'django_browserid.auth.BrowserIDBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS) + [
    'django_browserid.context_processors.browserid_form',
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

LOGGING = dict(loggers=dict(playdoh = {'level': logging.DEBUG}))
