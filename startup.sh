#!/bin/bash
cd /home/tux/CHIP
sudo python /home/tux/CHIP/server.py &
sudo python /home/tux/CHIP/face.py &
python /home/tux/CHIP/voice2.py &

