import itertools
import math
import os
from operator import attrgetter
import csv
from karateclub import Graph2Vec
from scipy.spatial.distance import cityblock
import networkx
import networkx as nx
import cv2
import glob
from math import dist
import mediapipe
import mediapipe as mp
import re
from karateclub.graph_embedding import graph2vec
from scipy.spatial import Delaunay

class Landmark:
    x = 0
    y = 0
    mosso = 0
    normalizedX = 0
    normalizedY = 0
    movedDistance = 0
    avgDistance = 0
    modulo = 0

    def __init__(self, numero):
        self.numero = numero
        self.euclideanDistanceLandmarks = []
        self.nearLandmarks = []

    def setNumero(self, numero):
        self.numero = numero

    def aumentaMosso(self):
        self.mosso = self.mosso + 1

    def getNumero(self):
        return self.numero

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setDistance(self, d):
        self.movedDistance = self.movedDistance + d

    def getDistance(self):
        return self.movedDistance

    def getAvgDistance(self):
        return self.avgDistance

    def setAvgDistance(self, avgD):
        self.avgDistance = avgD

    def getMosso(self):
        return self.mosso

    def aumentaMosso(self):
        self.mosso = self.mosso + 1

    def getNormalizedX(self):
        return self.normalizedX

    def setNormalizedX(self, x):
        self.normalizedX = x

    def getNormalizedY(self):
        return self.normalizedY

    def setNormalizedY(self, y):
        self.normalizedY = y

    def getModulo(self):
        return self.modulo

    def setModulo(self, m):
        self.modulo = m

    def getEuclideanDistanceLandmarks(self):
        return self.euclideanDistanceLandmarks

    def setEuclideanDistanceLandmarks(self, x):
        self.euclideanDistanceLandmarks.append(x)

    def getNearLandmarks(self):
        return self.nearLandmarks

    def setNearLandmarks(self, x):
        self.nearLandmarks.append(x)


drawingModule = mediapipe.solutions.drawing_utils
faceModule = mediapipe.solutions.face_mesh

directories = os.listdir("/home/ale/Desktop/biwi_rgb_renamedFixed/2/")
landmarks = []
landmarksImportanti = [
    1,
    4,
    5,
    6,
    8,
    9,
    10,
    33,
    45,
    46,
    48,
    49,
    53,
    55,
    61,
    63,
    67,
    69,
    78,
    81,
    87,
    95,
    104,
    107,
    108,
    109,
    115,
    148,
    151,
    152,
    168,
    171,
    173,
    175,
    185,
    195,
    197,
    230,
    249,
    275,
    279,
    283,
    285,
    293,
    297,
    299,
    308,
    311,
    317,
    318,
    324,
    333,
    336,
    337,
    338,
    344,
    375,
    382,
    396,
    402,
    440,
    450,
]
graphJSON = []
i = 0
x = 0
n = 0
indixeImmagini = 0
indice = 0

while x < 468:
    l = Landmark(x)
    landmarks.append(l)
    x = x + 1


def min_n_nums(nums, n=1):
    return sorted(nums, reverse=False)[:n]

connesso = 0
with faceModule.FaceMesh(static_image_mode=True) as face:
    imgs = [cv2.imread(file) for file in glob.glob("/home/ale/Desktop/biwi_rgb_renamedFixed/2/*")]
    for pic in imgs:
        results = face.process(cv2.cvtColor(pic, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks is not None:
            for faceLandmarks in results.multi_face_landmarks:
                """drawingModule.draw_landmarks(img, faceLandmarks, faceModule.FACEMESH_LIPS, circleDrawingSpec,
                                                     lineDrawingSpec)"""

                for landmark in faceLandmarks.landmark:
                    x = landmark.x
                    y = landmark.y

                    shape = pic.shape
                    relative_x = int(x * shape[1])
                    relative_y = int(y * shape[0])
                    landmarks[n].setX(relative_x)
                    landmarks[n].setY(relative_y)
                    n = n + 1

        G = nx.Graph()
        graphLandmarks = []

        # aggiungo i landmark al grafo (saranno i nodi)
        for item in landmarks:
            if item.getNumero() in landmarksImportanti:
                graphLandmarks.append(item)
                G.add_node(item.getNumero())



        for item in graphLandmarks:
            item.setModulo(math.sqrt(item.getX() ** 2 + item.getY() ** 2))

        maximumM = max(graphLandmarks, key=attrgetter('modulo')).getModulo()
        minimumM = min(graphLandmarks, key=attrgetter('modulo')).getModulo()

        for item in landmarks:  # normalizzo
            item.setNormalizedX((item.getX() - graphLandmarks[0].getX()) / (maximumM - minimumM))
            item.setNormalizedY((item.getY() - graphLandmarks[0].getY()) / (maximumM - minimumM))


        points = []

        for n in graphLandmarks:
            point = [n.getNormalizedX(), n.getNormalizedY()]
            points.append(point)
        #D = nx.complete_graph(len(points))
        D = nx.Graph()
        #D.add_nodes_from(graphLandmarks)

        for i, point in enumerate(points):
            D.add_node(i, posX=point[0], posY=point[1])

        for u in D.nodes(data=True):
            p1 = (u[1]['posX'], u[1]['posY'])
            for v in D.nodes(data=True):
                if u[0] < v[0]:
                    p2 = (v[1]['posX'], v[1]['posY'])
                    manhattanDistance = cityblock(p1, p2)
                    D.add_edge(u[0], v[0], weight=manhattanDistance)


        if nx.is_connected(D):
            connesso = connesso + 1
        
        
        n = 0
        data1 = nx.node_link_data(D)
        graphJSON.append(data1)
        print(data1)

graphID = 0
file = open('/home/ale/Desktop/histograms/Delaunay/csvK3/graph2.csv', 'w', newline='')
print(connesso)
with file:
    # identifying header
    header = ['filename', 'graph']
    writer = csv.DictWriter(file, fieldnames=header)

    # writing data row-wise into the csv file
    writer.writeheader()
    for file in directories:
        writer.writerow({'filename': file,
                         'graph': graphJSON[graphID],
                         })
        graphID = graphID + 1

