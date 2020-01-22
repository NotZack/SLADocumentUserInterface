import socket

client_socket = socket.socket()


# Opens a client socket on the given port
def open_socket(port_number):
    host = socket.gethostname()
    port = port_number
    client_socket.connect((host, port))


# Sends text to the open socket
def send_query_to_socket(message):
    client_socket.sendall((message + '\n').encode())

    data = client_socket.recv(4096).decode()
    return data


# Sends an exact room query to the open socket
def collect_room_data(room_string):
    return send_query_to_socket("Collect_Unique_Room_Data:" + room_string)
