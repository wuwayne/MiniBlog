import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or r'21ed213red23r'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir,'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = os.environ.get('MAIL_PORT')
	MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') 
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') 
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['wayne_we@163.com','wulove5@gmail.com']

	MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

	POSTS_PER_PAGE = 20
	FOLLOWEDS_AND_FOLLWERS_PER_PAGE = 20

	LANGUAGES = ['en','zh']

