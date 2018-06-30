from datetime import datetime

from flask import render_template,flash,redirect,url_for,request
from flask_login import login_user,logout_user,current_user,login_required
from werkzeug.urls import url_parse

from app import app,db
from app.forms import LoginForm,RegistrationForm,EditProfileForm,PostForm
from app.models import User,Post


@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.post.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash("发布成功！")
		return redirect(url_for('index'))
	posts = current_user.followed_posts().all()
	return render_template('index.html', posts=posts,form=form)


@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('用户名或密码错误！')
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
		flash('注册成功！')
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
	posts = user.posts
	return render_template('user.html',user=user,posts=posts)


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


@app.route('/edit_profile',methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if not current_user.username == form.username.data and user :
			flash('用户名已被注册！')
			return render_template('edit_profile.html', title='个人主页',form=form)
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('修改成功！')
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
	flash("已成功关注{}!".format(username))
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
	flash("已取消关注{}!".format(username))
	return redirect(url_for('user',username=username))