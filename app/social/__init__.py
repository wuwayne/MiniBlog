from flask import Blueprint


bp = Blueprint('social',__name__,template_folder='templates')

from app.social import forms,views