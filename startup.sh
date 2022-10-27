#!/bin/bash
sleep 30
git -C /home/tux/CHIP3 pull https://github.com/tuxwhitetiger/CHIP3.0.git
cd /home/tux/CHIP3/CHIP 
sudo mcs -out:bob.exe *.cs /r:RGBLedMatrix.dll
cd /home/tux/CHIP
sudo python /home/tux/CHIP/server.py &
sudo python /home/tux/CHIP/face.py &
python /home/tux/CHIP/voice2.py &

#this  is a test