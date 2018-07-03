from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_babel import lazy_gettext as _l

from app.models import User

class LoginForm(FlaskForm):
	username = StringField(_l('用户名'),validators=[DataRequired()])
	password = PasswordField(_l('密码'),validators=[DataRequired()])
	remember_me = BooleanField(_l('记住我'))
	submit = SubmitField(_l('提交'))

class RegistrationForm(FlaskForm):
	username = StringField(_l('用户名'),validators=[DataRequired()])
	email = StringField(_l('邮箱'),validators=[DataRequired(),Email()])	
	password = PasswordField(_l('密码'),validators=[DataRequired()])
	password2 = PasswordField(_l('确认密码'),validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField(_l('提交'))

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError(_l('用户名已被注册！'))

	def validate_email(self,email):
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError(_l('邮箱已被注册！'))

class EditProfileForm(FlaskForm):
	username = StringField(_l('用户名'), validators=[DataRequired()])
	about_me = TextAreaField(_l('关于我'), validators=[Length(min=0, max=140)])
	submit = SubmitField(_l('提交'))

class PostForm(FlaskForm):
	post = TextAreaField(_l('说点什么'),validators=[DataRequired(),Length(min=1,max=140)])
	submit = SubmitField(_l('提交'))

class ResetPasswordRequestForm(FlaskForm):
	email = StringField(_l('邮箱'), validators=[DataRequired(), Email()])
	submit = SubmitField(_l('提交'))

class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('密码'), validators=[DataRequired()])
	password2 = PasswordField(
		_l('确认密码'), validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField(_l('提交'))
