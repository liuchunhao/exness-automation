import time
from flask import Blueprint

bp = Blueprint('heartbeat', __name__)

@bp.route('/ping')
def index():
    return {
        "code": 200,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "msg": 'pong'
    }, 200
