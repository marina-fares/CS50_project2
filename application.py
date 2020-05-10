import os
import requests
import numpy as np
import json

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from models import *

from db_fun import *

#init application
app = Flask(__name__)
socketio=SocketIO(app)

#init database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///chatdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def signin():
    return render_template("signin.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")
'''
@app.route("/star")
def start():
    return render_template("start.html")
'''
@app.route("/viewroom/<username>/<roomname>")
def ViewRoom(username,roomname):
    members=get_room_members(roomname)
    room= Room.query.filter_by(name=roomname).first()
    if username not in members:
        add_room_member(roomname, username)
    list_of_messages = get_messages(roomname)
    return render_template("chat.html",roomname=roomname,room=room, members=members, username=username, list_of_messages=list_of_messages )

@app.route('/start',methods=["POST"])
def storedata():
    rooms=[]
    rooms= Room.query.add_columns('name').all()
    
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email is None:
        user=UserData.query.filter_by(name=username , password=password).first()
        if not user:
            return "this user name isn't exist"
    else:
        store_user_data(username,email,password)
        print("Done")
    return render_template('start.html',username=username, rooms=rooms)

@app.route('/chat',methods=["POST"])
def chat():
    roomName = request.form.get('username')
    roomId = request.form.get('room')

    return render_template('start.html',room=roomId,username=roomName)

@app.route('/create_room/<ownername>', methods=['post'])
def createroom(ownername):

    if request.method== 'POST':
        roomname= request.form.get('roomname')
        if len(roomname):
            create_room(ownername,roomname)
        else:
            return "Error! please enter Room Name"
        room= Room.query.filter_by(name=roomname).first()
        return render_template('chat.html',roomname=roomname, room = room, username=ownername)
    else:
        return "Method isn't post"

@app.route('/updateroom/<username>/<roomname>',methods=['POST', 'GET'])
def updateroom1(username, roomname):
    room = Room.query.filter_by(name=roomname).first()

    if room and is_owner(username):
        members= get_room_members(roomname)

        if request.method == 'POST':
            roomname = request.form.get('room_name')
            room.name= roomname
            db.session.commit()
            list_of_messages = get_messages(roomname)
            return render_template('chat.html', roomname=room, members=members,username=username,list_of_messages=list_of_messages)

        return render_template('update_room.html', room=room, members=members,username=username)
    
    else:
        return "Room Not found"

@socketio.on('join_room')
def handle_join_room_event(data):   
    app.logger.info("{} has joined the room {}".format(data['username'], data['roomname']))
    join_room(data['roomname'])
    socketio.emit('join_room_announcement',data)

@socketio.on('send_message')
def handle_send_message_event(data):
    message = Message( room_id=data['roomid'], text=data['message'], created_by=data['username'], created_at=datetime.now() )
    db.session.add(message)
    db.session.commit()

    d=datetime.now()
    def myconverter(o):
        if isinstance(o, datetime):
            return o.__str__()
    data['created_at']=json.dumps(d, default = myconverter)

    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],data['roomname'],data['message']))
    socketio.emit('receive_message', data, room=data['roomname'])

socketio.run(app,debug=True)