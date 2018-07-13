import os

class Default():
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = True