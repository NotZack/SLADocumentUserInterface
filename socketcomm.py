import socket

client_socket = socket.socket()


def open_socket(port_number):
    host = socket.gethostname()
    port = port_number
    client_socket.connect((host, port))


def send_query_to_socket(message):
    client_socket.sendall((message + '\n').encode())

    data = client_socket.recv(2048).decode()
    return data


def collect_room_data(room_string):
    return send_query_to_socket("Collect_Unique_Room_Data:" + room_string)