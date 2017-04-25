# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:06:08 2017

@author: Edurne
"""
import goodreads as gr
import json
import time as t
import bisect as b

client = gr.Client(client_id="2uQMlznVEwfI4YTVFQwsA", client_secret="DWs5Gii98b9KaYZBD9B3NL6nxE9SFRCKyUsZJIEv5Sg")
client.authenticate(access_token='2uQMlznVEwfI4YTVFQwsA',access_token_secret='"DWs5Gii98b9KaYZBD9B3NL6nxE9SFRCKyUsZJIEv5Sg')
client.authenticate()

lista_ids = []

''' Búsqueda binaria '''
def binary_search(a, x, lo=0, hi=None):
    hi = hi if hi is not None else len(a) 
    pos = b.bisect_left(a, x, lo, hi)
    return (pos if pos != hi and a[pos] == x else -1)

''' Importar ficheros con urls de reviews'''
def get_id_reviews (nombre_fichero):
    fichero_reviews=open(nombre_fichero).read()
    data = json.loads(fichero_reviews)
    id_reviews = []
    for i in data:
        link = str(i['link'])
        pos = link.find('?')
        id_reviews.append(link[38:pos])
    return id_reviews
    
''' Obtener una lista con la información de todos los usuarios de un género'''
def get_info_usuario (reviews, client, genero):
    users=[]
    for i in reviews:
        aux = client.get_review_user(i, genero)
        if binary_search(lista_ids, aux['id_user']) == -1:
            users.append(aux)
            b.insort(lista_ids,aux['id_user'])
        t.sleep(1)
    return users

'''De todos los usuarios obtenidos previamente, obtener 60 de sus amigos. Sirve para obtener los nodos
    de la segunda capa del grafo. '''        
def get_amigos_usuarios(lista_usuarios):
    amigos_lista = []
    for user in lista_usuarios:        
        try:
            amigos = client.get_friends(user['id_user'], 60)
        except Exception:
            amigos = []
        for amigo in amigos:
            if binary_search(lista_ids, str(amigo[0])) == -1:
                b.insort(lista_ids,str(amigo[0]))
                amigo_data = {}
                amigo_data['id_user'] = str(amigo[0])
                amigo_data['nombre'] = amigo[1]
                amigo_data['enlace'] = 'https://www.goodreads.com/user/show/'+str(amigo[0])
                amigo_data['is_friend_of'] = str(user['id_user']) 
                amigos_lista.append(amigo_data)
        t.sleep(1)
    return amigos_lista

''' Obtiene todos los amigos de cada uno de los ids y crea las aristas correspondientes'''    
def get_aristas_grafo():
    for id in lista_ids:
        amigos = client.get_friends(id)
        fichero = open('grafo.txt','a')
        for amigo in amigos:
            if binary_search(lista_ids,str(amigo[0])) != -1:
                fichero.write('edge [ \n')
                fichero.write('source '+ id +' \n')
                fichero.write('target '+str(amigo[0])+' \n')
                fichero.write('] \n')
        fichero.close()
                     
'''Guardar los usuarios en un fichero formato igraph'''   
def guardar_nodos_en_fichero(lista_usuarios,vacio):
    fichero = open('grafo.txt','a')
    if vacio:
        fichero.write('graph [ \n')
        fichero.write('directed 1 \n')
    for user in lista_usuarios:
        fichero.write('node [ \n')
        fichero.write('id '+user['id_user']+' \n')
        if user['nombre'] == None:
            user['nombre'] = 'J. Doe'
            print(user['nombre'])
        fichero.write('nombre_usuario '+str(user['nombre'].encode('utf-8'))+' \n')
        fichero.write('] \n')
    fichero.close()
            
def guardar_info_usuario_fichero(lista_usuarios,vacio,capa):
    fichero = open('info_usuarios.txt','a')
    if vacio:
        fichero.write('ID_usuario Nombre Enlace_usuario ID_libro Genero Review \n')
    if capa==2:
        for user in lista_usuarios:
            fichero.write(str(user['id_user']))
            fichero.write(','+user['nombre'].encode('utf-8'))
            fichero.write(','+str(user['enlace']))
            fichero.write(','+str(user['is_friend_of']))
    else:
        for user in lista_usuarios:
            fichero.write(str(user['id_user'])+','+str(user['nombre'])+','+str(user['enlace'])+','+str(user['id_libro'])+','+str(user['genero'])+','+ user['review'].encode('utf-8'))
   
    fichero.close()
        


#Listas de ids de reviews
r_arte = set(get_id_reviews('./crawler_reviews/reviews_arte.json'))
r_adolescente = set(get_id_reviews('./crawler_reviews/reviews_adolescente.json'))
r_clasicos = set(get_id_reviews('./crawler_reviews/reviews_clasicos.json'))
r_crimen = set(get_id_reviews('./crawler_reviews/reviews_crimen.json'))
r_espiritualidad = set(get_id_reviews('./crawler_reviews/reviews_espiritualidad.json'))
r_fantasia = set(get_id_reviews('./crawler_reviews/reviews_fantasia.json'))
r_ficcion = set(get_id_reviews('./crawler_reviews/reviews_ficcion.json'))
r_historico = set(get_id_reviews('./crawler_reviews/reviews_historico.json'))
r_infantil = set(get_id_reviews('./crawler_reviews/reviews_infantil.json'))
r_lgtb = set(get_id_reviews('./crawler_reviews/reviews_lgtb.json'))
r_manga = set(get_id_reviews('./crawler_reviews/reviews_manga.json'))
r_misterio = set(get_id_reviews('./crawler_reviews/reviews_misterio.json'))
r_musica = set(get_id_reviews('./crawler_reviews/reviews_musica.json'))
r_poesia = set(get_id_reviews('./crawler_reviews/reviews_poesia.json'))
r_romance = set(get_id_reviews('./crawler_reviews/reviews_romance.json'))
r_scifi = set(get_id_reviews('./crawler_reviews/reviews_scifi.json'))
r_suspense = set(get_id_reviews('./crawler_reviews/reviews_suspense.json'))
r_terror = set(get_id_reviews('./crawler_reviews/reviews_terror.json'))

#Listas con información de usuarios

usuarios_arte = get_info_usuario(r_arte,client,'arte')
usuarios_adolescente = get_info_usuario(r_adolescente,client,'adolescente')
usuarios_clasicos = get_info_usuario(r_clasicos,client,'clasicos')
usuarios_crimen = get_info_usuario(r_crimen,client,'crimen')
usuarios_espiritualidad = get_info_usuario(r_espiritualidad,client,'espiritualidad')
usuarios_fantasia = get_info_usuario(r_fantasia,client,'fantasia')
usuarios_ficcion = get_info_usuario(r_ficcion,client,'ficcion')
usuarios_historico = get_info_usuario(r_historico,client,'historico')
usuarios_infantil = get_info_usuario(r_infantil,client,'infantil')
usuarios_lgtb = get_info_usuario(r_lgtb,client,'lgtb')
usuarios_manga = get_info_usuario(r_manga,client,'manga')
usuarios_misterio = get_info_usuario(r_misterio,client,'misterio')
usuarios_musica = get_info_usuario(r_musica,client,'musica')
usuarios_poesia = get_info_usuario(r_poesia,client,'poesia')
usuarios_romance = get_info_usuario(r_romance,client,'romance')
usuarios_scifi = get_info_usuario(r_scifi,client,'ciencia ficcion')
usuarios_suspense = get_info_usuario(r_suspense,client,'suspense')
usuarios_terror = get_info_usuario(r_terror,client,'terror')

usuarios_primera_capa = usuarios_arte + usuarios_adolescente + usuarios_clasicos + usuarios_crimen + usuarios_espiritualidad + usuarios_fantasia + usuarios_ficcion + usuarios_historico + usuarios_infantil + usuarios_lgtb + usuarios_manga + usuarios_misterio + usuarios_musica + usuarios_poesia + usuarios_romance + usuarios_scifi + usuarios_suspense + usuarios_terror
usuarios_segunda_capa = get_amigos_usuarios(usuarios_primera_capa)

guardar_nodos_en_fichero(usuarios_primera_capa,1)
guardar_nodos_en_fichero(usuarios_segunda_capa,0)
guardar_info_usuario_fichero(usuarios_primera_capa,1,1)
guardar_info_usuario_fichero(usuarios_segunda_capa,0,2)



