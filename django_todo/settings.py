from pathlib import Path  # Importing the Path class to manage filesystem paths easily
import os  # Importing the os module to access environment variables and handle file paths
import dj_database_url  # Importing dj_database_url to easily parse the database URL from environment variables
from dotenv import load_dotenv

load_dotenv()

# Determine if the application is running in development mode
development = os.environ.get('DEVELOPMENT') == "True"

# Define the base directory of the project (2 levels up from the current file)
BASE_DIR = Path(__file__).resolve().parent.parent

# Retrieve the secret key for Django from environment variables (ensure it is kept secret in production)
SECRET_KEY = os.environ.get('SECRET_KEY')

# Enable or disable debug mode based on the environment (development mode should have DEBUG=True)
DEBUG = development

# Define the allowed hosts for the application (retrieve from environment or default to 'localhost')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")

print(f"Development mode: {development}")
print(f"SECRET_KEY: {SECRET_KEY}")
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")

# Database configuration (switch between SQLite for development and a database URL for production)
if development:
    # Use SQLite as the default database in development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    # Retrieve the database URL from environment variables
    DATABASE_URL = os.environ.get('DATABASE_URL')

    # Убедимся, что DATABASE_URL — это строка, а не байты
    if not isinstance(DATABASE_URL, str):
        raise ValueError("DATABASE_URL must be a string.")

    # Parse the database URL and set it as the default database configuration
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }

# Define the installed apps (including Django's built-in apps and your custom apps)
INSTALLED_APPS = [
    'django.contrib.admin',  # Admin site
    'django.contrib.auth',  # Authentication system
    'django.contrib.contenttypes',  # Content types framework
    'django.contrib.sessions',  # Session framework
    'django.contrib.messages',  # Messaging framework
    'django.contrib.staticfiles',  # Static files handling
    'todo',  # Custom app for managing TODO tasks
]

# Define middleware (processes requests and responses)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',  # Common HTTP utilities
    'django.middleware.csrf.CsrfViewMiddleware',  # Protect against CSRF attacks
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication support
    'django.contrib.messages.middleware.MessageMiddleware',  # Messaging support
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Prevent clickjacking attacks
]

# Define the root URL configuration module
ROOT_URLCONF = 'django_todo.urls'

# Configure templates (how Django renders HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Use Django's template engine
        'DIRS': [],  # Directories where Django will search for templates
        'APP_DIRS': True,  # Automatically load templates from each app's "templates" directory
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Add debug context processor
                'django.template.context_processors.request',  # Add request context processor
                'django.contrib.auth.context_processors.auth',  # Add authentication context processor
                'django.contrib.messages.context_processors.messages',  # Add messaging context processor
            ],
        },
    },
]

# WSGI application (entry point for WSGI-compatible web servers)
WSGI_APPLICATION = 'django_todo.wsgi.application'

# Password validation settings (enforce security policies for user passwords)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Prevent passwords similar to user attributes
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Enforce minimum password length
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Prevent commonly used passwords
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Prevent passwords that are entirely numeric
    },
]

# Internationalization and localization settings
LANGUAGE_CODE = 'en-us'  # Default language code
TIME_ZONE = 'UTC'  # Default timezone
USE_I18N = True  # Enable Django's translation system
USE_L10N = True  # Enable localization of data formats
USE_TZ = True  # Enable timezone-aware datetime objects

# Static files (CSS, JavaScript, Images) settings
STATIC_URL = '/static/'  # URL prefix for serving static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory where static files will be collected

# Default primary key field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'