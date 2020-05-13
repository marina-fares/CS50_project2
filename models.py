from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class UserData(db.Model):
    __tablename__ = "userdata"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)# add uniqe query
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class Room(db.Model):
    __tablename__ = "room"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, nullable=False)

class RoomMember(db.Model):
    __tablename__ = "roommember"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("userdata.id"))
    room_id = db.Column(db.Integer, ForeignKey("room.id"))
    owner_flag = db.Column(db.Boolean, nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)

    billing_address_user = relationship("UserData", foreign_keys=[user_id])
    billing_address_room = relationship("Room", foreign_keys=[room_id])

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, ForeignKey("room.id"))
    text = db.Column(db.String, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    billing_address_room = relationship("Room", foreign_keys=[room_id])