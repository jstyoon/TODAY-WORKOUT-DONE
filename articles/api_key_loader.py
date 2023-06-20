from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import os, json

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())
def get_secret(setting):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)
    
weather_key = get_secret("WEATHER_KEY")
map_key = get_secret("GOOGLE_API_KEY")
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True