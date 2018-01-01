#!/bin/bash
host=192.168.86.192
scp ~/amsen/git/amsen/python/*.py pi@$host:/home/pi/Strnad/amsen/python
scp ~/amsen/git/amsen/python/*.sh pi@$host:/home/pi/Strnad/amsen/python
echo executing run.sh on raspberry pi
ssh -tt pi@$host sudo /home/pi/Strnad/amsen/python/run.sh