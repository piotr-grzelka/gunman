import os
from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['barrel-finder.gunman.pl']
SECRET_KEY = os.getenv('SECRET_KEY')

