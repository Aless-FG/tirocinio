import ast
import csv
import math

import pandas as pd
import networkx as nx
import scipy
from karateclub import Graph2Vec
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


test = pd.read_csv("/home/ale/Desktop/histograms/csvK7/graphs1.csv", usecols=['filename', 'graph'])  # test subject
controlSet = pd.read_csv("/home/ale/Desktop/histograms/csvK7/graphK7.csv", usecols=['filename', 'graph'])
file = open('/home/ale/Desktop/histograms/csvK5/graphsManhattanK7.csv', 'w', newline='')
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

        # graph embedding
        graphs_model_H = Graph2Vec(dimensions=64)
        graph_num_H = nx.convert_node_labels_to_integers(H, first_label=0, ordering='default')
        graphs_model_H.fit([graph_num_H])
        graph_embeddings_H = graphs_model_H.get_embedding()
        print("---->TEST FILE: " + filenameTest)
        for filenameControlSet, gControlSet in zip(controlSet['filename'], controlSet['graph']):
            y = ast.literal_eval(gControlSet)
            K = nx.node_link_graph(y)

            graphs_model_K = Graph2Vec(dimensions=64)
            graph_num_K = nx.convert_node_labels_to_integers(K, first_label=0, ordering='default')
            graphs_model_K.fit([graph_num_K])
            graph_embeddings_K = graphs_model_K.get_embedding()

            distance = cityblock(graph_embeddings_H.flatten(), graph_embeddings_K.flatten())
            print(filenameControlSet + ": " + str(distance))
            dict_obj.add(filenameControlSet, distance)
            # print(nx.graph_edit_distance(H, K, node_del_cost=costNode, edge_del_cost=costEdge))
        temp = min(dict_obj.values())
        res = [key for key in dict_obj if dict_obj[key] == temp]
        print("---->TEST FILE: " + filenameTest)
        print("DOVE CAZZO SIAMO ARRIVATI?!:  " + str(ACHEPUNTOSIAMO))
        print("Keys with minimum values are : " + str(res))
        print("Min value: " + str(temp))

        writer.writerow({'filename': filenameTest,
                         'graph': res,
                         'value': temp
                         })
        dict_obj.clear()
        ACHEPUNTOSIAMO = ACHEPUNTOSIAMO + 1
    # magari creo un altro csv, ci scrivo res (nome file) nella prima colonna e temp (il minimo) nella seconda
