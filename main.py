import csv
import math
import re

from pandas import read_csv


def sortSecond(val):
    return val[1]


col_names = ["testGraph", "avg"]
data1 = read_csv("/home/ale/Desktop/histograms/Delaunay/csvK3/graphsK3YPR.csv", usecols=col_names)
data2 = read_csv("/home/ale/Desktop/histograms/csvK5/graphsK5YPR.csv", usecols=col_names)

avgData = data1.values
avg1 = []
avg2 = []

for item in avgData:
    avg1.append(item)
avg1.sort(key=sortSecond, reverse=True)

avgData = data2.values
for item in avgData:
    avg2.append(item)
avg2.sort(key=sortSecond, reverse=True)

for item1, item2 in zip(avg1, avg2):
    print(item1)
    print(item2)
    print("-------------")
