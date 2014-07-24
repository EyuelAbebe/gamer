from configurations import Configuration


class Common(Configuration):
    u"""
    Django settings for chessfellows project.

    For more information on this file, see
    https://docs.djangoproject.com/en/1.6/topics/settings/

    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/1.6/ref/settings/
    """

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'uw2071e1jt(zlsqoq&9*ikayz74_(rk@e^45cronly8!ot8c7x'

    ALLOWED_HOSTS = []


    # Application definition

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'south',
        'chess',
        'rest_framework',
        'registration',
        'bootstrap3',
        'chatrooms',
        'polymorphic',
        'gunicorn',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'chessfellows.urls'

    WSGI_APPLICATION = 'chessfellows.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'gamerdb',
            'USER': 'codefellow',
            'PASSWORD': 'codefellow',
            'HOST': 'gamer.ccjdipvshbwe.us-west-2.rds.amazonaws.com',
            'PORT': '5432'
        }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = '../chessfellows/uploaded_images'
    MEDIA_URL = '/media/'

    EMAIL_USE_TLS = True
    with open(os.path.join(BASE_DIR, 'access/email.txt')) as f:
        EMAIL_HOST = f.readline().strip()
        EMAIL_PORT = f.readline().strip()
        EMAIL_HOST_USER = f.readline().strip()
        EMAIL_HOST_PASSWORD = f.readline().strip()
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

    ACCOUNT_ACTIVATION_DAYS = 7
    CHATROOMS_HANDLERS_CLASS = 'chatrooms.utils.handlers.MessageHandler'

class Dev(Common):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
