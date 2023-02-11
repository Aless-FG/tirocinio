import os
import re
from statistics import mean

from matplotlib import pyplot as plt
import numpy as np
from pandas import read_csv
import math

listPitch = []
listYaw = []
listRoll = []
height = []
listTestGraph = []
pitchTestArray = []
yawTestArray = []
rollTestArray = []

pitchRangeAndError = []
yawRangeAndError = []
rollRangeAndError = []
range = -80
col_names = ["testGraph", "pitch", "yaw", "roll", "avg"]
data = read_csv("/home/ale/Desktop/histograms/graphK3/graphsk3YPRManhattan.csv", usecols=col_names)


x_ticks = [-80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80]
for item in x_ticks:
        pitchRangeAndError.append([range, range + 10])
        yawRangeAndError.append([range, range + 10])
        rollRangeAndError.append([range, range + 10])
        range = range + 10
del pitchRangeAndError[16]
del yawRangeAndError[16]
del rollRangeAndError[16]
for item in data.values:

    if isinstance(item[0], str):
        listTestGraph.append(item[0])
        chunksTest = re.split('(?<=\D)(?=\d)|(?<=\d)(?=\D)', item[0])
        pitchTest = float(chunksTest[0] + chunksTest[1] + chunksTest[2] + chunksTest[3])
        if pitchTest >= -80 and pitchTest < -70:
            pitchRangeAndError.__getitem__(0).append(item[1])
        if pitchTest >= -70 and pitchTest < -60:
            pitchRangeAndError.__getitem__(1).append(item[1])
        if pitchTest >= -60 and pitchTest < -50:
            pitchRangeAndError.__getitem__(2).append(item[1])
        if pitchTest >= -50 and pitchTest < -40:
            pitchRangeAndError.__getitem__(3).append(item[1])
        if pitchTest >= -40 and pitchTest < -30:
            pitchRangeAndError.__getitem__(4).append(item[1])
        if pitchTest >= -30 and pitchTest < -20:
            pitchRangeAndError.__getitem__(5).append(item[1])
        if pitchTest >= -20 and pitchTest < -10:
            pitchRangeAndError.__getitem__(6).append(item[1])
        if pitchTest >= -10 and pitchTest < 0:
            pitchRangeAndError.__getitem__(7).append(item[1])
        if pitchTest >= 0 and pitchTest < 10:
            pitchRangeAndError.__getitem__(8).append(item[1])
        if pitchTest >= 10 and pitchTest < 20:
            pitchRangeAndError.__getitem__(9).append(item[1])
        if pitchTest >= 20 and pitchTest < 30:
            pitchRangeAndError.__getitem__(10).append(item[1])
        if pitchTest >= 30 and pitchTest < 40:
            pitchRangeAndError.__getitem__(11).append(item[1])
        if pitchTest >= 40 and pitchTest < 50:
            pitchRangeAndError.__getitem__(12).append(item[1])
        if pitchTest >= 50 and pitchTest < 60:
            pitchRangeAndError.__getitem__(13).append(item[1])
        if pitchTest >= 60 and pitchTest < 70:
            pitchRangeAndError.__getitem__(14).append(item[1])
        if pitchTest >= 70 and pitchTest < 80:
            pitchRangeAndError.__getitem__(15).append(item[1])
        yawTest = float(chunksTest[4] + chunksTest[5] + chunksTest[6] + chunksTest[7])
        if yawTest >= -80 and yawTest < -70:
            yawRangeAndError.__getitem__(0).append(item[2])
        if yawTest >= -70 and yawTest < -60:
            yawRangeAndError.__getitem__(1).append(item[2])
        if yawTest >= -60 and yawTest < -50:
            yawRangeAndError.__getitem__(2).append(item[2])
        if yawTest >= -50 and yawTest < -40:
            yawRangeAndError.__getitem__(3).append(item[2])
        if yawTest >= -40 and yawTest < -30:
            yawRangeAndError.__getitem__(4).append(item[2])
        if yawTest >= -30 and yawTest < -20:
            yawRangeAndError.__getitem__(5).append(item[2])
        if yawTest >= -20 and yawTest < -10:
            yawRangeAndError.__getitem__(6).append(item[2])
        if yawTest >= -10 and yawTest < 0:
            yawRangeAndError.__getitem__(7).append(item[2])
        if yawTest >= 0 and yawTest < 10:
            yawRangeAndError.__getitem__(8).append(item[2])
        if yawTest >= 10 and yawTest < 20:
            yawRangeAndError.__getitem__(9).append(item[2])
        if yawTest >= 20 and yawTest < 30:
            yawRangeAndError.__getitem__(10).append(item[2])
        if yawTest >= 30 and yawTest < 40:
            yawRangeAndError.__getitem__(11).append(item[2])
        if yawTest >= 40 and yawTest < 50:
            yawRangeAndError.__getitem__(12).append(item[2])
        if yawTest >= 50 and yawTest < 60:
            yawRangeAndError.__getitem__(13).append(item[2])
        if yawTest >= 60 and yawTest < 70:
            yawRangeAndError.__getitem__(14).append(item[2])
        if yawTest >= 70 and yawTest < 80:
            yawRangeAndError.__getitem__(15).append(item[2])
        rollTest = float(chunksTest[8] + chunksTest[9] + chunksTest[10] + chunksTest[11])
        if rollTest >= -80 and rollTest < -70:
            rollRangeAndError.__getitem__(0).append(item[3])
        if rollTest >= -70 and rollTest < -60:
            rollRangeAndError.__getitem__(1).append(item[3])
        if rollTest >= -60 and rollTest < -50:
            rollRangeAndError.__getitem__(2).append(item[3])
        if rollTest >= -50 and rollTest < -40:
            rollRangeAndError.__getitem__(3).append(item[3])
        if rollTest >= -40 and rollTest < -30:
            rollRangeAndError.__getitem__(4).append(item[3])
        if rollTest >= -30 and rollTest < -20:
            rollRangeAndError.__getitem__(5).append(item[3])
        if rollTest >= -20 and rollTest < -10:
            rollRangeAndError.__getitem__(6).append(item[3])
        if rollTest >= -10 and rollTest < 0:
            rollRangeAndError.__getitem__(7).append(item[3])
        if rollTest >= 0 and rollTest < 10:
            rollRangeAndError.__getitem__(8).append(item[3])
        if rollTest >= 10 and rollTest < 20:
            rollRangeAndError.__getitem__(9).append(item[3])
        if rollTest >= 20 and rollTest < 30:
            rollRangeAndError.__getitem__(10).append(item[3])
        if rollTest >= 30 and rollTest < 40:
            rollRangeAndError.__getitem__(11).append(item[3])
        if rollTest >= 40 and rollTest < 50:
            rollRangeAndError.__getitem__(12).append(item[3])
        if rollTest >= 50 and rollTest < 60:
            rollRangeAndError.__getitem__(13).append(item[3])
        if rollTest >= 60 and rollTest < 70:
            rollRangeAndError.__getitem__(14).append(item[3])
        if rollTest >= 70 and rollTest < 80:
            rollRangeAndError.__getitem__(15).append(item[3])
        """pitchTestArray.append(pitchTest)
        yawTestArray.append(yawTest)
        rollTestArray.append(rollTest)"""
for item in pitchRangeAndError:
    if len(item) > 2:
        sommaP = mean(item[2::])
        item.append(sommaP)
        pitchTestArray.append(sommaP)
for item in yawRangeAndError:
    if len(item) > 2:
        sommaY = mean(item[2::])
        item.append(sommaY )
        yawTestArray.append(sommaY)
for item in rollRangeAndError:
    if len(item) > 2:
        sommaR = mean(item[2::])
        item.append(sommaR)
        rollTestArray.append(sommaR)

print("pitch")
for item in pitchRangeAndError:
    if len(item) > 3:

        print(str(item[0]) + str(item[1]) + " " + str(item[2]))

print("------------------")
print("yaw")
for item in yawRangeAndError:
    if len(item) > 3:

        print(str(item[0]) + str(item[1]) + " " + str(item[2]))

print("------------------")
print("roll")
for item in rollRangeAndError:
    if len(item) > 3:

        print(str(item[0]) + str(item[1]) + " " + str(item[2]))

print("------------------")

