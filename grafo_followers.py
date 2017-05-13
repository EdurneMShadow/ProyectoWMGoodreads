# -*- coding: utf-8 -*-
"""
Created on Mon May 08 10:44:47 2017

@author: Edurne
"""
import grafo_amigos as ga
import bisect
import time as t

g = ga.grafo_amigos()
lista_users = g.get_lista_ids()

def get_followers_usuarios(lista_usuarios, client):
    followers_lista = []
    for user in lista_usuarios:        
        try:
            followers = client.get_followers(user['id_user'], num=60)
        except Exception:
            followers = []
        for follower in followers:
            if g.binary_search(lista_users, str(follower[0])) is -1:
                bisect.insort(lista_users,str(follower[0]))
                follower_data = {}
                follower_data['id_user'] = str(follower[0])
                follower_data['nombre'] = follower[1]
                follower_data['enlace'] = 'https://www.goodreads.com/user/show/'+str(follower[0])
                follower_data['is_follower_of'] = str(user['id_user']) 
                followers_lista.append(follower_data)
        t.sleep(1)
    return followers_lista
    
''' Obtiene todos los amigos de cada uno de los ids y crea las aristas correspondientes'''    
def get_aristas_grafo_followers(client):
    for id in lista_users:
        try:
            followers = client.get_followers(id)
            print (id)
        except Exception:
            followers = []
        fichero = open('grafo_followers.txt','a')
        for follower in followers:
            if g.binary_search(lista_users,str(follower[0])) != -1:
                fichero.write('edge [ \n')
                fichero.write('source '+ str(follower[0]) +' \n') #seguidor
                fichero.write('target '+ id +' \n') #seguido
                fichero.write('] \n')
        fichero.close()