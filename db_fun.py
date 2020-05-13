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


def get_room_members(room_name):
    '''
    this function returns all members_ID of each room
    '''
    members = db.session.query(UserData.name).join(RoomMember.billing_address_user).join(RoomMember.billing_address_room).filter_by(name=room_name).all()
    members = np.array(members).T[0]
    return members

def is_owner(username , roomname):
    '''
    check if user is 
    '''
    room = Room.query.filter_by(name = roomname).first()
    user = UserData.query.filter_by(name = username).first()
    owner = RoomMember.query.add_column('owner_flag').filter_by(user_id = user.id, room_id = room.id).first()
    return owner[1]


def add_room_member(roomname, username):
    '''
    add user in spesific room
    once user decided to join any room
    '''
    user_id = UserData.query.add_column('id').filter_by(name=username).first()[1]
    room_id = Room.query.add_column('id').filter_by(name=roomname).first()[1]
    member = RoomMember.query.filter_by(user_id=user_id, room_id=room_id).first()
    if not member:
        member = RoomMember(user_id=user_id, room_id=room_id, owner_flag=False, added_at=datetime.now())
        db.session.add(member)
        db.session.commit()

def get_messages(roomname):
    '''
    return history chats for any room
    '''
    messages = db.session.query(Message).join(Room).filter_by(name=roomname).all()
    list_of_messages=[]
    for message in messages:
        list_of_messages.append([message.created_by ,message.created_at , message.text])    
    return list_of_messages

def update_room(room_name):
    room= Room.query.filter_by(room_name=room_name).first()

def remove_room_member(member_name , room_name):
    room = Room.query.filter_by(name=room_name).first()
    member = UserData.query.filter_by(name=member_name).first()
    roommember = RoomMember.query.filter_by(user_id= member.id , room_id = room.id).first()
    db.session.delete(roommember)
    db.session.commit()
    return True





