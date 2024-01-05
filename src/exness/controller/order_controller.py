from flask import Blueprint

bp = Blueprint('order_controller', __name__)

@bp.route('/hello')
def index():
    return "Hello from hello_controller!"
