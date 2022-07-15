import socket
from _thread import *
from PIL import Image
from PIL import GifImagePlugin
import numpy as np

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

face = "Happy face"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.settimeout(0.2)
s.listen()

socketList = []

socketList.append(s)

def loadGif(fileName):
    image = Image.open(fileName)
    output =''
    for frame in range(0,image.n_frames):
        image.seek(frame)
        arr = np.array(image.convert('RGB'))
        print("\nThe Numpy 2D-Array is:")
        for i in arr:
            for j in i:
                output.join(j+',')
    print(output)
    return output

loadGif('faces/test.gif')

while True:
    ##roll though list of avalible sockets
    for sock in socketList:
        ##if looking at server see if we can pickup another client
        if sock == s:
            try:
                Client,addr = s.accept()
                Client.settimeout(0.2)
                socketList.append(Client)
            except socket.timeout:
                pass
        ##if not looking at server socket deal with any client request to get set face    
        else:
            try:
                data = sock.recv(2048)
                info = data.decode('utf-8')
                if info:
                    if "Get Face" in info:
                        sock.sendall(face.encode())
                    elif "Set Face:" in info:
                        face = info.split(':',1)[1]
                        sock.sendall("done".encode())
                    elif "Pull Gif:" in info:
                        giftoget = info.split(':',1)[1]
                        gifdata = loadGif('faces/'+giftoget)
                        sock.sendall(gifdata.encode())
                    else:
                        print("could not deal with:",info)
            except socket.timeout:
                pass

