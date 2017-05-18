# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:06:08 2017

@author: Edurne
"""
%load_ext autoreload
%autoreload 2

import goodreads as gr
import grafo_amigos as ga
import grafo_followers as fog



client = gr.Client(client_id="2uQMlznVEwfI4YTVFQwsA", client_secret="DWs5Gii98b9KaYZBD9B3NL6nxE9SFRCKyUsZJIEv5Sg")
client.authenticate(access_token='2uQMlznVEwfI4YTVFQwsA',access_token_secret='"DWs5Gii98b9KaYZBD9B3NL6nxE9SFRCKyUsZJIEv5Sg')
client.authenticate()


#########   MAIN   ########       

g = ga.grafo_amigos()


#Listas de ids de reviews
r_arte = set(g.get_id_reviews('./crawler_reviews/reviews_arte.json'))
r_adolescente = set(g.get_id_reviews('./crawler_reviews/reviews_adolescente.json'))
r_clasicos = set(g.get_id_reviews('./crawler_reviews/reviews_clasicos.json'))
r_crimen = set(g.get_id_reviews('./crawler_reviews/reviews_crimen.json'))
r_espiritualidad = set(g.get_id_reviews('./crawler_reviews/reviews_espiritualidad.json'))
r_fantasia = set(g.get_id_reviews('./crawler_reviews/reviews_fantasia.json'))
r_ficcion = set(g.get_id_reviews('./crawler_reviews/reviews_ficcion.json'))
r_historico = set(g.get_id_reviews('./crawler_reviews/reviews_historico.json'))
r_infantil = set(g.get_id_reviews('./crawler_reviews/reviews_infantil.json'))
r_lgtb = set(g.get_id_reviews('./crawler_reviews/reviews_lgtb.json'))
r_manga = set(g.get_id_reviews('./crawler_reviews/reviews_manga.json'))
r_misterio = set(g.get_id_reviews('./crawler_reviews/reviews_misterio.json'))
r_musica = set(g.get_id_reviews('./crawler_reviews/reviews_musica.json'))
r_poesia = set(g.get_id_reviews('./crawler_reviews/reviews_poesia.json'))
r_romance = set(g.get_id_reviews('./crawler_reviews/reviews_romance.json'))
r_scifi = set(g.get_id_reviews('./crawler_reviews/reviews_scifi.json'))
r_suspense = set(g.get_id_reviews('./crawler_reviews/reviews_suspense.json'))
r_terror = set(g.get_id_reviews('./crawler_reviews/reviews_terror.json'))

#Listas con información de usuarios

usuarios_arte = g.get_info_usuario(r_arte,client,'arte')
usuarios_adolescente = g.get_info_usuario(r_adolescente,client,'adolescente')
usuarios_clasicos = g.get_info_usuario(r_clasicos,client,'clasicos')
usuarios_crimen = g.get_info_usuario(r_crimen,client,'crimen')
usuarios_espiritualidad = g.get_info_usuario(r_espiritualidad,client,'espiritualidad')
usuarios_fantasia = g.get_info_usuario(r_fantasia,client,'fantasia')
usuarios_ficcion = g.get_info_usuario(r_ficcion,client,'ficcion')
usuarios_historico = g.get_info_usuario(r_historico,client,'historico')
usuarios_infantil = g.get_info_usuario(r_infantil,client,'infantil')
usuarios_lgtb = g.get_info_usuario(r_lgtb,client,'lgtb')
usuarios_manga = g.get_info_usuario(r_manga,client,'manga')
usuarios_misterio = g.get_info_usuario(r_misterio,client,'misterio')
usuarios_musica = g.get_info_usuario(r_musica,client,'musica')
usuarios_poesia = g.get_info_usuario(r_poesia,client,'poesia')
usuarios_romance = g.get_info_usuario(r_romance,client,'romance')
usuarios_scifi = g.get_info_usuario(r_scifi,client,'ciencia ficcion')
usuarios_suspense = g.get_info_usuario(r_suspense,client,'suspense')
usuarios_terror = g.get_info_usuario(r_terror,client,'terror')

usuarios_primera_capa = (usuarios_arte + usuarios_adolescente + usuarios_clasicos
                         + usuarios_crimen + usuarios_espiritualidad + 
                         usuarios_fantasia + usuarios_ficcion + usuarios_historico
                         + usuarios_infantil + usuarios_lgtb + usuarios_manga + 
                         usuarios_misterio + usuarios_musica + usuarios_poesia + 
                         usuarios_romance + usuarios_scifi + usuarios_suspense + 
                         usuarios_terror)
usuarios_segunda_capa = g.get_amigos_usuarios(usuarios_primera_capa, client)
usuarios_tercera_capa = g.get_amigos_usuarios(usuarios_segunda_capa, client)


g.guardar_nodos_en_fichero(usuarios_primera_capa,True,'grafo_3capas.txt')
g.guardar_nodos_en_fichero(usuarios_segunda_capa,False,'grafo_3capas.txt')
g.guardar_nodos_en_fichero(usuarios_tercera_capa,False,'grafo_3capas.txt')

#lista=[]
#for i in usuarios_primera_capa:
#    lista.append(i['id_user'])
#for i in usuarios_segunda_capa:
#    lista.append(i['id_user'])
#for i in usuarios_tercera_capa:
#    lista.append(i['id_user'])

#g.set_lista_ids(lista)

g.get_aristas_grafo(client,'grafo_3capas.txt')
g.guardar_info_usuario_fichero(usuarios_primera_capa,1,1)
g.guardar_info_usuario_fichero(usuarios_segunda_capa,0,2)
g.guardar_info_usuario_fichero(usuarios_tercera_capa,0,2)

#Obtener followers de la primera capa de usuarios
#g.guardar_nodos_en_fichero(usuarios_primera_capa,True,'grafo_followers.txt')
#followers = fog.get_followers_usuarios(usuarios_primera_capa, client)
#g.guardar_nodos_en_fichero(followers,False,'grafo_followers.txt')
#fog.get_aristas_grafo_followers(client)
#followers2 = fog.get_followers_usuarios(followers, client)
#fog.get_aristas_grafo_followers(client)