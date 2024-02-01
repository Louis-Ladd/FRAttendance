import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 1002))
server.listen()

client_socket, client_address = server.accept()

with open("Proofreceives.png", "wb") as file:
    image_chunk = client_socket.recv(2048)

    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(2048)

client_socket.close()
server.close()