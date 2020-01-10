from flask import (
    Blueprint, flash,g, redirect ,render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from .auth import authorize
from .db import get_dbsession
from .db import User_zwq

bp = Blueprint('blog', __name__)

@bp.route('/')
@authorize
def index():
    user = get_dbsession().query(User_zwq.id, User_zwq.pwd).filter_by(id=session.get("user_id")).first()
    return str(user.id)