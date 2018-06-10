from flask import (
	Blueprint, flash, g, redirect, render_template, request, session,url_for,abort
)
import time
from werkzeug.security import check_password_hash, generate_password_hash
from KBS.db import get_db

bp = Blueprint('views', __name__)

@bp.route('/hello/<name>')
def hello(name):
	if name:
		return "Hello %s!"%name
	else:
		return "Hello world!"


def login_required(view):
	"""View decorator that redirects anonymous users to the login page."""
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('views.login'))

		return view(**kwargs)

	return wrapped_view


@bp.before_request
def load_logged_in_user():
	"""If a user id is stored in the session, load the user object from
	the database into ``g.user``."""
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id = ?', (user_id,)
		).fetchone()


@bp.route('/')
def index():
	"""Show all the posts, most recent first."""
	if g.user:
		db = get_db()
		posts = db.execute(
			'SELECT p.id, title, body, created, author_id, username'
			' FROM post p JOIN user u ON p.author_id = u.id'
			' ORDER BY created DESC'
		).fetchall()
		return render_template('index.html', posts=posts)
	else:
		return redirect(url_for('views.login'))


@bp.route('/login/', methods=('GET', 'POST'))
def login():
	"""Log in a registered user by adding the user id to the session."""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username,)
		).fetchone()


		if not (user and check_password_hash(user['password'], password)):
			error = '用户名或密码错误！'

		if error is None:
			# store the user id in a new session and return to the index
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('views.index'))

		flash(error)

	return render_template('login.html')

@bp.route('/register/', methods=('GET', 'POST'))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = '\"{0}\"已被占用！'.format(username)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            flash("注册成功！")
            time.sleep(2)
            return redirect(url_for('views.index'))

        flash(error)

    return render_template('register.html')

@bp.route('/logout/')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('signin'))