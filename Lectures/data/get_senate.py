#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 15:13:21 2020

@author: kevinreuning
"""


import pandas as pd 
from TwitterAPI import TwitterAPI
import time
from tqdm import tqdm

data = pd.read_csv("https://raw.githubusercontent.com/CivilServiceUSA/us-senate/master/us-senate/data/us-senate.csv")



APP_KEY = 'NBa0kFD92S7aP99xyJU354HlO'
APP_SECRET = 'cOJ4dncbvsBswH79HAZPQBpz57umO5taE4hYsucfOfgMapzEsU'
 
api = TwitterAPI(APP_KEY,
                  APP_SECRET,
                  auth_type='oAuth2')

ids = []
friends = {}
for u in tqdm(data.twitter_handle):
    
    friend_list = []
    usercheck = api.request('users/lookup', {'screen_name':u}).json()
    
    if 'errors' in usercheck:
        ids.append("")
        continue
    
    ids.append(str(usercheck[0]['id']))
        
    results = api.request('friends/ids',
                             {'screen_name':u, 'count':5000}).json()
    friend_list = results['ids']
        
    while results['next_cursor'] != 0: 
        time.sleep(65)
        results = api.request('friends/ids',
                         {'screen_name':u, 'count':5000, 
                          'cursor':results['next_cursor']}).json()
        friend_list.extend(results['ids'])
        
    friend_list = [str(friend) for friend in friend_list]
    friends[usercheck[0]['id']] = friend_list
    time.sleep(65)
    
data['twitter_id'] = ids
data.to_csv("senate_data.csv", index=False)
    
set_ids = set(ids)

adj_mat = {}
for k, v in friends.items():
    lim_friends = set(v) & set_ids
    friends[k] = lim_friends
    
    adj_mat[k] = [friend in v for friend in ids]


data_out = pd.DataFrame.from_dict(adj_mat,  orient='index', columns=ids )


data_out.to_csv("senate_adj.csv")
 

        