from flask import render_template,flash,redirect,url_for,request,g
from flask_login import login_user,logout_user,current_user
from werkzeug.urls import url_parse
from flask_babel import _
from flask_babel import lazy_gettext as _l

from app import db
from .forms import LoginForm,RegistrationForm,ResetPasswordRequestForm,\
ResetPasswordForm
from app.models import User,Post
from .email import send_password_reset_email

from app.auth import bp


@bp.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash(_('用户名或密码错误！'))
			return redirect(url_for('auth.login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('main.index')
		return redirect(next_page)
	return render_template('login.html', title='登陆', form=form)


@bp.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash(_('注册成功！'))
		return redirect(url_for('main.index'))
	return render_template('register.html',title='注册',form=form)


@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))

@bp.route('/reset_password_request',methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
			flash(_("重置链接已发送至邮箱中！"))
			return redirect(url_for('auth.login'))##到底跳转什么链接比较好？
		else:
			flash(_("该邮箱未注册！"))
			return redirect(url_for('auth.reset_password_request'))
	return render_template('reset_password_request.html',title='重置密码',form=form)


@bp.route('/reset_password/<token>',methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('main.index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash(_("重置密码成功！"))
		return redirect(url_for('auth.login'))
	return render_template('reset_password.html',form=form)
