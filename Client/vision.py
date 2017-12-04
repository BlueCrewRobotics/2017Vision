import sys
import time
from networktables import NetworkTables
import logging

logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize(server = "localhost")
sd = NetworkTables.getTable("/vision")

while True:
    try:
        x = sd.getNumberArray('centerX')
        width = sd.getNumberArray('width')
        
        try:
            firstEdge = x[1] - (width[1]/2)
            secondEdge = x[0] + (width[0]/2)
            edgeDiff = secondEdge - firstEdge
            location = firstEdge + (edgeDiff/2)
            locationError = location - 200
        except IndexError:
            locationError = 0

        if (locationError == 0):
            neededDirection = "Straight"
        elif (locationError > 5):
            neededDirection = "Right"
        elif (locationError < -5):
            neededDirection = "Left"
        elif (-5 <= locationError <= 5):
            neededDirection = "Stop"
        else:
            neededDirection = "Unknown"

        print(neededDirection)
    except KeyError:
        print('Waiting for Connection...')
    time.sleep(1)
