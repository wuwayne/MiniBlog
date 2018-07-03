from datetime import datetime

from flask import render_template,flash,redirect,url_for,request,g
from flask_login import login_user,logout_user,current_user,login_required
from werkzeug.urls import url_parse
from flask_babel import _,get_locale
from flask_babel import lazy_gettext as _l

from app import app,db
from app.forms import LoginForm,RegistrationForm,EditProfileForm,PostForm,ResetPasswordRequestForm,\
ResetPasswordForm
from app.models import User,Post
from app.email import send_password_reset_email


@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.post.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(_("发布成功！"))
		return redirect(url_for('index'))

	page = request.args.get('page',1,type=int)
	posts = current_user.followed_posts().paginate(
		page,app.config['POSTS_PER_PAGE'],False)

	next_url = url_for('index',page=posts.next_num) if posts.has_next else None
	prev_url = url_for('index',page=posts.prev_num) if posts.has_prev else None

	return render_template('index.html', posts=posts.items,form=form,next_url=next_url,prev_url=prev_url)


@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash(_('用户名或密码错误！'))
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='登陆', form=form)


@app.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash(_('注册成功！'))
		return redirect(url_for('index'))
	return render_template('register.html',title='注册',form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()

	page = request.args.get('page',1,type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(
		page,app.config['POSTS_PER_PAGE'],False)

	next_url = url_for('user',username=username,page=posts.next_num) if posts.has_next else None
	prev_url = url_for('user',username=username,page=posts.prev_num) if posts.has_prev else None

	return render_template('user.html',user=user,posts=posts.items,next_url=next_url, prev_url=prev_url)



@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.locale = str(get_locale())
	if g.locale == 'zh':
		g.locale = 'zh_CN'

@app.route('/edit_profile',methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if not current_user.username == form.username.data and user :
			flash(_('用户名已被注册！'))
			return render_template('edit_profile.html', title='个人主页',form=form)
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash(_('修改成功！'))
		return redirect(url_for('user',username=current_user.username))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='个人主页',form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	# if user == current_user:
	# 	flash("不能关注自己！")
	# 	return redirect(url_for('user',username=username))
	current_user.follow(user)
	db.session.commit()
	flash(_("已成功关注%(username)s!",username=username))
	return redirect(url_for('user',username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	# if user == current_user:
	# 	flash("不能关注自己！")
	# 	return redirect(url_for('user',username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash(_("已取消关注%(username)s!",username=username))
	return redirect(url_for('user',username=username))


@app.route('/explore')
@login_required
def explore():
	page = request.args.get('page',1,type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(
		page,app.config['POSTS_PER_PAGE'],False)

	next_url = url_for('explore',page=posts.next_num) if posts.has_next else None
	prev_url = url_for('explore',page=posts.prev_num) if posts.has_prev else None

	return render_template('index.html',title='发现',posts=posts.items,next_url=next_url, prev_url=prev_url)

@app.route('/reset_password_request',methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
			flash(_("重置链接已发送至邮箱中！"))
			return redirect(url_for('login'))##到底跳转什么链接比较好？
		else:
			flash(_("该邮箱未注册！"))
			return redirect(url_for('reset_password_request'))
	return render_template('reset_password_request.html',title='重置密码',form=form)


@app.route('/reset_password/<token>',methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash(_("重置密码成功！"))
		return redirect(url_for('login'))
	return render_template('reset_password.html',form=form)