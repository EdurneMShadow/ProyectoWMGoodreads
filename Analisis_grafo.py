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

'''Elimina los clusters que solo contenga un nodo.'''
def seleccionar_clusters(clusters, amigos):
    lista_nueva_clusters = []     
    for cluster in clusters:
        if amigos:
            if len(cluster) >20 and len(cluster)<100:
                lista_nueva_clusters.append(cluster)
        else:
            if len(cluster) >100:
                lista_nueva_clusters.append(cluster)
    return lista_nueva_clusters

'''Obtiene una lista de listas con los libros de los usuarios de un cluster.'''
def get_libros(cluster, client, nombre):
    libros = []
    eliminados = 0
    for i in range(len(cluster)):
        try:
            books = set(client.get_books_user(cluster[i]))
            libros.append(books)
        except Exception:
            eliminados+=1
    print('Nodos eliminados: ' + str(eliminados))
    with open(nombre , 'wb') as handle:
        pickle.dump(libros, handle, protocol= pickle.HIGHEST_PROTOCOL)
    return libros

'''Ejecuta el método anterior para un conjunto de clusters.'''
def get_libros_comunidades(clusters, client):   
    for i in range(len(clusters)):
        print ('i: ' + str(i) + ' / ' + str(len(clusters)))
        get_libros(clusters[i], client, 'lista' + str(i) + '.txt') 
    
'''Devuelve la media de libros en común entre dos comunidades distintas'''    
def compare_books_comunidades_distintas(libros01, libros02):
    cont = 0  
    comunes = 0
    for i in range(len(libros01)):
        print('i: ' + str(i))
        books = set(libros01[i])
        for j in range(len(libros02)):
            print('j: ' + str(j))
            books_2 = set(libros02[j])
            if len(books) == 0 or len(books_2) == 0:
                print('Nada en común')
            else:
                comunes += len(books & books_2)
                cont+=1
    media = comunes / cont
    return media 

'''Devuelve la media de libros en común entre los usuarios de una misma comunidad''' 
def compare_books_misma_comunidad(libros):
    comunes = 0
    cont = 0
    for i in range(len(libros)):
        for j in range(i+1,len(libros)):
            print('i: ' + str(i) + ' , j: ' + str(j) + ' / ' + str(len(libros)))
            books = set(libros[i])
            books_2 = set(libros[j])
            if len(books) == 0 or len(books_2) == 0:
                print('Nada en común')
            else:
                comunes += len(books & books_2)**2
                print('Sumando')
                cont+=1
    media = comunes / cont
    return media

'''Calcula la desviación típica para una lista de medias.'''
def calculo_desviacion(medias_comunidades_iguales, media):
    suma = 0
    for i in range(len(medias_comunidades_iguales)):
        suma+=(i-media)**2
    desviacion = np.sqrt(suma / len(medias_comunidades_iguales))
    return desviacion

'''Devuelve un dataframe con datos para cada combinaciond de usuarios. Tarda muchísimo en ejecutar'''
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

#Seleccionar los clusters con los que se va a trabajar
clusters_amigos = seleccionar_clusters(nodos_amigos, True)
clusters_followers = seleccionar_clusters(nodos_followers, False)

#Sacar los libros de los clusters seleccionados           
get_libros_comunidades(clusters_amigos, client)

for i in range(25):
    nombre = 'libros'+str(i)
    txt = nombre + '.txt'
    with open(txt, 'rb') as handle :
        nombre = pickle.load(handle)

lista_libros_amigos = (lista0 + lista1 +lista2 + lista3+ lista4+lista5+lista6+
                      lista7+liesta8+lista9+lista10+lista11+lista12+lista13+
                      lista14+lista15+lista16+lista17+lista18+lista19+lista20+
                      lista21+lista22+lista23+lista24)

#Cálculo de la media de libros de cada una de las comunidades
medias_iguales_amigos = []
for i in lista_libros_amigos:
    medias_iguales_amigos.append(compare_books_misma_comunidad(i))

medias_distintas_amigos = []
for i in range(len(lista_libros_amigos)):
    for j in range(i+1, len(lista_libros_amigos)):
        medias_distintas_amigos.append(compare_books_comunidades_distintas(lista_libros_amigos[i], lista_libros_amigos[j]))

suma = 0
for i in medias_iguales_amigos:
    suma+=i
media_iguales_amigos_total = suma / len(medias_iguales_amigos)

suma = 0
for i in medias_distintas_amigos:
    suma+=i
media_distintas_amigos_total = suma / len(medias_distintas_amigos)

desviacion_iguales_amigos = calculo_desviacion(medias_iguales_amigos, media_iguales_amigos_total)
desviacion_distintas_amigos = calculo_desviacion(medias_distintas_amigos, media_distintas_amigos_total)

print('Grafo de amigos')
print('Misma comunidad: Media:' + str(media_iguales_amigos_total) + ' ,Desviacion_típica:' + str(desviacion_iguales_amigos))
print('Distintas comunidades: Media:' + str(media_distintas_amigos_total) + ' ,Desviacion_típica:' + str(desviacion_distintas_amigos))
#Análisis del grafo de followers
get_libros_comunidades(clusters_followers, client)

for i in range(25):
    nombre = 'libros'+str(i)
    txt = nombre + '.txt'
    with open(txt, 'rb') as handle :
        nombre = pickle.load(handle)

lista_libros_followers = (lista0 + lista1 +lista2 + lista3+ lista4+lista5+lista6+
                      lista7+liesta8+lista9+lista10+lista11+lista12+lista13+
                      lista14+lista15+lista16+lista17+lista18+lista19+lista20+
                      lista21+lista22+lista23+lista24)

#Cálculo de la media de libros de cada una de las comunidades
medias_iguales_followers = []
for i in lista_libros_followers:
    medias_iguales_followers.append(compare_books_misma_comunidad(i))

medias_distintas_followers = []
for i in range(len(lista_libros_followers)):
    for j in range(i+1, len(lista_libros_followers)):
        medias_distintas_followers.append(compare_books_comunidades_distintas(lista_libros_followers[i], lista_libros_followers[j]))

suma = 0
for i in medias_iguales_followers:
    suma+=i
media_iguales_followers_total = suma / len(medias_iguales_followers)

suma = 0
for i in medias_distintas_followers:
    suma+=i
media_distintas_followers_total = suma / len(medias_distintas_followers)

desviacion_iguales_followers = calculo_desviacion(medias_iguales_followers, media_iguales_followers_total)
desviacion_distintas_followers = calculo_desviacion(medias_distintas_followers, media_distintas_followers_total)

print('Grafo de followers')
print('Misma comunidad: Media:' + str(media_iguales_followers_total) + ' ,Desviacion_típica:' + str(desviacion_iguales_followers))
print('Distintas comunidades: Media:' + str(media_distintas_followers_total) + ' ,Desviacion_típica:' + str(desviacion_distintas_followers))