import os
from decouple import config

from django.utils.timezone import utc
import datetime
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# def get_env_variable(var_name):
#     try:
#         return os.environ[var_name]
#     except KeyError:
#         error_msg = "Set the %s environment variable" % var_name
#         raise ImproperlyConfigured(error_msg)


SECRET_KEY = config('SECRET_KEY')


# DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'help.localhost', '192.168.200.105']
# ALLOWED_HOSTS = []
# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'robots',
    'seo',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'ckeditor',
    'ckeditor_uploader',
    'taggit',
    'crispy_forms',
    'hitcount',
    'analytical',
    'sorl.thumbnail',
    'newsletter',

    'darisset.apps.blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # seo
    'seo.middleware.url_seo_middleware',
]

ROOT_URLCONF = 'darisset.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'seo.context_processors.seo',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1
# SITE_ID = 2

WSGI_APPLICATION = 'darisset.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# language

LANGUAGES = (
    ('en', _('English')),
    ('id', _('Indonesia')),
)


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# location


now_naive = datetime.datetime.now()
now_aware = datetime.datetime.utcnow().replace(tzinfo=utc)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Dropbox
#DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
#DROPBOX_OAUTH2_TOKEN = 'yRUcUf2MFtEAAAAAAAAAAeDFkkbTDFD9Dk97AtHK2CvllwycrpOhoZ1Pzvi_DmuG'
#DROPBOX_ROOT_PATH = '/media/'

# Media
MEDIA_URL = "/media/"
#MEDIA_URL = DROPBOX_ROOT_PATH
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Allauth
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'  # default to /accounts/profile
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True

# Provaider facebook
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12',
    }
}

# Email Backend

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# Ckeditor

CKEDITOR_UPLOAD_PATH = "blog/post/images/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'heigth': '100hv',
        'width': '100%',
        'toolbar_Custom': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline',
                'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BgColor'],
            ['Smiley', 'SpecialChar'], ['Source']
        ],
        'toolbar': 'Special',
        'tollbar_Special': [
            ['CodeSnippet', 'Youtube'],
        ],
        # 'extraPlugins': ',' .join(['codesnippet', 'youtube']),
    }
}


# Newsletter
NEWSLETTER_CONFIRM_EMAIL = True

NEWSLETTER_RICHTEXT_WIDGET = "ckeditor.widgets.CKEditorWidget"

# Amount of seconds to wait between each email. Here 100ms is used.
NEWSLETTER_EMAIL_DELAY = 0.1


# Crispy Form tags
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Hitcount
HITCOUNT_KEEP_HIT_ACTIVE = {'days': 7}
HITCOUNT_HITS_PER_IP_LIMIT = 0
HITCOUNT_EXCLUDE_USER_GROUP = ('penulis',)
HITCOUNT_KEEP_HIT_IN_DATABASE = {'days': 30}


# reCaptcha
GOOGLE_RECAPTCHA_SECRET_KEY = config('RECAPTCHA')

# Robots
ROBOTS_CACHE_TIMEOUT = 60 * 60 * 24
ROBOTS_USE_SCHEME_IN_HOST = True

# Seo
SEO_VIEWS_CHOICES = (
    ('index', 'Index'),
    ('faq', 'Faq'),
)

SEO_MODELS = [
    'blog.post',
    'auth.user',
    'flatpages.flatpage'
]

SEO_HTML_ADMIN_WIDGET = {
    'widget': 'CKEditor',
    'widget_path': 'ckeditor.widgets.CKEditorWidget'
}

GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-162553650-2'
