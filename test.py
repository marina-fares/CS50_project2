from db_fun import * 

def main():
    room = get_messages('Room1')
    print(room)
    # Add user data
    '''
    user=UserData(name='marina1', email='marina1@gmail.com', password='1' )
    db.session.add(user)
    db.session.commit()

    user=UserData(name='marina2', email='marina2@gmail.com', password='2' )
    db.session.add(user)
    db.session.commit()
    
    user=UserData(name='marina3', email='marina3@gmail.com', password='3' )
    db.session.add(user)
    db.session.commit()
    '''
    # Add Room
    '''
    room=Room(name='room1', created_at=datetime.now(), created_by='marina1' )
    db.session.add(room)
    db.session.commit()
    
    room=Room(name='room2', created_at=datetime.now(), created_by='marina2' )
    db.session.add(room)
    db.session.commit()

    room=Room(name='room3', created_at=datetime.now(), created_by='marina3' )
    db.session.add(room)
    db.session.commit()
    '''
    # Add Room Member
    '''
    member = RoomMember(user_id=5, room_id=4, owner_flag=False, added_at=datetime.now())
    db.session.add(member)
    db.session.commit()
    '''
    # check join query
    
    #print(is_owner('room1'))

    #members= np.array(RoomMember.query.add_column('roommember.user_id').filter(RoomMember.room_id=='2').all()).T[1]
    #print(members)
    #m= RoomMember.query.join (UserData.id).filter(RoomMember.room_id=='2').all()[1]
   
    
    
if __name__ == "__main__":
    with app.app_context():
        main()

