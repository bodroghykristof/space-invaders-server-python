from flask import Flask, render_template, url_for, request, redirect, session, jsonify, json, flash
from flask_socketio import SocketIO, join_room, leave_room, emit, close_room
import json
from room import Room
from datetime import datetime
from gevent import monkey

monkey.patch_all()

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

count = 0
rooms = []


@socketio.on('create')
def create_room(room_name):
    global count
    count += 1
    rooms.append(Room(count, room_name, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    join_room(count)
    emit("set_own_room", count)


@socketio.on('join')
def join_game_room(room_id):
    join_room(room_id)


@app.route("/list")
def list_all_rooms():
    return json.dumps([room.__dict__ for room in rooms])


@socketio.on('game_data')
def stream_game_data(data):
    game_data = json.loads(data)
    emit("game_data", data, room=game_data.get('roomId'), include_self=False)


@socketio.on('owner_exit')
def finish_game(room_id):
    emit("game_over", room=room_id)
    close_room(room_id)
    rooms.remove([room for room in rooms if room.room_id == room_id][0])


@socketio.on('spectator_exit')
def exit_spectator(room_id):
    leave_room(room_id)


if __name__ == '__main__':
    socketio.run(app)

