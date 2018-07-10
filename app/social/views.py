from app.models import User,Post
from guess_language import guess_language

from app.social import bp

@bp.route('/comment',methods=['POST'])
def comment(post_id):
	form = g.comment_form
	if form.validate_on_submit():
		language = guess_language(form.post.data)
		if language == 'UNKNOWN' or len(language) > 5:
			language = ''
		comment = Comment(body=form.post.data,language=language,post_id=int(post_id),user_id=current_user.id)
		db.session.add(comment)
		db.session.commit()
