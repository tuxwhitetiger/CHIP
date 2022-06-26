#!/usr/bin/python

from os import environ, path
import pyaudio

from pocketsphinx import *
import socket

MODELDIR = "/home/tux/CHIP/model"

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
#build a list of word one per line and pump into the following site
#http://www.speech.cs.cmu.edu/tools/lmtool.html
config.set_string('-lm', path.join(MODELDIR, '/home/tux/CHIP/my.lm'))
config.set_string('-dict', path.join(MODELDIR, '/home/tux/CHIP/my.dict'))
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

def networksendsetface(message):
    data = "Set Face:"+message
    print("setting face")
    network.sendall(data.encode())
    print("awating responce")
    data = network.recv(1024)
    print("recived:", data.decode('utf-8'))


while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()

                if "SET SAD FACE" in decoder.hyp().hypstr:
                    print ('set sad face')
                    networksendsetface('Sad face')
                elif "SET HAPPY FACE" in decoder.hyp().hypstr:
                    print ('set happy face')
                    networksendsetface('Happy face')
                elif "SET ANGRY FACE" in decoder.hyp().hypstr: 
                    print ('set angry face')
                    networksendsetface('Angry face')
                elif "SET WHAT FACE" in decoder.hyp().hypstr:
                    print ('set what face')
                    networksendsetface('What face')
                elif "SET FLAG FACE" in decoder.hyp().hypstr:
                    print ('set flag face')
                    networksendsetface('Flag face')
                elif "SET GIF FACE" in decoder.hyp().hypstr:
                    print ('set gif face')
                    networksendsetface('Gif face')
                elif "SET OH FACE" in decoder.hyp().hypstr:
                    print ('set oh face')
                    networksendsetface('Oh face')
                decoder.start_utt()
    else:
        break
decoder.end_utt()


