from .base import *
from environs import Env  # new

env = Env()  # new
env.read_env()  # new

DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
SECRET_KEY = os.getenv("SECRET_KEY")
