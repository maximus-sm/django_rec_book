from .base import *  # noqa
from environs import Env  # new

# env = Env()  # new
# env.read_env()  # new
# env.read_env(".env.test", recurse=False)
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
SECRET_KEY = os.getenv("SECRET_KEY", "development_env")
CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
]
