from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import lazy_gettext as _l

from app.models import User


class CommentForm(FlaskForm):
	comment = TextAreaField(_l('说点什么'),validators=[DataRequired(),Length(min=1,max=140)])
	submit = SubmitField(_l('提交'))