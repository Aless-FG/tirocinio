import csv
import math
import re
import pandas as pd

import statistics
from pandas import read_csv


data = read_csv("/home/ale/Desktop/histograms/Delaunay/csvK3/graphsK3YPR.csv")

pitch = data['pitch']
del pitch[499]
del pitch[500]

yaw = data['yaw']
del yaw[499]
del yaw[500]

roll = data['roll']
del roll[499]
del roll[500]


print("Standard Deviation of pitch is % s " % (statistics.stdev(pitch)))
print("Standard Deviation of yaw is % s " % (statistics.stdev(yaw)))
print("Standard Deviation of roll is % s " % (statistics.stdev(roll)))