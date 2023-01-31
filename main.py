import os
import cProfile
import matplotlib.pyplot as plt
import cv2
import glob
from retinaface import RetinaFace


img = cv2.imread("/home/ale/Desktop/biwi_rgb_renamedFixed/1/frame_00003_+007.61+003.29-001.57.png")
#images = [cv2.imread(file) for file in glob.glob("/home/ale/Desktop/biwi_rgb_renamed/1/*")]
#directories = os.listdir("/home/ale/Desktop/immagini_scartate_mediapipe/24")
#print(len(images))
n = 0
obj = RetinaFace.detect_faces("/home/ale/Desktop/biwi_rgb_renamedFixed/1/frame_00003_+007.61+003.29-001.57.png")
"""for img in images:
    obj = RetinaFace.detect_faces(images[n])
    #print("Leggendo file: " + directories[n])
    #'face_1' -> nome key
"""

for key in obj.keys():
    print("Numero volti: " + str(len(obj.keys())))
    identity = obj[key]
    #print(identity)
    #print(n)
    facial_area = identity["facial_area"]
    cv2.rectangle(img, (facial_area[2], facial_area[3])
                  , (facial_area[0], facial_area[1]), (255, 255, 255), 1)

    facial_img = img[facial_area[1]: facial_area[3], facial_area[0]: facial_area[2]]
    #cv2.imwrite('/home/ale/Desktop/switch/testRetinaFace/24/a.png' + f'_{n}', img)
    #n = n + 1
#Draw a red circle with zero radius and -1 for filled circle
img = cv2.circle(img, (322,253), radius=0, color=(0, 0, 255), thickness=2) #rightEye
img = cv2.circle(img, (342,272), radius=0, color=(0, 0, 255), thickness=2) #naso
img = cv2.circle(img, (361, 252), radius=0, color=(0, 0, 255), thickness=2) #leftEye
img = cv2.circle(img, (326,292), radius=0, color=(0, 0, 255), thickness=2) #mouthRight
img = cv2.circle(img, (359,291), radius=0, color=(0, 0, 255), thickness=2) #mouthLeft




cv2.imshow("test", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
