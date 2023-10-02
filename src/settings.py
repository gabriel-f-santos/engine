# This value should be generated and stored in an environment variable
import os


JWT_SECRET = "secret"
DB_CONNECT = os.getenv('DB_CONNECT')
DEBUG = int(os.getenv('DEBUG', "1"))
