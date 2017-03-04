import os

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

URL_API_T411 = "https://api.t411.li/"
USERNAME_T411 = ""
PASSWORD_T411 = ""
TOKEN_T411 = ''
TOKEN_T411_VALIDITY = ''
