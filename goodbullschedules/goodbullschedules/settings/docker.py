from .base import *

SECRET_KEY = open("/run/secrets/SECRET_DJANGO_KEY").read()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "goodbullschedules",
        "USER": open("/run/secrets/SECRET_POSTGRES_USER").read(),
        "PASSWORD": open("/run/secrets/SECRET_POSTGRES_PASS").read(),
        "HOST": "db",
    }
}

# Caching settings

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "TIMEOUT": 60 * 60,  # 1 hour
    }
}

# Elasticsearch settings

ELASTICSEARCH_DSL = {"default": {"hosts": "http://elasticsearch:9200"}}
