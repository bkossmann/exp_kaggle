# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 18:03:47 2016

@author: Brad Kossmann
"""

import CA
import train
import exp_io
import numpy as np
import time

#Bring in the training data
print 'training'
cluster_proj, u, feature_order = train.train()
print 'training complete'

#Begin outer for loop to go through massive file
start=0
for start in range(0,2528244,50000):
    begin=time.time()

    features, identifiers = exp_io.import_data(start)

    #Project new data onto vector space
    obs_proj=[]
    for f in features:
        m = CA.CDT_map(f, feature_order)
        opt_vec, vec_idx, overlap, overlaps = CA.max_proj(u, m)
        obs_proj.append(overlaps)

    #Determine best fit between observations and cluster projections
    results={}
    for i in range(len(obs_proj)):
        clust_idx=0
        dots=[]
        max_dots=0
    
        for j in range(len(cluster_proj)):
            curr_dot=np.dot(obs_proj[i]/np.linalg.norm(obs_proj[i]), \
            cluster_proj[j]/np.linalg.norm(cluster_proj[j]))
            dots.append(curr_dot)
            
            if curr_dot > max_dots:
                clust_idx=j
                max_dots=curr_dot
                
        results[identifiers[i]]=clust_idx
                
        #print 'observation ', i, abs(max_dots-np.average(dots))/np.std(dots)
    print time.time() - begin
        
    exp_io.export_data(results)