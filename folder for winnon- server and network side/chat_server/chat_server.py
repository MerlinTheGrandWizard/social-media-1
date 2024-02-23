import socket
import threading
import random
import sqlite3
import uuid


connect = sqlite3.connect('Server.db')

cursor = connect.cursor()
#will delete if asked
cursor.execute('''
      CREATE TABLE IF NOT EXISTS User_Table (
           UID TEXT PRIMARY KEY,
           UserName TEXT NOT NULL,
           Hashed_Password TEXT NOT NULL,
           FriendTable_ID TEXT
       )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS Forum_table (
            FormID TEXT PRIMARY KEY,
            CreatedBy TEXT NOT NULL,
            ForumTitle TEXT NOT NULL
        )
    ''')
connect.commit()
connect.close()

def add_toForums(createdBy,FormTitle):#creates a post
     connect = sqlite3.connect('Server.db')
     cursor = connect.cursor() 
     FormID = str(uuid.uuid4())
     cursor.execute('''
        INSERT INTO Forum_table (FormID, createdBy, FormTitle)
        VALUES (?, ?)
    ''', (FormID, createdBy, FormTitle))
    #create a new table
     cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {FormID} (
            FormMessageNum TEXT INTEGER KEY AUTOINCREMENT,
            UserThatSentMessage TEXT NOT NULL,
            Message TEXT NOT NULL
        )
    ''')
     connect.commit()
     connect.close()

def order_ids(id1, id2):
        return sorted([id1, id2])#used when adding friend req

def insert_user_record(user_name, hashed_password ):#method to add a record and creates a corresponding friend list/table

    connect = sqlite3.connect('Server.db')
    cursor = connect.cursor()
    UID = str(uuid.uuid4())
    # Insert a new record into the User_Table with the specified UID
    cursor.execute('''
        INSERT INTO User_Table (UID, UserName, Hashed_Password, FriendTable_ID)
        VALUES (?, ?, ?, ?)
    ''', (UID, user_name, hashed_password, UID))
    # the 'f' allows UID to be inputed
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {UID} (
            friendID TEXT PRIMARY KEY,
            IsFriend BOOLEAN,
            SentFriReq BOOLEAN,
            ReceiveFriReq BOOLEAN,
            DMID TEXT
        )
    ''')
    #DMID must also be unique
    connect.commit()
    connect.close()

def add_friend_request(user_uid, friend_id,sent_friend_request, receive_friend_request):#add to user_uid client, states if the user client sent or recieved a request
    connect = sqlite3.connect('Server.db')
    cursor = connect.cursor()
    DMID = str(uuid.uuid4())# kept same so both users are on same dm 
    is_friend = False
    #one who recieves
    cursor.execute(f'''
        INSERT INTO {friend_id} (friendID, IsFriend, SentFriReq, ReceiveFriReq, DMID)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_uid, is_friend, not sent_friend_request,not receive_friend_request, DMID))   
    #one who sends
    cursor.execute(f'''
        INSERT INTO {user_uid} (friendID, IsFriend, SentFriReq, ReceiveFriReq, DMID)
        VALUES (?, ?, ?, ?, ?)
    ''', (friend_id, is_friend, sent_friend_request, receive_friend_request, DMID))
    
    #reuse for send message function

    user1, user2 = order_ids(user_uid, friend_id) # the two are now in alphabetical order, user1 is first in order
    
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {DMID} (
            {user1} TEXT,
            {user2} TEXT,
            Message_num INTEGER PRIMARY KEY AUTOINCREMENT,
            DidUser1_send BOOLEAN,
            Message TEXT,
        )
    ''')
    
    connect.commit()
    connect.close()

def add_message_toDM(sender,receiver,message):#allow only the ID be passed in
    connect = sqlite3.connect('Server.db')
    cursor = connect.cursor()
    user1, user2 = order_ids(sender,receiver) 
    if sender == user1:
        didU1send = True
    else:
        didU1send = False 
    DMID_LOL = cursor.execute(f"SELECT DMID FROM {user1} WHERE friendID = ?",(1,)) # dont mind me, i cant be asked right now its midnight mate, no joke its like 00:01 on my computer, i should watch heavenly delusion tmrw
    resultDMID = cursor.fetchone()
    #should add a message to the table , there should only be one table for each pair of users
    cursor.execute(f'''
        INSERT INTO {resultDMID} ({user1}, {user2}, DidUser1_send, Message)
        VALUES (?, ?, ?, ?)
    ''', ({user1}, {user2}, didU1send, message))
    connect.commit()
    connect.close()

def text_inForum(forumID, userID, message):
    connect = sqlite3.connect('Server.db')
    cursor = connect.cursor()
    cursor.execute(f'''
        INSERT INTO {forumID} ( UserThatSentMessage, Message)
        VALUES ( ?, ?)
    ''', (userID, message))
    
    connect.commit()
    connect.close()

def handle_client(client_socket, address):
    # Receive and print the message from the client
    message = client_socket.recv(1024).decode('utf-8')
    print(f"Received message from client: {message}")
    client_socket.close()
    return message

def start_server():
    server_ip = "127.0.0.1"  # the ip (use 127.0.0.1 to test in a closed system)
    server_port = 12345  # Choose an available port
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((server_ip, server_port))

    server_socket.listen()

    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()