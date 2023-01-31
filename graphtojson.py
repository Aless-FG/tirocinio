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
import matplotlib
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

directories = os.listdir("/home/ale/Desktop/biwi_rgb_renamedFixed/24/")
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


with faceModule.FaceMesh(static_image_mode=True) as face:
    imgs = [cv2.imread(file) for file in glob.glob("/home/ale/Desktop/biwi_rgb_renamedFixed/24/*")]
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

        # calcolo la distanza di ciascun landmark dagli altri landmark
        for n1 in graphLandmarks:
            point1 = (n1.getNormalizedX(), n1.getNormalizedY())
            for n2 in graphLandmarks:
                point2 = (n2.getNormalizedX(), n2.getNormalizedY())
                manDistance = cityblock(point1, point2)
                n1.setEuclideanDistanceLandmarks(manDistance)

        for item in graphLandmarks:
            for i in min_n_nums(item.getEuclideanDistanceLandmarks(),
                                8):  # prendo i 3/5/7 landmark più vicini (compreso il landmark stesso)
                landmarkIndex = item.getEuclideanDistanceLandmarks().index(
                    i)  # il primo item è sempre il landmark stesso
                if landmarkIndex >= len(graphLandmarks):
                    continue
                item.setNearLandmarks(graphLandmarks[landmarkIndex])
            del item.getNearLandmarks()[0]  # rimuovo il primo landmark dalla lista (ovvero il landmark stesso)

        for nodeU in graphLandmarks:
            pt1 = (nodeU.getNormalizedX(), nodeU.getNormalizedY())
            for nodeV in nodeU.getNearLandmarks():
                pt2 = (nodeV.getNormalizedX(), nodeV.getNormalizedY())
                manhattan = cityblock(pt1, pt2)
                G.add_edge(nodeU.getNumero(), nodeV.getNumero(), weight=manhattan)
        """for arco in G.edges:
            print(G.get_edge_data(arco[0], arco[1]))"""

        """graphs_model = Graph2Vec(dimensions=64)
        graph_num = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default')
        graphs_model.fit([graph_num])
        graph_embeddings = graphs_model.get_embedding()"""
        for item in graphLandmarks:
            item.getEuclideanDistanceLandmarks().clear()
            item.getNearLandmarks().clear()
        n = 0
        shortestTest1 = nx.shortest_path_length(G, weight="weight")
        shortestTest2 = dict(shortestTest1)
        eccTest = nx.eccentricity(G, sp=shortestTest2)
        data1 = nx.node_link_data(G)
        graphJSON.append(data1)
        print(data1)

graphID = 0
file = open('/home/ale/Desktop/histograms/csvK7/graphs24.csv', 'w', newline='')

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

"""cv2.imshow("test", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
