import socket
import datetime
import uuid
import os
from threading import Thread

face_directory = r"C:\Users\Owner\Desktop\FRAttendance\FRAttedence\Faces"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 1002))
server.listen()


while True:
    client_socket, client_address = server.accept()

    print(f"Recieved image from {client_address[0]}")
    
    with open(os.path.join(face_directory, (str(uuid.uuid1()) + ".png")), "wb") as file:
        image_chunk = client_socket.recv(2048)
        while image_chunk:
            file.write(image_chunk)
            image_chunk = client_socket.recv(2048)

    client_socket.close()