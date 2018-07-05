from flask_mail import Message
from flask import render_template,current_app

from app import mail

def send_mail(subject,sender,recipients,text_body,html_body):
	msg = Message(subject,sender=sender,recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	mail.send(msg)

def send_password_reset_email(user):
	token = user.get_reset_password_token()
	send_mail("[MiniBlog]重置密码",
			sender=current_app.config['MAIL_USERNAME'],
			recipients=[user.email],
			text_body=render_template('email/reset_password_zh.txt',user=user,token=token),
			html_body=render_template('email/reset_password_en.html',user=user,token=token))