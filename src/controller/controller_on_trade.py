from flask import Blueprint

bp = Blueprint('heartbeat', __name__)

@bp.route('/ping')
def index():
    return "pong", 200
