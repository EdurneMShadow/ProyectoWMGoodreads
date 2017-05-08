# -*- coding: utf-8 -*-
"""
Created on Mon May 08 10:44:47 2017

@author: Edurne
"""
import grafo_amigos as g
import bisect
import time as t

def get_followers_usuarios(lista_usuarios, client):
    followers_lista = []
    lista_ids = g.get_lista_ids()
    for user in lista_usuarios:        
        try:
            followers = client.get_followers(user['id_user'], 60)
        except Exception:
            followers = []
        for follower in followers:
            if g.binary_search(lista_ids, str(follower[0])) is -1:
                bisect.insort(lista_ids,str(follower[0]))
                follower_data = {}
                follower_data['id_user'] = str(follower[0])
                follower_data['nombre'] = follower[1]
                follower_data['enlace'] = 'https://www.goodreads.com/user/show/'+str(follower[0])
                follower_data['is_follower_of'] = str(user['id_user']) 
                followers_lista.append(follower_data)
        t.sleep(1)
    return followers_lista