from flask import Flask, render_template, url_for, request, redirect, session, jsonify, json, flash
from flask_socketio import SocketIO, join_room, leave_room, emit
import json
from gevent import monkey

monkey.patch_all()

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)


@socketio.on('join')
def create_room(data):
    print('JOINED TO: ' + str(data))
    emit('newclient', broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
