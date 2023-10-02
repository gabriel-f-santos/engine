# This value should be generated and stored in an environment variable
import os


JWT_SECRET = "secret"
DB_CONNECT = os.getenv('DEBUG', True)
DEBUG = os.getenv('DEBUG', True)
