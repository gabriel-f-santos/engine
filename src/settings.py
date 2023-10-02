# This value should be generated and stored in an environment variable
import os


JWT_SECRET = "secret"
DEBUG = os.getenv('DEBUG', True)
