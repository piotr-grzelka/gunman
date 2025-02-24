from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['barrel-finder.gunman.pl', 'testy.gunman.pl']
SECRET_KEY = os.getenv('SECRET_KEY')

