# -*- coding: utf-8 -*-
"""
Created on Mon May 08 10:45:42 2017

@author: Edurne
"""

import json
import time as t
import bisect
import string

class grafo_amigos:
    #Atributos de clase
    lista_ids = []
    printable = set(string.printable)
    printable.remove('"')
    
    def get_lista_ids(self):
        return self.lista_ids
        
    def set_lista_ids(self, lista):
        self.lista_ids = lista
    
    
    ''' Búsqueda binaria '''
    def binary_search(self, a, x, lo=0, hi=None):
        hi = hi if hi is not None else len(a) 
        pos = bisect.bisect_left(a, x, lo, hi)
        return (pos if pos != hi and a[pos] == x else -1)
    
    ''' Importar ficheros con urls de reviews'''
    def get_id_reviews (self, nombre_fichero):
        fichero_reviews=open(nombre_fichero).read()
        data = json.loads(fichero_reviews)
        id_reviews = []
        for i in data:
            link = str(i['link'])
            pos = link.find('?')
            id_reviews.append(link[38:pos])
        return id_reviews
        
    ''' Obtener una lista con la información de todos los usuarios de un género'''
    def get_info_usuario (self, reviews, client, genero):
        users=[]
        for i in reviews:
            aux = client.get_review_user(i, genero)
            if self.binary_search(self.lista_ids, aux['id_user']) == -1:
                users.append(aux)
                bisect.insort(self.lista_ids,aux['id_user'])
            t.sleep(1)
        return users
    
    '''De todos los usuarios obtenidos previamente, obtener 60 de sus amigos. Sirve para obtener los nodos
        de la segunda capa del grafo. '''        
    def get_amigos_usuarios(self, lista_usuarios, client):
        amigos_lista = []
        for user in lista_usuarios:        
            try:
                amigos = client.get_friends(user['id_user'], num=60)
            except Exception:
                amigos = []
            for amigo in amigos:
                if self.binary_search(self.lista_ids, str(amigo[0])) == -1:
                    bisect.insort(self.lista_ids,str(amigo[0]))
                    amigo_data = {}
                    amigo_data['id_user'] = str(amigo[0])
                    amigo_data['nombre'] = amigo[1]
                    amigo_data['enlace'] = 'https://www.goodreads.com/user/show/'+str(amigo[0])
                    amigo_data['is_friend_of'] = str(user['id_user']) 
                    amigos_lista.append(amigo_data)
            t.sleep(1)
        return amigos_lista
    
    '''Guardar los usuarios en un fichero formato igraph'''   
    def guardar_nodos_en_fichero(self, lista_usuarios,vacio,nombre_fichero):
        fichero = open(nombre_fichero,'a')
        if vacio:
            fichero.write('graph [ \n')
            fichero.write('directed 1 \n')
        for user in lista_usuarios:
            fichero.write('node [ \n')
            fichero.write('id '+user['id_user']+' \n')
            if user['nombre'] == None:
                user['nombre'] = 'J. Doe'
            usuario=''   
            for i in range (len (user['nombre'])):
                if user['nombre'][i] in self.printable:
                    usuario+=user['nombre'][i]
            if usuario.isspace() or len(usuario) == 0:
                usuario = 'J.Doe'            
                
            fichero.write('nombre_usuario '+'"'+usuario+'"' +' \n')
            fichero.write('] \n')
        fichero.close()
        
    ''' Obtiene todos los amigos de cada uno de los ids y crea las aristas correspondientes'''    
    def get_aristas_grafo(self, client):
        for id in self.lista_ids:
            try:
                amigos = client.get_friends(id)
            except Exception:
                amigos = []
            fichero = open('grafo.txt','a')
            for amigo in amigos:
                if self.binary_search(self.lista_ids,str(amigo[0])) != -1:
                    fichero.write('edge [ \n')
                    fichero.write('source '+ id +' \n')
                    fichero.write('target '+ str(amigo[0])+' \n')
                    fichero.write('] \n')
            fichero.close()
                         
    ''' Crea el fichero de información de los usuarios'''            
    def guardar_info_usuario_fichero(self, lista_usuarios,vacio,capa):
        fichero = open('info_usuarios.txt','a')
        if vacio:
            fichero.write('ID_usuario Nombre Enlace_usuario ID_libro Genero Review \n')
        if capa==2:
            for user in lista_usuarios:
                fichero.write(str(user['id_user']))
                fichero.write(','+user['nombre'].encode('utf-8'))
                fichero.write(','+str(user['enlace']))
                fichero.write(','+str(user['is_friend_of'])+' \n')
        else:
            for user in lista_usuarios:
                fichero.write(str(user['id_user'])+','+str(user['nombre'].encode('utf-8'))+','+str(user['enlace'])+','+str(user['id_libro'])+','+str(user['genero'])+','+ user['review'].encode('utf-8'))
       
        fichero.close()