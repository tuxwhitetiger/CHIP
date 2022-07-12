#!/usr/bin/python
from email.mime import base
import socket
from turtle import clear
from PIL import Image
from PIL import GifImagePlugin
from colour import Color as Col
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
from snake import *

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
network.connect((HOST, PORT))

def networksendGetface():
    network.sendall("Get Face".encode())
    data = network.recv(1024)
    #print(data.decode('utf-8'))
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
    blinkBase = 5
    blinkAdition = (random.randint(0, 5000)/1000)
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
        if ((seconds+blinkBase+blinkAdition) - time.time()) <= 0:

            if doubleBlink:
                #fastdoubleblinks
                playFastAnimatedGif("./faces/happy.gif")
                playFastAnimatedGif("./faces/happy.gif")
            else:
                #blink
                playAnimatedGif("./faces/happy.gif")
            seconds = time.time()
            doubleBlink = bool(random.getrandbits(1))
            blinkAdition = (random.randint(0, 5000)/1000)

        
    

def showSnakeFace():
    mysnake = snake()
    mysnake.setup()
    foodcolor =  graphics.Color(0, 255, 0) #random color
    headcolor =  graphics.Color(255, 0, 0) #random color
    bodycolor =  graphics.Color(255, 255, 255) #random color
    offscreen_canvas = matrix.CreateFrameCanvas()
    while True:
        checkface = networksendGetface()
        if checkface not in face:
            face = checkface
            break

        mysnake.update()
        offscreen_canvas.clear()
        #drawfood
        graphics.DrawLine(offscreen_canvas, mysnake.food.x, mysnake.food.y, mysnake.food.x, mysnake.food.y, foodcolor)
        #drawhead
        graphics.DrawLine(offscreen_canvas, mysnake.head.x, mysnake.head.y, mysnake.head.x, mysnake.head.y, headcolor)
        #draw body
        for seg in mysnake.segments:
            graphics.DrawLine(offscreen_canvas, seg.x, seg.y, seg.x, seg.y, bodycolor)
        
        matrix.SwapOnVSync(offscreen_canvas)





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
    global face
    #need to run each time ? placed
    # need to remove time constraint and increase no of ? per frame as time goes on
    while i<count:
        textColor =  graphics.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) #random color
        font = random.choice(mfonts)
        x = random.randint(0, 128)
        y = random.randint(0, 32)
        graphics.DrawText(offscreen_canvas, font, x, y, textColor, "?")
        matrix.SwapOnVSync(offscreen_canvas)
        sleepTimer = sleepTimer-(sleepTimer/(count-i))
        i = i + 1 
        checkface = networksendGetface()
        if checkface not in face:
            face = checkface
            break
        time.sleep(sleepTimer)
        time.sleep(0.001)
    time.sleep(0.5)

def showUwUFace():
    #set up vars
    offscreen_canvas = matrix.CreateFrameCanvas()
    offscreen_canvas.Clear()
    font = graphics.Font()
    font.LoadFont("./fonts/9x15.bdf")
    global face
    continuum = 0
    x = 0
    y = 0
    owo_down = True
    owo_right = True
    i = 0
    c=Col
    while True:
        #check for new face
        if i % 40 == 0:
            checkface = networksendGetface()
            if checkface not in face:
                face = checkface
                break
        i = i+1
        offscreen_canvas.Clear()
        #pick colour
        continuum += 0.005
        if continuum >= 1:
            continuum = 0
        c = Col(hsl=(continuum, 1, 0.5))
        red,green,blue = c.rgb
        textColor =  graphics.Color(red*255,green*255,blue*255)
        #pick location
        #check bounding boxs
        if(y>=32):
            owo_down = False
        if(y<=11):
            owo_down = True
        if(x>=38):
            owo_right = False
        if(x<=0):
            owo_right = True
        #move in correct direction
        if(owo_down):
            y = y+1
        else:
            y = y-1
        if(owo_right):
            x = x+1
        else:
            x = x-1
        
        #draw
        graphics.DrawText(offscreen_canvas, font, x, y, textColor, "OwO")
        matrix.SwapOnVSync(offscreen_canvas)
        time.sleep(0.04)



while True:
    face = networksendGetface()
    
    if "Sad face" in face:
        showUwUFace()
    elif "Happy face" in face:
        showHappyFace()
    elif "Flag face" in face:
        showFlagFace()
    elif "Angry face" in face:
        showSnakeFace()
    elif "Gif face" in face:
        showGifFace()
    elif "Oh face" in face:
        showOhFace
    elif "What face" in face:
        showWhatFace()

   




