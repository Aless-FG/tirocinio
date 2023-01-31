import math
from operator import attrgetter

from karateclub import Graph2Vec
from networkx import eccentricity
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

circleDrawingSpec = drawingModule.DrawingSpec(thickness=1, circle_radius=0, color=(0, 255, 0))
lineDrawingSpec = drawingModule.DrawingSpec(thickness=1, color=(255, 0, 0))

# directories = os.listdir(path)
landmarks = []

landmarksImportanti = [
    1, 4, 195, 197, 6, 168, 8, 9, 49, 279, 115, 45, 275, 440, 344, 279, 48, 378, 450, 148, 152, 377, 230, 147, 411, 151,
    108, 69, 104, 337, 299, 333, 396, 5, 171, 175, 10, 21, 33, 46, 53, 54, 55, 58, 61, 63, 67, 70, 78, 81, 87, 93, 95,
    103, 107, 109, 127, 132, 136, 148, 149, 150, 152, 162, 172, 173, 176, 185, 234, 249, 251, 263, 276, 283, 284, 285,
    288, 293, 297, 300, 308, 311, 317, 318, 323, 324, 332, 336, 338, 356, 361, 365, 375, 377, 378, 379, 382, 389, 397,
    400, 402, 454, 466]
i = 0
x = 0
n = 0
while x < 468:
    l = Landmark(x)
    landmarks.append(l)
    x = x + 1


def min_n_nums(nums, n=1):
    return sorted(nums, reverse=False)[:n]


with faceModule.FaceMesh(static_image_mode=True) as face:
    image = cv2.imread("/home/ale/Desktop/biwi_rgb_renamed/1/frame_00003_+007.61+003.29-001.57.png")  # posa frontale
    results = face.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_face_landmarks is not None:
        for faceLandmarks in results.multi_face_landmarks:
            for landmark in faceLandmarks.landmark:
                x = landmark.x
                y = landmark.y

                shape = image.shape
                relative_x = int(x * shape[1])
                relative_y = int(y * shape[0])
                landmarks[n].setX(relative_x)
                landmarks[n].setY(relative_y)
                n = n + 1
n = 0

for item in landmarks:
    item.setModulo(math.sqrt(item.getX() ** 2 + item.getY() ** 2))

maximumM = max(landmarks, key=attrgetter('modulo')).getModulo()
minimumM = min(landmarks, key=attrgetter('modulo')).getModulo()

for item in landmarks:  # normalizzo landmark posa frontale
    item.setNormalizedX((item.getX() - landmarks[1].getX()) / (maximumM - minimumM))
    item.setNormalizedY((item.getY() - landmarks[1].getY()) / (maximumM - minimumM))

with faceModule.FaceMesh(static_image_mode=True) as face:

    images = [cv2.imread(file) for file in glob.glob("/home/ale/Desktop/biwi_rgb_renamedFixed/1/*")]

    for img in images:
        results = face.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks is not None:
            for faceLandmarks in results.multi_face_landmarks:
                for landmark in faceLandmarks.landmark:

                    x = landmark.x
                    y = landmark.y

                    shape = img.shape
                    relative_x = int(x * shape[1])
                    relative_y = int(y * shape[0])

                    if relative_x != landmarks[n].getX() or relative_y != landmarks[n].getY():
                        landmarks[n].aumentaMosso()
                        relative_x_norm = (relative_x - landmarks[1].getX()) / (maximumM - minimumM)
                        relative_y_norm = (relative_y - landmarks[1].getY()) / (maximumM - minimumM)
                        p1 = (relative_x_norm, relative_y_norm)
                        p2 = (landmarks[n].getNormalizedX(), landmarks[n].getNormalizedY())
                        dist_math = dist(p1, p2)
                        landmarks[n].setDistance(dist_math)

                    n = n + 1
                    if n == 468:
                        n = 0
                        break


for item in landmarks:
    item.setAvgDistance(item.getDistance() / item.getMosso())
    # print(str(item.getAvgDistance()))

sortedByAvgDistance = sorted(landmarks, key=lambda h: h.avgDistance, reverse=True)
chosenLandmarks = []
for item in landmarks:
    if item.getAvgDistance() > 0.39:
        chosenLandmarks.append(item)
G = nx.Graph()
graphLandmarks = []

# aggiungo i landmark al grafo (saranno i nodi)
for item in chosenLandmarks:
    if item.getNumero() in landmarksImportanti:
        graphLandmarks.append(item)
        G.add_node(item.getNumero())

# calcolo la distanza di ciascun landmark dagli altri landmark
for n1 in graphLandmarks:
    point1 = (n1.getNormalizedX(), n1.getNormalizedY())
    for n2 in graphLandmarks:
        point2 = (n2.getNormalizedX(), n2.getNormalizedY())
        manDistance = cityblock(point1, point2)
        n1.setEuclideanDistanceLandmarks(manDistance)



"""for item in graphLandmarks:
    for i in min_n_nums(item.getEuclideanDistanceLandmarks(),
                        4):  # prendo i 3/5/7 landmark più vicini (compreso il landmark stesso (da cancellare))
        landmarkIndex = item.getEuclideanDistanceLandmarks().index(i)  # il primo item è sempre il landmark stesso
        item.setNearLandmarks(graphLandmarks[landmarkIndex])
    del item.getNearLandmarks()[0]  # rimuovo il primo landmark dalla lista (ovvero il landmark stesso)

for nodeU in graphLandmarks:
    pt1 = (nodeU.getNormalizedX(), nodeU.getNormalizedY())
    for nodeV in nodeU.getNearLandmarks():
        pt2 = (nodeV.getNormalizedX(), nodeV.getNormalizedY())
        manhattan = cityblock(pt1, pt2)
        G.add_edge(nodeU.getNumero(), nodeV.getNumero(), weight=manhattan)
for arco in G.edges:
    print(G.get_edge_data(arco[0], arco[1]))"""

for nodeU in graphLandmarks:
    startPoint = (nodeU.getX(), nodeU.getY())
    for nodeV in nodeU.getNearLandmarks():
        endPoint = (nodeV.getX(), nodeV.getY())

        cv2.line(image, startPoint, endPoint, color=(255, 250, 255), thickness=1)



"""data1 = nx.node_link_data(G)
print(data1)"""

cv2.imshow("test", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
