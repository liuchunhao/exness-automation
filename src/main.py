
from flask import Flask, request, abort, g
from flask_cors import CORS

from controller import controller_withdraw

app = Flask(__name__)
CORS(app)


# registered controllers
app.register_blueprint(controller_withdraw.bp)

@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return {
        "code": -1,
        "msg": f"{err}",
        "data": []
    }, 200


if __name__ == '__main__':
    app.run(port=5100, debug=True)
