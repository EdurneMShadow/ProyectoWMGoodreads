from igraph import *

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cairo
#import myigraph as myg

# ### Cargar grafo de usuarios

import pickle

g = Graph.Read_GML('grafo_4capas.gml')
f = Graph.Read_GML('grafo_followers_3capas.gml')

#pintar grafo de amigos
myg._plot(g,filename='usuarios.png')
print 'He terminado'

myg._plot(g,filename='followers.png')
print 'He terminado'

#Número de nodos y aristas
def analizarValidezGrafo(g):
    nodos = g.vcount()
    print 'Número de nodos: ' + str(nodos)
    aristas = g.ecount()
    print 'Número de aristas: ' + str(aristas)
    
    #Cálculo de la componente conexa
    cc = g.clusters(mode=STRONG)
    max = 0
    for i in cc:
        if len(i) > max:
            max = len(i)
            nodos = i
            
    print max
    print nodos
    
    #Cálculo de la densidad del grafo
    d = g.density(loops=False)
    print d

'''Detección de comunidades con el algoritmo de Girvan Newman'''
comunidades_amigos = Graph.as_undirected(g).community_multilevel(weights=None, return_levels=False)
comunidades_followers = f.comunidades_followers = f.community_infomap(edge_weights=None, vertex_weights=None, trials=10)

def obtener_nodos_comunidades(comunidades):
    nodos_clusters=[]
    grafos = comunidades.subgraphs()
    for g in grafos:
        lista_nodos = []
        for v in g.vs:
            lista_nodos.append(int(v['id']))
        nodos_clusters.append(lista_nodos)
    return nodos_clusters

nodos_amigos = obtener_nodos_comunidades(comunidades_amigos)
with open('nodos_amigos.txt', 'wb') as handle:
    pickle.dump(nodos_amigos, handle, protocol= pickle.HIGHEST_PROTOCOL)

#with open('nodos_amigos.txt', 'rb') as handle :
#    Var = pickle.load(handle)
