# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:06:08 2017

@author: Edurne
"""
import goodreads as gr
import json
import time as t

client = gr.Client(client_id="2uQMlznVEwfI4YTVFQwsA", client_secret="DWs5Gii98b9KaYZBD9B3NL6nxE9SFRCKyUsZJIEv5Sg")
client.authenticate(access_token='2uQMlznVEwfI4YTVFQwsA',access_token_secret='"DWs5Gii98b9KaYZBD9B3NL6nxE9SFRCKyUsZJIEv5Sg')
client.authenticate()
#amigos = client.get_friends('2195441',num=10)

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
        users.append(aux)    
        t.sleep(1)
    return users

 '''Guardar los usuarios en un fichero formato igraph'''   
def guardar_en_fichero(lista_usuarios):
    fichero = open('grafo.txt','a')
    for user in lista_usuarios:
        fichero.write('node [ \n')
        fichero.write('id '+user['id_user']+' \n')
        fichero.write('nombre_usuario '+user['nombre']+' \n')
        fichero.write('] \n')
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

#Listas con información de usuarios + guardar en fichero

usuarios_arte = get_info_usuario(r_arte,client,'arte')
guardar_en_fichero(usuarios_arte)

usuarios_adolescente = get_info_usuario(r_adolescente,client,'adolescente')
guardar_en_fichero(usuarios_adolescente)

usuarios_clasicos = get_info_usuario(r_clasicos,client,'clasicos')
guardar_en_fichero(usuarios_clasicos)

usuarios_crimen = get_info_usuario(r_crimen,client,'crimen')
guardar_en_fichero(usuarios_crimen)

usuarios_espiritualidad = get_info_usuario(r_espiritualidad,client,'espiritualidad')
guardar_en_fichero(usuarios_espiritualidad)

usuarios_fantasia = get_info_usuario(r_fantasia,client,'fantasia')
guardar_en_fichero(usuarios_fantasia)

usuarios_ficcion = get_info_usuario(r_ficcion,client,'ficcion')
guardar_en_fichero(usuarios_ficcion)

usuarios_historico = get_info_usuario(r_historico,client,'historico')
guardar_en_fichero(usuarios_historico)

usuarios_infantil = get_info_usuario(r_infantil,client,'infantil')
guardar_en_fichero(usuarios_infantil)

usuarios_lgtb = get_info_usuario(r_lgtb,client,'lgtb')
guardar_en_fichero(usuarios_lgtb)

usuarios_manga = get_info_usuario(r_manga,client,'manga')
guardar_en_fichero(usuarios_manga)

usuarios_misterio = get_info_usuario(r_misterio,client,'misterio')
guardar_en_fichero(usuarios_misterio)

usuarios_musica = get_info_usuario(r_musica,client,'musica')
guardar_en_fichero(usuarios_musica)

usuarios_poesia = get_info_usuario(r_poesia,client,'poesia')
guardar_en_fichero(usuarios_poesia)

usuarios_romance = get_info_usuario(r_romance,client,'romance')
guardar_en_fichero(usuarios_romance)

usuarios_scifi = get_info_usuario(r_scifi,client,'ciencia ficcion')
guardar_en_fichero(usuarios_scifi)

usuarios_suspense = get_info_usuario(r_suspense,client,'suspense')
guardar_en_fichero(usuarios_suspense)

usuarios_terror = get_info_usuario(r_terror,client,'terror')
guardar_en_fichero(usuarios_terror)









