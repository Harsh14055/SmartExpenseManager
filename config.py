import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///expenses.db'

SECRET_KEY = "123456"  # Needed for session management

SQLALCHEMY_TRACK_MODIFICATIONS = False
