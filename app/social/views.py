from flask import g,request,jsonify
from guess_language import guess_language
from flask_login import current_user

from app import db
from app.social import bp
from app.models import User,Post,Comment

@bp.route('/post_comment',methods=['POST'])
def post_comment():
	form = g.comment_form
	post_id = request.form['id']
	body = request.form['comment']
	post = Post.query.filter_by(id=post_id).first()
	language = guess_language(body)
	if language == 'UNKNOWN' or len(language) > 5:
		language = ''
	comment = Comment(body=body,language=language,post_id=int(post_id),user_id=current_user.id)
	db.session.add(comment)
	db.session.commit()

	return jsonify({
					'comment_num':post.comments.count(),
					'avatarURL':current_user.avatar(70),
					'comment_username':current_user.username,
		})