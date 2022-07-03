#!/usr/bin/python
from email.mime import base
import socket
from PIL import Image
from PIL import GifImagePlugin
import random
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time



HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
network.connect((HOST, PORT))

def networksendGetface():
    network.sendall("Get Face".encode())
    data = network.recv(1024)
    print(data.decode('utf-8'))
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
face = networksendGetface()
image = Image.open("./faces/test.gif")

def playAnimatedGif(fileName):
    image = Image.open(fileName)
    global face
    for frame in range(0,image.n_frames):
        if frame % 10 == 0:
            checkface = networksendGetface()
            if checkface not in face:
                face = checkface
                break
        time.sleep(0.04)
        image.seek(frame)
        matrix.SetImage(image.convert('RGB'))

def playFastAnimatedGif(fileName):
    image = Image.open(fileName)
    global face
    for frame in range(0,image.n_frames):
        if frame % 40 == 0:
            checkface = networksendGetface()
            if checkface not in face:
                face = checkface
                break
        time.sleep(0.01)
        image.seek(frame)
        matrix.SetImage(image.convert('RGB'))

def showStaticGif(fileName):
    image = Image.open(fileName)
    if image.n_frames > 1:
        image.seek(0)
    matrix.SetImage(image.convert('RGB'))

def showSadFace():
    image = Image.open("./faces/sad.gif")
    matrix.SetImage(image.convert('RGB'))

def showHappyFace():
    ## random bounce between with in max and chance of double blink face /// animate it?
    #hold on first frame then randomly deside to play it and sometimes play it twice at double speed
    happyFaceNetworkTickCount = 0
    seconds = time.time()
    blinkBase = 5000
    blinkAdition = random.randint(0, 5000)
    doubleBlink = bool(random.getrandbits(1))
    global face
    while True:
        happyFaceNetworkTickCount = happyFaceNetworkTickCount+1
        if happyFaceNetworkTickCount % 10 == 0:
            checkface = networksendGetface()
            happyFaceNetworkTickCount = 0
            if checkface not in face:
                face = checkface
                break

        #static
        showStaticGif("./faces/happy.gif")
        if (time.time() - (seconds+blinkBase+blinkAdition)) <= 0:

            if doubleBlink:
                #fastdoubleblinks
                playFastAnimatedGif("./faces/happy.gif")
                playFastAnimatedGif("./faces/happy.gif")
            else:
                #blink
                playAnimatedGif("./faces/happy.gif")
            seconds = time.time()
            doubleBlink = bool(random.getrandbits(1))
            blinkAdition = random.randint(0, 5000)




   

def showFlagFace():
    showStaticGif("./faces/flag.gif")

def showAngryFace():
    ## growl + nose flareing
    image = Image.open("./faces/angry.gif")
    matrix.SetImage(image.convert('RGB'))

def showGifFace():
    playAnimatedGif("./faces/pacman.gif")

def showOhFace():
    image = Image.open("./faces/oh.gif")
    matrix.SetImage(image.convert('RGB'))

def showWhatFace():
    ## do the ? spam in here 
    #set up vars
    offscreen_canvas = matrix.CreateFrameCanvas()
    offscreen_canvas.Clear()
    font1 = graphics.Font()
    font1.LoadFont("./fonts/5x8.bdf")   
    font2 = graphics.Font()
    font2.LoadFont("./fonts/6x10.bdf")
    font3 = graphics.Font()
    font3.LoadFont("./fonts/7x13.bdf")
    font4 = graphics.Font()
    font4.LoadFont("./fonts/9x15.bdf")
    mfonts = [font1,font2,font3,font4]
    i = 0
    count = 100
    sleepTimer = 0.6
    #need to run each time ? placed
    while i<count:
        textColor =  graphics.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) #random color
        font = random.choice(mfonts)
        x = random.randint(0, 128)
        y = random.randint(0, 32)
        graphics.DrawText(offscreen_canvas, font, x, y, textColor, "?")
        matrix.SwapOnVSync(offscreen_canvas)
        sleepTimer = sleepTimer-(sleepTimer/(count-i))
        i = i + 1 
        time.sleep(sleepTimer)
        time.sleep(0.001)
    time.sleep(0.5)



while True:
    face = networksendGetface()
    
    if "Sad face" in face:
        showSadFace()
    elif "Happy face" in face:
        showHappyFace()
    elif "Flag face" in face:
        showFlagFace()
    elif "Angry face" in face:
        showAngryFace()
    elif "Gif face" in face:
        showGifFace()
    elif "Oh face" in face:
        showOhFace
    elif "What face" in face:
        showWhatFace()

   




