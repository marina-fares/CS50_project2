import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room


app = Flask(__name__)
socketio=SocketIO(app)

@app.route("/")
def index():
    return render_template("signin.html")

@app.route('/chat',methods=["POST"])
def chat():
    roomName = request.form.get('username')
    roomId = request.form.get('room')

    return render_template('welcome.html',room=roomId,username=roomName)



@socketio.on('join_room')
def handle_join_room_event(data):   
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement',data)

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],data['room'],data['message']))
    socketio.emit('receive_message', data, room=data['room'])

socketio.run(app,debug=True)