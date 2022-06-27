#!/usr/bin/python
import socket
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions



HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
network.connect((HOST, PORT))

def networksendGetface():
    network.sendall('Get Face')
    data = network.recv(1024)
    return data.decode('utf-8')




# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.gpio_slowdown = 3
options.hardware_mapping = 'regular'

matrix = RGBMatrix(options = options)

image = Image.open("./faces/test.gif")

while True:
    face = networksendGetface()

    if "SAD FACE" in face:
        image = Image.open("./faces/sad.gif")
    elif "HAPPY FACE" in face:
        image = Image.open("./faces/happy.gif")
    elif "FLAG FACE" in face:
        image = Image.open("./faces/flag.gif")
    elif "ANGRY FACE" in face:
        image = Image.open("./faces/angry.gif")
    elif "GIF FACE" in face:
        image = Image.open("./faces/pacman.gif")
    elif "OH FACE" in face:
        image = Image.open("./faces/oh.gif")
    elif "WHAT FACE" in face:
        image = Image.open("./faces/what.gif")

    matrix.SetImage(image.convert('RGB'))





