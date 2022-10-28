#!/bin/bash
sleep 30
git -C /home/tux/CHIP pull https://github.com/tuxwhitetiger/CHIP.git
git -C /home/tux/CHIP3 pull https://github.com/tuxwhitetiger/CHIP3.0.git
cd /home/tux/CHIP3/CHIP 
sudo mcs -out:bob.exe *.cs /r:RGBLedMatrix.dll
cd /home/tux/CHIP
sleep 15
sudo python server.py &
sleep 15
cd /home/tux/CHIP
su tux -c "python3 voice2.py &"
sleep 15
cd /home/tux/CHIP3/CHIP
sudo mono bob.exe &
sudo systemctl start isc-dhcp-server.service
