from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import os


weather_key = os.environ.get("WEATHER_KEY")
map_key = os.environ.get("GOOGLE_API_KEY")

    
# weather_key = get_secret("WEATHER_KEY")
# map_key = get_secret("GOOGLE_API_KEY")
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True