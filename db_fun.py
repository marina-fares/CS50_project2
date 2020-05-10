import csv
import os
from flask import Flask, render_template, request
from models import *
from datetime import datetime
import numpy as np

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///chatdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def create_room(owner,roomname):
    '''
    this functon makes new room
    and add details in RoomMember table
    '''
    roomunit = Room(name=roomname, created_at=datetime.now(), created_by=owner)
    db.session.add(roomunit)
    db.session.commit()
    user_id= UserData.query.add_columns('id').filter_by(name=owner).first()
    room_id= Room.query.add_columns('id').filter_by(name=roomname).first()
    member = RoomMember(user_id=user_id[1], room_id=room_id[1], owner_flag=True, added_at=datetime.now())
    db.session.add(member)
    db.session.commit()

def add_room_member(user_id,room_id):
    '''
    this function when user join any room
    input: user_id and room_id
    '''
    member = RoomMember(user_id=user_id, room_id=room_id[1], owner_flag=False, added_at=datetime.now())
    db.session.add(member)
    db.session.commit()

def get_room_members(room_name):
    '''
    this function returns all members_ID of each room
    '''
    members = db.session.query(UserData.name).join(RoomMember.billing_address_user).join(RoomMember.billing_address_room).filter_by(name=room_name).all()
    members = np.array(members).T[0]
    return members

def is_owner(room_name):
    owner = RoomMember.query.add_column('owner_flag').all()
    return owner

def update_room(room_name):
    room= Room.query.filter_by(room_name=room_name).first()

def remove_room_member():
    pass

def store_user_data(username,email,password):
    a=np.array(UserData.query.add_columns('name').all()).T
    user=UserData(name=username, email=email, password=password )
    if len(a):
        if username in a:
            return "Error, this username or password already exist"
    db.session.add(user)
    db.session.commit()

def add_room_member(roomname, username):
    user_id= UserData.query.add_column('id').filter_by(name=username).first()[1]
    room_id= Room.query.add_column('id').filter_by(name=roomname).first()[1]
    member = RoomMember(user_id=user_id, room_id=room_id, owner_flag=False, added_at=datetime.now())
    db.session.add(member)
    db.session.commit()

def get_messages(roomname):
    messages = db.session.query(Message).join(Room).filter_by(name=roomname).all()
    list_of_messages=[]
    for message in messages:
        list_of_messages.append([message.created_by ,message.created_at , message.text])    
    return list_of_messages

