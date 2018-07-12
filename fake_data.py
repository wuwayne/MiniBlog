from faker import Faker
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import random

from app.models import User,Post,Comment

basedir = os.path.abspath(os.path.dirname(__file__))


# print(fake.company_email())
# print(fake.name())
# print(fake.license_plate())
# print(fake.locale())
# print(generate_password_hash('1'))


def create_session():
	engine = create_engine('sqlite:///' + os.path.join(basedir,'app.db'))
	DBSession = sessionmaker(bind=engine)
	session = DBSession()

	return session


def add_user(n,locale='zh_CN'):
	session = create_session()
	fake = Faker(locale)

	for _ in range(n):
		user = User(username=fake.name(),email=fake.company_email(),password_hash=generate_password_hash('1'))
		session.add(user)
	try:
		session.commit()
	except Exception as e:
		pass
	session.close()

def add_post(n,locale='zh_CN'):
	session = create_session()
	fake = Faker(locale)
	user_num = session.query(User.id).count()
	for _ in range(n):
		post = Post(user_id=random.randint(1,user_num),body=fake.text())
		session.add(post)
	try:
		session.commit()
	except Exception as e:
		pass
	session.close()	

def add_comment(n,locale='zh_CN'):
	session = create_session()
	fake = Faker(locale)

	user_num = session.query(User.id).count()
	post_num = session.query(Post.id).count()

	for _ in range(n):
		comment = Comment(user_id=random.randint(1,user_num),post_id=random.randint(1,post_num),body=fake.text())
		session.add(comment)

	try:
		session.commit()
	except Exception as e:
		pass
	session.close()


if __name__ == '__main__':
	# add_user(100)
	# add_post(1000)
	add_comment(10000)