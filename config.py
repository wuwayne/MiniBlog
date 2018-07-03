import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or r'N\x82\xe25\xae|@Ntp\xfa{\x8bIT\xe5\xadB\xfc\xb7\xed2"\x89'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir,'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

	ADMINS = ['wayne_we@163.com','wulove5@gmail.com']

	POSTS_PER_PAGE = 10

	LANGUAGES = ['en','zh']

