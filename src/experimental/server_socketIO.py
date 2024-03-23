# app.py
import datetime
from flask import Flask
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# @app.route('/')
# def home():
#     return render_template('home.html')

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: ")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: ")

@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    send(msg, broadcast=True)

@socketio.on('timestamp')
def handle_timestamp():
    while True:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emit('timestamp', {'timestamp': timestamp})
        socketio.sleep(10)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5200, use_reloader=True, log_output=True)

