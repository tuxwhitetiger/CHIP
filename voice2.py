#!/usr/bin/python

from os import environ, path
import pyaudio
import subprocess
from pocketsphinx import *
import socket

MODELDIR = "/home/tux/CHIP/"

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'model/en-us/en-us'))
#build a list of word one per line and pump into the following site
#http://www.speech.cs.cmu.edu/tools/lmtool.html
config.set_string('-lm', path.join(MODELDIR, 'my.lm'))
config.set_string('-dict', path.join(MODELDIR, 'my.dict'))
config.set_string('-logfn','nul')
decoder = Decoder(config)


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream() 
decoder.start_utt()
in_speech_bf = False


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
network.connect((HOST, PORT))

lastface="Happy face"
faceToConfirm="Happy face"

def networksendsetface(message):
    data = "Set Face:"+message
    print(data)
    network.sendall(data.encode())
    print("awating responce")
    data = network.recv(1024)
    print("recived:", data.decode('utf-8'))
    return data.decode('utf-8')

def confirmspeak(message):
    global faceToConfirm
    global lastface
    lastface=faceToConfirm
    faceToConfirm=message
    confirm = 'confirm '
    messageToRead = confirm + message
    subprocess.Popen(['espeak', messageToRead])

def speak(message):
    
    subprocess.Popen(['espeak', message])




while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                guess = decoder.hyp()
                if guess != None:
                    if "CONFIRM" in guess.hypstr:
                        lastface = faceToConfirm
                        speak(networksendsetface(faceToConfirm))
                    elif "SET SAD FACE" in guess.hypstr:
                        confirmspeak("Sad face")
                    elif "SET HAPPY FACE" in guess.hypstr:
                        confirmspeak("Happy face")
                    elif "SET ANGRY FACE" in guess.hypstr: 
                        confirmspeak("Angry face")
                    elif "SET WHAT FACE" in guess.hypstr:
                        confirmspeak("What face")
                    elif "SET FLAG FACE" in guess.hypstr:
                        confirmspeak("Flag face")
                    elif "SET GIF FACE" in guess.hypstr:
                        confirmspeak("Gif face")
                    elif "SET OH FACE" in guess.hypstr:
                        confirmspeak("Oh face")
                    elif "SET SNAKE FACE" in guess.hypstr:
                        confirmspeak("Snake face")
                    elif "SET OVERHEAT FACE" in guess.hypstr:
                        confirmspeak("Overheat face")
                    elif "SET OVER HEAT FACE" in guess.hypstr:
                        confirmspeak("Overheat face")
                    elif "SET SEE WOOD FACE" in guess.hypstr:
                        confirmspeak("Cwood face")
                    elif "SET LOW BATTERY FACE" in guess.hypstr:
                        confirmspeak("Lowbatt face")
                    elif "SET PACk MAN FACE" in guess.hypstr:
                        confirmspeak("Pacman face")
                    elif "SET PACkMAN FACE" in guess.hypstr:
                        confirmspeak("Pacman face")
                    elif "SET MATRIX FACE" in guess.hypstr:
                        confirmspeak("Matrix face")
                    elif "SET BALL FACE" in guess.hypstr:
                        confirmspeak("8 Ball Face")
                    elif "SHAKE BALL" in guess.hypstr:
                        confirmspeak("SHAKE BALL")
                    elif "SET HALLOWEEN FACE" in guess.hypstr:
                        confirmspeak("HALLOWEEN FACE")
                    elif "CANCEL" in guess.hypstr: ## stop gap coz i don't have NO in my dict yet
                        speak("canceled")
                        faceToConfirm = lastface
                decoder.start_utt()
    else:
        break
decoder.end_utt()


