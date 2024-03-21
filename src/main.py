
from flask import Flask, request, abort, g
from flask_cors import CORS

from controller import controller_heartbeat
from controller import controller_withdraw
from controller import controller_order
from controller import controller_account
from controller import controller_position


app = Flask(__name__)
CORS(app)


# registered controllers
app.register_blueprint(controller_heartbeat.bp)
app.register_blueprint(controller_withdraw.bp)
app.register_blueprint(controller_order.bp)
app.register_blueprint(controller_account.bp)
app.register_blueprint(controller_position.bp)


@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return {
        "code": -1,
        "msg": f"{err}",
        "data": []
    }, 200


if __name__ == '__main__':
    from service.exness_order import init
    init()

    app.run(port=5100, debug=True)
