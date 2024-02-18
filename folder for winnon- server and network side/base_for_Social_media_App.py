
from email import message
import socket
import threading
import sys
'''
# gets ip address of a website
ip = socket.gethostbyname("www.google.com")
print(ip)
'''

alias = input('Create an alias: ')
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',55000))

def client_recieve():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'alias?':
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print("error!")
            client.close()
            break
       
def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))
     
recieve_thread = threading.Thread(target=client_recieve)
recieve_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()