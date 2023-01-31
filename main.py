import ast
import csv
import math
import json
import pandas as pd
import networkx as nx
import scipy
from karateclub import Graph2Vec
from networkx import eccentricity
from scipy.spatial.distance import cityblock


class CreateDictionary(dict):
    def __init__(self):
        self = dict()

        # Function to add key:value

    def add(self, key, value):
        self[key] = value


def costNode(node):
    return 1


def costEdge(edge):
    return edge["weight"]


test = pd.read_csv("/home/ale/Desktop/histograms/Delaunay/csvK3/graph1.csv", usecols=['filename', 'graph'])  # test subject
controlSet = pd.read_csv("/home/ale/Desktop/histograms/Delaunay/csvK3/graphsControlSet.csv", usecols=['filename', 'graph'])
file = open('/home/ale/Desktop/histograms/Delaunay/csvK3/graphsManhattan.csv', 'w', newline='')
dict_obj = CreateDictionary()

ACHEPUNTOSIAMO = 0

with file:
    # identifying header
    header = ['filename', 'graph', 'value']
    writer = csv.DictWriter(file, fieldnames=header)

    # writing data row-wise into the csv file
    writer.writeheader()
    for filenameTest, gTest in zip(test['filename'], test['graph']):

        x = ast.literal_eval(gTest)
        H = nx.node_link_graph(x)  # ricreo il grafo
        shortestTest1 = nx.shortest_path_length(H, weight="weight")
        shortestTest2 = dict(shortestTest1)
        eccTest = eccentricity(H, sp=shortestTest2)
        totEccTest = 0

        vectTest = []
        for flt in eccTest:
            totEccTest = totEccTest + eccTest.get(flt);
            #vectTest.append(eccTest.get(flt))
        averageEccTest = totEccTest / len(eccTest)
        #bcent = nx.barycenter(H, sp=shortest2)
        diamTest = nx.diameter(H, e=eccTest)
        radTest = nx.radius(H, e=eccTest)
        # graph embedding
        vectTest = [averageEccTest, diamTest, radTest]
        print("---->TEST FILE: " + filenameTest)
        for filenameControlSet, gControlSet in zip(controlSet['filename'], controlSet['graph']):
            y = ast.literal_eval(gControlSet)
            K = nx.node_link_graph(y)
            shortestControl1 = nx.shortest_path_length(K, weight="weight")
            shortestControl2 = dict(shortestControl1)
            eccControl = eccentricity(H, sp=shortestControl2)
            totEccControl = 0
            vectControl = []
            for flt in eccControl:
                totEccControl = totEccControl + eccControl.get(flt);
                #vectControl.append(eccTest.get(flt))
            averageEccControl = totEccControl / len(eccControl)
            # bcent = nx.barycenter(H, sp=shortest2)
            diamControl = nx.diameter(H, e=eccControl)
            radControl = nx.radius(H, e=eccControl)
            vectControl = [averageEccControl, diamControl, radControl]

            distance = cityblock(vectTest,vectControl)
            print(filenameControlSet + ": " + str(distance))
            dict_obj.add(filenameControlSet, distance)
            # print(nx.graph_edit_distance(H, K, node_del_cost=costNode, edge_del_cost=costEdge))
        temp = min(dict_obj.values())
        res = [key for key in dict_obj if dict_obj[key] == temp]
        print("---->TEST FILE: " + filenameTest)
        print("DOVE SIAMO ARRIVATI?!:  " + str(ACHEPUNTOSIAMO))
        print("Keys with minimum values are : " + str(res))
        print("Min value: " + str(temp))

        writer.writerow({'filename': filenameTest,
                         'graph': res,
                         'value': temp
                         })
        dict_obj.clear()
        ACHEPUNTOSIAMO = ACHEPUNTOSIAMO + 1
