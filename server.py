import socket
from _thread import *
from PIL import Image
from PIL import GifImagePlugin
import numpy as np

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
alarm = "null"
Request = "null"
TSM = "null" #tellegram send message
face = "Happy face"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.settimeout(0.2)
s.listen()

socketList = []

socketList.append(s)

def loadGif(fileName):
    print("filename:"+fileName)
    image = Image.open(fileName)
    output =""
    for frame in range(0,image.n_frames):
        image.seek(frame)
        arr = np.array(image.convert('RGB'))
        for i in arr:
            for j in i:
                text = str(j)+','
                output+=text
            output+="R"
        output+="F"
    output+="DONE"
    print("DONE")
    return output



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
                        if("SHAKE BALL" in face):
                            face = "8 Ball Face"
                    elif "Set Face:" in info:
                        face = info.split(':',1)[1]
                        sock.sendall("done".encode())
                    elif "Get Alarm" in info:
                        sock.sendall(alarm.encode())
                        alarm = "null"
                    elif "Set Alarm" in info:
                        alarm = info.split(':',1)[1]
                        sock.sendall("done".encode())
                    elif "Pull Gif:" in info:
                        print("info:"+info)
                        giftoget = info.split(':',1)[1]
                        print("giftoget:"+giftoget)
                        gifdata = loadGif('./faces/'+giftoget)
                        sock.sendall(gifdata.encode())
                    elif "say:" in info:
                        AlarmMessage = info.split(':',1)[1]
                        subprocess.Popen(['espeak', AlarmMessage])
                        sock.sendall(AlarmMessage.encode())
                    elif "Get Request" in info:
                        sock.sendall(Request.encode())
                        Request = "null"
                    elif "Request:" in info:
                        Request = info.split(':',1)[1]
                        sock.sendall("done".encode())
                    elif "Get Telegram Send Message:" in info:
                        sock.sendall(TSM.encode())
                    elif "Set Telegram Send Message:" in info:
                        TSM = info.split(':',1)[1]
                        sock.sendall("done".encode())
                    else:
                        print("could not deal with:",info)
            except socket.timeout:
                pass

