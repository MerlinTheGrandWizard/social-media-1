import socket
import json

def send_request(sock, request_type, data):#can send data aproiatly
    request = {
        "type": request_type,
        "data": data
    }
    json_request = json.dumps(request)
    sock.send(json_request.encode())

def receive_response(sock):
    response = sock.recv(1024).decode('utf-8')
    return response

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("127.0.0.1", 12345)

    client_socket.connect(server_address)

    #Authentication Request
    send_request(client_socket, "authen_creds", {"username": "your_username", "password": "your_password"})
    authentication_response = receive_response(client_socket)
    print(authentication_response)

    #Register User Request
    send_request(client_socket, "register_user", {"username": "new_user", "password": "new_password"})
    registration_response = receive_response(client_socket)
    print(registration_response)

    #Get Friend List Request (assuming you implement this in the server)
    send_request(client_socket, "get_friendList", {})
    friend_list_response = receive_response(client_socket)
    print(friend_list_response)

    client_socket.close()

if __name__ == "__main__":
    main()



