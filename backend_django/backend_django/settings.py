from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key-here'  # Replace with a secure key
WSGI_APPLICATION = 'backend_django.wsgi.application'


# SECURITY WARNING: don’t run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    # Required Django apps
    'django.contrib.admin',
    'django.contrib.auth',          # Needed for Permission model
    'django.contrib.contenttypes',  # Needed for auth permissions
    'django.contrib.sessions',      # Optional but recommended
    'django.contrib.messages',      # Optional but recommended
   
    
    # Your custom apps
    'users',
    
    # Third-party apps
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required for auth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Disable auth system


ROOT_URLCONF = 'backend_django.urls'
CSRF_TRUSTED_ORIGINS = [
    "https://localhost:5173",
    "http://localhost:5173",
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # You can add Vue templates here if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend_django.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'parking.db',
    }
}

# Password validation

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True




# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings (for Vue.js or any frontend running on a different port)
CORS_ALLOW_ALL_ORIGINS = True  # Development only

JWT_SECRET = 'your_jwt_secret_here'
JWT_ALGORITHM = 'HS256'


