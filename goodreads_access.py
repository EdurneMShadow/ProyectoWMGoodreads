# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:06:08 2017

@author: Edurne
"""
import goodreads as gr

client = goodreads.Client(client_id="2uQMlznVEwfI4YTVFQwsA", client_secret="DWs5Gii98b9KaYZBD9B3NL6nxE9SFRCKyUsZJIEv5Sg")
client.authenticate(access_token='2uQMlznVEwfI4YTVFQwsA',access_token_secret='"DWs5Gii98b9KaYZBD9B3NL6nxE9SFRCKyUsZJIEv5Sg')
client.authenticate()
amigos = client.get_friends('2195441',num=10)
