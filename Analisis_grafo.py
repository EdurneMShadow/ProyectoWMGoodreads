#from igraph import *
#import cairo
#import myigraph as myg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
import time as t
import copy

'''Cargar grafo de usuarios'''
def cargar_grafos():
    g = Graph.Read_GML('grafo_4capas.gml')
    f = Graph.Read_GML('grafo_followers_3capas.gml')

'''Crea una imagen con los nodos y aristas del grafo'''
def pintar_grafos():
    myg._plot(g,filename='usuarios.png')
    print ('Pintado grafo de amigos')
    
    myg._plot(g,filename='followers.png')
    print ('Pintado grafo de followers')

'''Devuelve las medidas típicas de un grafo: número de nodos, de aristas, tamaño de la componente conexa'''
def analizarValidezGrafo(g):
    nodos = g.vcount()
    print ('Número de nodos: ' + str(nodos))
    aristas = g.ecount()
    print ('Número de aristas: ' + str(aristas))
    
    #Cálculo de la componente conexa
    cc = g.clusters(mode=STRONG)
    max = 0
    for i in cc:
        if len(i) > max:
            max = len(i)
            nodos = i
            
    print (max)
    print (nodos)
    
    #Cálculo de la densidad del grafo
    d = g.density(loops=False)
    print (d)
 
'''Obtiene los ids de los nodos que forman cada comunidad. Devuelve una lista de listas.'''
def obtener_nodos_comunidades(comunidades):
    nodos_clusters=[]
    grafos = comunidades.subgraphs()
    for g in grafos:
        lista_nodos = []
        for v in g.vs:
            lista_nodos.append(int(v['id']))
        nodos_clusters.append(lista_nodos)
    return nodos_clusters

'''Elimina los clusters que solo contenga un nodo'''
def eliminar_clusters_pequenos(clusters):
    lista_nueva_clusters = [] 
    
    for cluster in clusters:
         if len(cluster) >1:
             lista_nueva_clusters.append(cluster)
    return lista_nueva_clusters

def eliminar_perfiles_privados(clusters,client):
    for i in clusters:
        for j in i:
            try:
                 client.get_books_user(j)
            except Exception:
                print(j)
                i.remove(j)
    return clusters

def eliminar_clusters_vacios(clusters):
    copia_clusters = clusters.copy()
    for i in clusters:
        if len(i) == 0:
            copia_clusters.remove(i)
    return copia_clusters

def compare_books(comunidades,client):
    df = pd.DataFrame(columns=['Usuario_01','Usuario_02','N_libros_comunes','% de U01','% de U02','Misma_comunidad'])
    cont = 0
    copia_comunidades = copy.deepcopy(comunidades)
    libros = {}
    eliminados = 0
    for i in range(len(comunidades)):
        for j in range(len(comunidades[i])):
            try:
                books = set(client.get_books_user(comunidades[i][j]))
                libros[comunidades[i][j]] = books
            except Exception:
                copia_comunidades[i].remove(comunidades[i][j])
                eliminados+=1
    print('Nodos eliminados: ' + str(eliminados))
    for i in range(len(copia_comunidades)):
        print('i: ' + str(i))
        for ii in range(i, len(copia_comunidades)):
            print('ii: ' + str(ii))
            for j in range(len(copia_comunidades[i])):
                print('j: ' + str(j))
                indice_inicial = 0
                if i == ii:
                    indice_inicial = j+1
                for jj in range(indice_inicial,len(copia_comunidades[ii])):
                    print('jj: ' + str(jj))
                    fila = []
                    fila.append(int(copia_comunidades[i][j]))
                    fila.append(int(copia_comunidades[ii][jj]))
                    books = libros[str(copia_comunidades[i][j])]
                    books_2 = libros[str(copia_comunidades[ii][jj])]
                    if len(books) == 0 or len(books_2) == 0:
                        fila.append(0)
                        fila.append(0)
                        fila.append(0)
                    else:
                        comunes = books & books_2
                        fila.append(len(comunes))
                        fila.append(len(comunes)/len(books)*100)
                        fila.append(len(comunes)/len(books_2)*100)
                    if i == ii:
                        fila.append('si')  
                    else:
                        fila.append('no') 
                    df.loc[cont] = fila
                    cont+=1
    return df
  
def compare_books_comunidades_distintas(comunidades, client):
    df = pd.DataFrame(columns=['Usuario_01','Usuario_02','N_libros_comunes','% de U01','% de U02','Misma_comunidad'])
    cont = 0
    for i in range(len(comunidades)):
        for j in comunidades:
            if i > j:
                for ii in i:
                    user = ii
                    books = set(client.get_books_user(user))
                    for jj in j:
                        fila = []
                        user_2 = jj
                        books_2 = set(client.get_books_user(user))
                        if len(books) == 0 or len(books_2) == 0:
                            fila.append(0)
                            fila.append(0)
                            fila.append(0)
                            fila.append('no')
                        else:
                            comunes = books & books_2
                            fila.append(len(comunes))
                            fila.append(len(comunes)/len(books)*100)
                            fila.append(len(comunes)/len(books_2)*100)
                            fila.append('no')  
                        df.loc[cont] = fila
                        cont+=1
                        
    return df

def compare_books_total(comunidades, client):
    frames = []
    for i in comunidades:
        frames.append(compare_books_misma_comunidad(i,client))
    df = pd.concat(frames)


#Detección de comunidades
comunidades_amigos = Graph.as_undirected(g).community_multilevel(weights=None, return_levels=False)
comunidades_followers = f.comunidades_followers = f.community_infomap(edge_weights=None, vertex_weights=None, trials=10)


#Guarda las variables en un fichero
nodos_amigos = obtener_nodos_comunidades(comunidades_amigos)
with open('nodos_amigos.txt', 'wb') as handle:
    pickle.dump(nodos_amigos, handle, protocol= pickle.HIGHEST_PROTOCOL)

nodos_followers = obtener_nodos_comunidades(comunidades_followers)
with open('nodos_followers.txt', 'wb') as handle:
    pickle.dump(nodos_followers, handle, protocol= pickle.HIGHEST_PROTOCOL)

#Recupera las variables de un fichero
with open('nodos_amigos.txt', 'rb') as handle :
    nodos_amigos = pickle.load(handle)
    
with open('nodos_followers.txt', 'rb') as handle :
    nodos_followers = pickle.load(handle)


clusters_amigos = eliminar_clusters_pequenos(nodos_amigos)
clusters_followers = eliminar_clusters_pequenos(nodos_followers)



            






