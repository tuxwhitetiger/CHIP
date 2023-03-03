#!/bin/bash
sleep 30
if ping -c 1 1.1.1.1 &> /dev/null
then
  git -C /home/tux/CHIP pull https://github.com/tuxwhitetiger/CHIP.git
  git -C /home/tux/CHIP3 pull https://github.com/tuxwhitetiger/CHIP3.0.git
else
  echo "no internet"
fi
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
sudo systemctl start isc-dhcp-server.service
cd /home/tux/CHIP3/CHIP/Debug/netcoreapp3.1
sudo dotnet CHIP.dll

#test