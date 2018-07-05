from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_babel import lazy_gettext as _l


class EditProfileForm(FlaskForm):
	username = StringField(_l('用户名'), validators=[DataRequired()])
	about_me = TextAreaField(_l('关于我'), validators=[Length(min=0, max=140)])
	submit = SubmitField(_l('提交'))

class PostForm(FlaskForm):
	post = TextAreaField(_l('说点什么'),validators=[DataRequired(),Length(min=1,max=140)])
	submit = SubmitField(_l('提交'))
