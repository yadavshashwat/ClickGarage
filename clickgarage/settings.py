"""
Django settings for clickgarage project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PRODUCTION = False
if os.getcwd()=='/home/ubuntu/beta/suigen':
    PRODUCTION = True

#connect('my_database', host='127.0.0.1', port=27017)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# PROJECT_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', '..'))
PROJECT_PATH = os.path.normpath(os.path.join(BASE_DIR, '..'))
# print PROJECT_PATH
print BASE_DIR
if PRODUCTION:
    WEBSITE_PATH = os.path.join(PROJECT_PATH, 'website')
else:
    WEBSITE_PATH = os.path.join(BASE_DIR,'../suigenwebsite')

# print WEBSITE_PATH
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# DATE_FORMAT = "dd-mm-YYYY"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(33s3+te*%e-h=*u%zh3b13gz7phh-talbz=+dut3_p03y_b-s'

AWS_UPLOAD_BUCKET_NAME = "dentingbucket"
AWS_UPLOAD_CLIENT_KEY = "AKIAICT2M5M5LIRAHWXQ"
AWS_UPLOAD_CLIENT_SECRET_KEY = "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"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'djangotoolbox',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'api',
    'activity',
    'dataEntry',
    'website',
    'mailing'
    ,'ajaxuploader',
    # 'djcelery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)


# STATIC_URL = BASE_DIR + '/website/static/'
STATIC_URL = WEBSITE_PATH + '/static/'
MOBILE_ROOT = WEBSITE_PATH + '/mobile/'

print "static = ", STATIC_URL
ROOT_URLCONF = 'clickgarage.urls'

print BASE_DIR
# MEDIA_ROOT = BASE_DIR + 'static/'
MEDIA_ROOT = WEBSITE_PATH + 'static/'

#def APP_MEDIA_ROOT(appName):
#    arrDir = MEDIA_ROOT.split('/')
#    arrDir[-1] = appName
#    appMediaDir = os.path.join('/'.join(arrDir), 'media')
#    return appMediaDir

# def TEMPLATES_ROOT(appName):
#     return os.path.join(BASE_DIR, appName, 'templates')

print os.path.join(BASE_DIR, 'website','templates')
print os.path.join(WEBSITE_PATH,'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [
        #     os.path.join(BASE_DIR, 'dataEntry', 'templates'),
        #     os.path.join(BASE_DIR, 'website', 'templates'),
        #     os.path.join(WEBSITE_PATH, 'templates'),
        # ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'social.apps.django_app.context_processors.backends',
                # 'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.load_template_source',
#     'django.template.loaders.app_directories.load_template_source'
# )
STATICFILES_DIRS = ( os.path.join(WEBSITE_PATH,'static'), )
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATE_DIRS = (
    os.path.join(WEBSITE_PATH,'templates')
)

print STATIC_URL
if PRODUCTION:
    WSGI_APPLICATION = 'clickgarage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
import socket
DB_NAME = 'test_clickg'
# if not PRODUCTION:
#     DB_NAME = 'test_clickg_testing'


if socket.gethostname().startswith('ip-'):
    if PRODUCTION:
        DATABASES = {
            'default': {
                'ENGINE' : 'django_mongodb_engine',
                'NAME' : DB_NAME,
                'USER': 'Clickadmin',
                'PASSWORD': 'DoctorWho?',
                'HOST': 'localhost',
                'PORT': 27017,
                'SUPPORTS_TRANSACTIONS': False,

        #        'ENGINE': 'django.db.backends.sqlite3',
        #        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django_mongodb_engine',
                'NAME': DB_NAME,
                'USER': 'Clickadmin',
                'PASSWORD': 'DoctorWho?',
                'HOST': 'localhost',
                'PORT': 27017,
                'SUPPORTS_TRANSACTIONS': False,

                #        'ENGINE': 'django.db.backends.sqlite3',
                #        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django_mongodb_engine',
            'NAME': DB_NAME,
            # 'USER': 'Clickadmin',
            # 'PASSWORD': 'DoctorWho?',
            'HOST': 'localhost',
            'PORT': 27017,
            'SUPPORTS_TRANSACTIONS': False,

            #        'ENGINE': 'django.db.backends.sqlite3',
            #        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

AUTH_USER_MODEL = 'activity.CGUserNew'

if PRODUCTION:
    AUTH_USER_MODEL = 'activity.CGUser'

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.google.GoogleOAuth2',
   'social.backends.twitter.TwitterOAuth',
    # 'activity.backends.ClientAuthBackend',
    'django.contrib.auth.backends.ModelBackend'
)
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

#social auth variable starts
# LOGIN_URL = '/login/'

LOGOUT_URL = 'https://www.clickgarage.in/'

LOGIN_REDIRECT_URL = 'https://www.clickgarage.in/'

LOGIN_ERORR_URL = '/'

SOCIAL_AUTH_FACEBOOK_KEY = '1394399690887901'
SOCIAL_AUTH_FACEBOOK_SECRET = '25f333e60b4b79990c9db69cc1a08276'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '280103750695-c5eiv9cp9hp4qoj3kdaa2eiajpa25sfo.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'nk0hnQ8_2AZhq3hyZS3rCrds'


SOCIAL_AUTH_USER_MODEL = 'activity.CGUser'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = 'https://www.clickgarage.in/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'https://www.clickgarage.in/'
SOCIAL_AUTH_COMPLETE_URL_NAME = 'https://www.clickgarage.in/complete/'

SOCIAL_AUTH_PIPELINE = (
    'activity.backends.clear_users',
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',

    'activity.backends.associate_by_email',

    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

# SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
# SOCIAL_AUTH_UID_LENGTH = 16
# SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
# SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
# SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
# SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
# SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook')
#
# FACEBOOK_APP_ID= '1394399690887901'
# FACEBOOK_API_SECRET= '25f333e60b4b79990c9db69cc1a08276'
#
#
# FACEBOOK_APP_AUTH = True
#


#social auth variable end
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'


# Celery
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# http://celery.readthedocs.org/en/latest/userguide/tasks.html#disable-rate-limits-if-they-re-not-used
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ALWAYS_EAGER = False #change to true for developement purposes
