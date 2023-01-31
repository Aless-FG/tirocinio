import os.path
import cProfile
import cv2
import itertools
import glob
import mediapipe
import numpy as np
import networkx as nx
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt
import re

class Landmark:
    x = 0
    y = 0
    mossoX = 0
    mossoY = 0

    def __init__(self, numero):
        self.numero = numero

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

    def aumentaMossoX(self):
        self.mossoX = self.mossoX + 1

    def aumentaMossoY(self):
        self.mossoY = self.mossoY + 1

    def getMossoX(self):
        return self.mossoX

    def getMossoY(self):
        return self.mossoY


drawingModule = mediapipe.solutions.drawing_utils
faceModule = mediapipe.solutions.face_mesh

circleDrawingSpec = drawingModule.DrawingSpec(thickness=1, circle_radius=0, color=(0, 255, 0))
lineDrawingSpec = drawingModule.DrawingSpec(thickness=1, color=(255, 0, 0))

# path = "/home/ale/Desktop/biwi_rgb_renamed/7"
# directories = os.listdir(path)
landmarks = []
landmarksIndexT = []
landmarksLeftEyebrow = [] # len = 8 * 2
landmarksRightEyebrow = [] # len = 8 * 2
landmarksFaceOval = [] # len = 36 * 2
landmarksLips = [] # len = 40 * 2
landmarksLeftEye = [] # len = 16 * 2
landmarksRightEye = [] # len = 16 * 2

totaleMossi = []
n = 0
i = 0
x = 0

while x < 468:
    l = Landmark(x)
    landmarks.append(l)
    x = x + 1

with faceModule.FaceMesh(static_image_mode=True) as face:
    image = cv2.imread("/home/ale/Desktop/biwi_rgb_renamed/1/frame_00003_+007.61+003.29-001.57.png")
    #images = [cv2.imread(file) for file in glob.glob("/home/ale/Desktop/biwi_rgb_renamed/1/*")]
    landmarksRightEye.append(faceModule.FACEMESH_RIGHT_EYE)
    landmarksLeftEye.append(faceModule.FACEMESH_LEFT_EYE)
    landmarksLips.append(faceModule.FACEMESH_LIPS)
    landmarksRightEyebrow.append(faceModule.FACEMESH_RIGHT_EYEBROW)
    landmarksLeftEyebrow.append(faceModule.FACEMESH_LEFT_EYEBROW)
    landmarksFaceOval.append(faceModule.FACEMESH_FACE_OVAL)


    def frozenSetToLandmark(lista):
        landmarksLipsString = str(lista)
        landmarksLipsString2 = landmarksLipsString[12:len(landmarksLipsString) - 3]
        vediamoMo = re.split('([(][^)]*[)])', landmarksLipsString2)
        listaZio = []
        listaZio.append(vediamoMo)
        del listaZio[0][00]  # cancello primo elemento
        del listaZio[0][len(listaZio[0]) - 1]  # cancello ultimo elemento
        for item in listaZio[0]:
            if item == ', ':
                listaZio[0].remove(item)

        for items in listaZio[0]:
            landmarkIndex = items.split(", ")
            landmarksIndexT.append(landmarkIndex[0][1:4])
            landmarksIndexT.append(landmarkIndex[1][:len(landmarkIndex[1]) - 1])


    frozenSetToLandmark(landmarksLips)
    frozenSetToLandmark(landmarksLeftEyebrow)
    frozenSetToLandmark(landmarksRightEyebrow)
    frozenSetToLandmark(landmarksRightEye)
    frozenSetToLandmark(landmarksLeftEye)
    frozenSetToLandmark(landmarksFaceOval)

    #for img in images:
    results = face.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_face_landmarks is not None:
        for faceLandmarks in results.multi_face_landmarks:
            """drawingModule.draw_landmarks(img, faceLandmarks, faceModule.FACEMESH_LIPS, circleDrawingSpec,
                                                 lineDrawingSpec)"""

            for landmark in faceLandmarks.landmark:

                x = landmark.x
                y = landmark.y

                shape = image.shape
                relative_x = int(x * shape[1])
                relative_y = int(y * shape[0])

                if relative_x != landmarks[n].getX():
                    landmarks[n].aumentaMossoX()
                    landmarks[n].setX(relative_x)

                if relative_y != landmarks[n].getY():
                    landmarks[n].aumentaMossoY()
                    landmarks[n].setY(relative_y)

                    # cv2.circle(image, (relative_x, relative_y), radius=0, color=(255, 0, 100), thickness=0)
                n = n + 1
                if n == 468:
                    n = 0
                    break

            # cv2.imwrite('/home/ale/Desktop/switch/test/7/' + directories[n] + f'_{n}', img)

    # cv2.circle(image, (364, 247), radius=0, color=(0, 0, 255), thickness=0) #landmark260
    #cv2.imshow('Test image', img)
    # cv2.imwrite("/home/ale/Desktop/switch/a.png" ,image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
for mossi in landmarks:
    totaleMossi.append(mossi.getMossoX() + mossi.getMossoY())

landmarksIndexT = list(dict.fromkeys(landmarksIndexT)) # rimuovo landmark duplicati
lp = 1
for l in landmarks:
    if str(l.getNumero()) in landmarksIndexT:
        print(str(l.getNumero()) + ",")
        lp = lp + 1
        #print(str(l.getNumero()))
        #print(str(l.getMossoX() + l.getMossoY()))
        cv2.circle(image, (l.getX(), l.getY()), radius=0, color=(0, 0, 255), thickness=0)
print(str(lp))
    
cv2.imshow('Test image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
