import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/vote_app')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')