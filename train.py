# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import CA

def train():

    features=[]
    train=[]
    keys={}
    
    with open('train.csv','r') as dataset:
        
        for x, i in enumerate(next(dataset).split(',')):
            keys[i]=x # Initialize list of feature names
    
        features=( [ next(dataset).strip('\n').replace(' ', '').split(',') for x in range(35000) ] )
        #Way too messy
    
    dataset.close()
    
    for i in range(len(features)):
        train.append(features[i].pop())
    
    #Remove unwanted data
    
    keep_list=[] #Only keep data points where room was booked
    for i in range(len(features)):
    
        if features[i][keys['is_booking']] == '1':
            keep_list.append(i)
    
    features=[ features[i] for i in keep_list ]
    train=[ train[i] for i in keep_list ]
            
    remove=['date_time','srch_ci','srch_co','cnt']
    features = zip(*features)
    rem_list=[]
    for i in remove:
        rem_list.append(keys[i])
        
    for i in features:
        if '' in i:
            rem_list.append(features.index(i)) #Deal with nulls later
    
    features =[ features[i] for i in range(len(features)) if i not in rem_list ]
    features = zip(*features)
    
    #Make CDT
    CDT, feature_order, cluster_order = CA.make_CDT(features, train)
    
    #Run MCA
    u_p, lambda_s, u, chi_sq, psi_sq = CA.MCA(CDT)
    
    #Project clusters onto principal axes
    cluster_proj = CA.projections(CDT, u)
    
    return cluster_proj, u, feature_order