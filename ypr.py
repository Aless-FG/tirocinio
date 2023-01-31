import ast
import csv
import math
import re
import pandas as pd
import networkx as nx
import scipy

file = open('/home/ale/Desktop/histograms/Delaunay/csvK3/graphsManhattan.csv', 'r')
file2 = open('/home/ale/Desktop/histograms/Delaunay/csvK3/graphsK3YPR.csv', 'w', newline='')
fileReader = csv.DictReader(file)
# ordine: pitch, yaw, roll
indexFile = 2
with file2:
    header = ['testGraph', 'controlSetGraph', 'pitch', 'yaw', 'roll']
    writer = csv.DictWriter(file2, fieldnames=header)

    # writing data row-wise into the csv file
    writer.writeheader()
    for col in fileReader:
        testGraph = col['\ufeffname']
        controlSetGraph = col['graph'][2:-2:]
        print(indexFile)
        testGraph = testGraph.split('_')[2].split('.png')[0]
        chunksTest = re.split('(?<=\D)(?=\d)|(?<=\d)(?=\D)', testGraph)
        pitchTest = float(chunksTest[0] + chunksTest[1] + chunksTest[2] + chunksTest[3])
        yawTest = float(chunksTest[4] + chunksTest[5] + chunksTest[6] + chunksTest[7])
        rollTest = float(chunksTest[8] + chunksTest[9] + chunksTest[10] + chunksTest[11])

        controlSetGraph = controlSetGraph.split('_')[2].split('.png')[0]
        chunksControlSet = re.split('(?<=\D)(?=\d)|(?<=\d)(?=\D)', controlSetGraph)
        pitchControlSet = float(chunksControlSet[0] + chunksControlSet[1] + chunksControlSet[2] + chunksControlSet[3])
        yawControlSet = float(chunksControlSet[4] + chunksControlSet[5] + chunksControlSet[6] + chunksControlSet[7])
        rollControlSet = float(chunksControlSet[8] + chunksControlSet[9] + chunksControlSet[10] + chunksControlSet[11])
        indexFile = indexFile + 1


        writer.writerow({'testGraph': testGraph,
                             'controlSetGraph': controlSetGraph,
                         'pitch': str(abs(pitchTest - pitchControlSet)),
                         'yaw': str(abs(yawTest - yawControlSet)),
                         'roll': str(abs(rollTest - rollControlSet))
                             })
