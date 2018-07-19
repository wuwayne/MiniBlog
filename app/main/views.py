from datetime import datetime

from flask import render_template,flash,redirect,url_for,request,g,jsonify
from flask_login import login_user,logout_user,current_user,login_required
from werkzeug.urls import url_parse
from flask_babel import _,get_locale
from flask_babel import lazy_gettext as _l
from guess_language import guess_language
from flask import current_app

from app import db
from .forms import EditProfileForm,PostForm
from app.models import User,Post
from app.translate import translate
from app.main import bp
from app.social.forms import CommentForm

@bp.route('/',methods=['GET', 'POST'])
@bp.route('/index',methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	if form.validate_on_submit():
		language = guess_language(form.post.data)
		if language == 'UNKNOWN' or len(language) > 5:
			language = ''
		post = Post(body=form.post.data,author=current_user,language=language)
		db.session.add(post)
		db.session.commit()
		flash(_("发布成功！"))
		return redirect(url_for('main.index'))

	page = request.args.get('page',1,type=int)
	posts = current_user.followed_posts().paginate(
		page,current_app.config['POSTS_PER_PAGE'],False)

	next_url = url_for('main.index',page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.index',page=posts.prev_num) if posts.has_prev else None

	return render_template('index.html', posts=posts.items,form=form,next_url=next_url,prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page',1,type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(
		page,current_app.config['POSTS_PER_PAGE'],False)

	next_url = url_for('main.user',username=username,page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.user',username=username,page=posts.prev_num) if posts.has_prev else None

	return render_template('user.html',user=user,posts=posts.items,next_url=next_url, prev_url=prev_url)


@bp.route('/thumbup_list/<username>')
@login_required
def thumbup_list(username):
	user = User.query.filter_by(username=username).first_or_404()	
	page = request.args.get('page',1,type=int)
	thumbeds = user.thumbed.paginate(
		page,current_app.config['FOLLOWEDS_AND_FOLLWERS_PER_PAGE'],False)	

	next_url = url_for('main.thumbup_list',username=username,page=thumbeds.next_num) if thumbeds.has_next else None
	prev_url = url_for('main.thumbup_list',username=username,page=thumbeds.prev_num) if thumbeds.has_prev else None

	return render_template('user.html',user=user,posts=thumbeds.items,next_url=next_url, prev_url=prev_url)


@bp.route('/star_list/<username>')
@login_required
def star_list(username):
	user = User.query.filter_by(username=username).first_or_404()	
	page = request.args.get('page',1,type=int)
	stareds = user.stared.paginate(
		page,current_app.config['FOLLOWEDS_AND_FOLLWERS_PER_PAGE'],False)	

	next_url = url_for('main.star_list',username=username,page=stareds.next_num) if stareds.has_next else None
	prev_url = url_for('main.star_list',username=username,page=stareds.prev_num) if stareds.has_prev else None

	return render_template('user.html',user=user,posts=stareds.items,next_url=next_url, prev_url=prev_url)


@bp.route('/follower_list/<username>')
@login_required
def follower_list(username):
	user = User.query.filter_by(username=username).first_or_404()	
	page = request.args.get('page',1,type=int)
	followers = user.followers.paginate(
		page,current_app.config['FOLLOWEDS_AND_FOLLWERS_PER_PAGE'],False)

	next_url = url_for('main.follower_list',username=username,page=followers.next_num) if followers.has_next else None
	prev_url = url_for('main.follower_list',username=username,page=followers.prev_num) if followers.has_prev else None

	return render_template('user.html',user=user,followers=followers.items,next_url=next_url, prev_url=prev_url)


@bp.route('/followed_list/<username>')
@login_required
def followed_list(username):
	user = User.query.filter_by(username=username).first_or_404()	
	page = request.args.get('page',1,type=int)
	followeds = user.followed.paginate(
		page,current_app.config['FOLLOWEDS_AND_FOLLWERS_PER_PAGE'],False)

	next_url = url_for('main.followed_list',username=username,page=followeds.next_num) if followeds.has_next else None
	prev_url = url_for('main.followed_list',username=username,page=followeds.prev_num) if followeds.has_prev else None

	return render_template('user.html',user=user,followeds=followeds.items,next_url=next_url, prev_url=prev_url)


@bp.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
		g.comment_form = CommentForm()
	g.locale = str(get_locale())
	# if g.locale == 'zh':
	# 	g.locale = 'zh_CN'


@bp.route('/edit_profile',methods=['GET', 'POST'])
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
		return redirect(url_for('main.user',username=current_user.username))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='个人主页',form=form)


@bp.route('/follow',methods=['POST'])
@login_required
def follow():
	username = request.form['user']
	user = User.query.filter_by(username=username).first()
	# if user == current_user:
	# 	flash("不能关注自己！")
	# 	return redirect(url_for('main.user',username=username))
	current_user.follow(user)
	db.session.commit()
	# flash(_("已成功关注%(username)s!",username=username))
	# return redirect(url_for('main.user',username=username))
	return jsonify({'state':_("已成功关注%(username)s!",username=username),
					'follower_num':user.followers.count(),
		})


@bp.route('/unfollow',methods=['POST'])
@login_required
def unfollow():
	username = request.form['user']
	user = User.query.filter_by(username=username).first()
	# if user == current_user:
	# 	flash("不能关注自己！")
	# 	return redirect(url_for('user',username=username))
	current_user.unfollow(user)
	db.session.commit()
	# flash(_("已取消关注%(username)s!",username=username))
	# return redirect(url_for('main.user',username=username))
	return jsonify({'state':_("已取消关注%(username)s!",username=username),
					"follower_num":user.followers.count(),
		})


@bp.route('/thumb_up',methods=['POST'])
@login_required
def thumb_up():
	id = request.form['post_id']
	post = Post.query.filter_by(id=id).first()
	current_user.thumb(post)
	db.session.commit()

	return jsonify({
				'thumbers_num':post.thumbers.count(),
				'thumbed_num':current_user.thumbed.count()
		})


@bp.route('/thumb_down',methods=['POST'])
@login_required
def thumb_down():
	id = request.form['post_id']
	post = Post.query.filter_by(id=id).first()
	current_user.unthumb(post)
	db.session.commit()
	
	return jsonify({
				'thumbers_num':post.thumbers.count(),
				'thumbed_num':current_user.thumbed.count()
		})


@bp.route('/star',methods=['POST'])
@login_required
def star():
	id = request.form['post_id']
	post = Post.query.filter_by(id=id).first()
	current_user.star(post)
	db.session.commit()

	return jsonify({

				'stared_num':current_user.stared.count()
		})


@bp.route('/unstar',methods=['POST'])
@login_required
def unstar():
	id = request.form['post_id']
	post = Post.query.filter_by(id=id).first()
	current_user.unstar(post)
	db.session.commit()

	return jsonify({

				'stared_num':current_user.stared.count()
		})



@bp.route('/explore')
@login_required
def explore():
	page = request.args.get('page',1,type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(
		page,current_app.config['POSTS_PER_PAGE'],False)

	next_url = url_for('main.explore',page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.explore',page=posts.prev_num) if posts.has_prev else None

	return render_template('index.html',title='发现',posts=posts.items,next_url=next_url, prev_url=prev_url)


@bp.route('/translate',methods=['POST'])
@login_required
def translate_text():
	return jsonify({'text': translate(request.form['text'],
									  request.form['source_language'],
									  request.form['dest_language'])})

