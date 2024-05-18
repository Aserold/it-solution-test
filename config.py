import os
from dotenv import load_dotenv

load_dotenv()
SECRET = os.environ.get('SECRET')
DEBUG_DJ = os.environ.get('DEBUG')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
