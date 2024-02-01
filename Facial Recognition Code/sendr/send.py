import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("10.235.91.100", 1002))

with open(r"Proof.png", "rb") as file:
    image_data = file.read(2048)

    while image_data:
        client.send(image_data)
        image_data = file.read(2048)

client.close()