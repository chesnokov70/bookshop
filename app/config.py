import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@db/bookstore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
