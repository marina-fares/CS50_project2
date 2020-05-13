import os
import requests
import numpy as np
import json

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
from models import *

from db_fun import *

#init application
app = Flask(__name__)
socketio=SocketIO(app)
app.secret_key='this is my own secret'

#init database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///chatdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

rooms=[]

@app.route("/")
def signin():
    '''
    this function for NavBar
    return : signin page
    '''
    return render_template('signin.html')


@app.route("/signup")
def signup():
    '''
    this function for NavBar
    return : signup page
    '''
    return render_template('signup.html')


@app.route("/start<username>")
def start(username):
    '''
    '''
    rooms=[]
    rooms= Room.query.add_columns('name').all()
    return render_template("start.html", username = username, rooms = rooms)

@app.route("/welcome",methods=['POST'])
def welcome():
    '''
    this function return user page  
    input : user data "username and password"
    '''
    rooms=[]
    rooms= Room.query.add_columns('name').all()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = UserData.query.filter_by(name=username , password=password).first()
        if not user:
            flash("Error! username or password not correct please try again")        
            return render_template('signin.html')

    return render_template("start.html", username = username, rooms = rooms)

@app.route("/storedata", methods=['POST'])
def storedate():
    '''
    this finction when user signup
    input : user data
    return : user page
    '''
    rooms=[]
    rooms= Room.query.add_columns('name').all()
    
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    try:
        user = UserData(name=username, email=email, password=password )
        db.session.add(user)
        db.session.commit()
        
        return render_template('start.html', username=username, rooms = rooms )
    except:
        flash('Error! this user name is used plaese use another one')
        return render_template("signin.html")



@app.route("/viewroom/<username>/<roomname>")
def ViewRoom(username,roomname):
    '''
    when user choose spesific room from drop down menue
    input : username & roomname
    return : room page with history of old chats and Room's partners
    '''
    members=get_room_members(roomname)
    room= Room.query.filter_by(name=roomname).first()

    if username not in members:
        add_room_member(roomname, username)
    list_of_messages = get_messages(roomname)
    
    return render_template("chat.html",room=room, members=members, username=username, list_of_messages=list_of_messages )


@app.route('/create_room/<ownername>', methods=['post'])
def createroom(ownername):
    '''
    this function create new room &
    make user as room owner who
    is have access to update this room
    '''
    rooms= Room.query.add_columns('name').all()

    if request.method== 'POST':
        roomname= request.form.get('roomname')
        if len(roomname):
            try:
                create_room(ownername,roomname)
            except:
                flash("Error! this Room name is used please choose uniqe one")
                return render_template('start.html',username = ownername, rooms = rooms)
    
        else:
            flash("Error! please enter Room Name")
            return render_template('start.html',username = ownername, rooms = rooms)
            
        room= Room.query.filter_by(name=roomname).first()
        return render_template('chat.html',roomname=roomname, room = room, username=ownername)
    else:
        return "Method isn't post"


@app.route('/updateroom/<username>/<roomname>',methods=['POST', 'GET'])
def updateroom(username, roomname):
    '''
    this function give an access to the owner 
    to update the Room data
    '''
    room = Room.query.filter_by(name=roomname).first()

    if room and is_owner(username, roomname):
        members= get_room_members(roomname)

        if request.method == 'POST':
            
            new_room_name = request.form.get('new_room_name')
            Remove_member = request.form.get('Remove_member')
            Add_member = request.form.get('Add_member')
            
            if new_room_name:
                try: #to check unique Room name
                    newroomname = new_room_name
                    room.name= newroomname
                    db.session.commit()
                    return redirect(url_for('ViewRoom',username=username,roomname=newroomname))
                except:
                    flash("this Room name is used please choose a uniqe one")
                    return redirect(url_for('ViewRoom',username=username,roomname=roomname))

            elif Remove_member:
                 #to check unique Room name
                try:
                    remove_room_member(Remove_member , roomname)
                    return redirect(url_for('ViewRoom',username=username,roomname=roomname))
                except:
                    flash("this user isn't Exist")
                    return redirect(url_for('ViewRoom',username=username,roomname=roomname))

            elif Add_member:
                try:#check if user name is right    
                    add_room_member(roomname, Add_member)
                    return redirect(url_for('ViewRoom',username=username,roomname=roomname))
                except:
                    flash("this user is't exist")
                    return redirect(url_for('ViewRoom',username=username,roomname=roomname))


        return render_template('update_room.html', room=room, members=members,username=username)
    
    else:
        flash("this function available for Admin only")
        return redirect(url_for('ViewRoom',username=username,roomname=roomname))

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