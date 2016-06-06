# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 09:09:12 2016

@author: Brad Kossmann

Terminology and notation follows "Data Analysis" 2009 by Gerard Govaert 
"""

'''
The purpose of make_tables is to take a raw array of features and create a 
complete disjunctive table and a Burt tablr from them for MCA.
feature_array comes in as rows of data points.

This implementation takes advantage of the fact that summing rows in a CDT does
not affect the result of the CA calculations. Each candidate (individual here)
is combined.
!!! Only CDT table implemented for now.

Returns 3 arrays:
2D CDT array of ints
list of feature orders in CDT
list of individual orders in CDT
'''
import numpy as np
from collections import Counter

def make_CDT(feature_array, training_set): #Arrays of strings
    
    #Make dict of possible outcomes
    individuals=dict(Counter(training_set))
            
    #Need list of sub categories for columns
    feature_array=zip( *feature_array )
    sub_cats=[]
    for i in range(len(feature_array)):
        sub_cats.append(dict(Counter(feature_array[i])))
    feature_array=zip( *feature_array )
    
    #Populate CDT as dictionary of lists by sub-category
    CDT={}
    for i in range(len(sub_cats)):
        for key, value in sub_cats[i].iteritems():
            CDT[str(i)+'-'+key]=[0]*( len(individuals)+1 )
            
    ind_order=[] #Returning the order of the individuals may come in handy
    for key, value in individuals.iteritems():
        
        #Populate list of all observations from individual 'key'
        ind_group=[ feature_array[x] for x in range(len(training_set)) \
        if training_set[x] == key]
            
        ind_group=zip( *ind_group )
        
        for i in range(len(ind_group)):
            for j in ind_group[i]:
                CDT[str(i)+'-'+str(j)][int(key)]+=1
                
        ind_order.append(key)
    
    CDT_array=[]
    cat_order=[] #output order of the sub-categories
    for key, value in CDT.iteritems():
        cat_order.append(key)
        CDT_array.append(list(value))
        
    CDT_array = zip(*CDT_array) #More intuitive to return by row-individual not row-feature
                
    return CDT_array, cat_order, ind_order
    
'''
The MCA function essentially performs correspondence analysis on a CDT. The following
processes are performed:
1) Create independence model and frequency table
2) Calculate psi and chi squared
2) Perform SVD on CDT, return eigenvectors and eigenvalues
'''

def MCA(CDT):
    CDT_T=zip(*CDT)
    sum_i=[ float(sum(i)) for i in CDT] #Row sums
    sum_j=[ float(sum(i)) for i in CDT_T] #Column sums

    n=float(sum(sum_i)) # Total sum, should be == sum(sum_j)

    #Create frequency table and independence model (frequency)
    independence=[]   
    frequency=[]
    for i in range(len(CDT)):
        independence.append([])
        frequency.append([])
        for j in range(len(CDT[i])):
            fij=sum_i[i]*sum_j[j]/n**2
            independence[i].append(fij)
            frequency[i].append(CDT[i][j]/n)
            
    #Transform CDT
    X=[]
    for i in range(len(CDT)):
        X.append([])
        for j in range(len(CDT[i])):
            X[i].append((CDT[i][j]*n/sum_j[j])-1)
    
    #Using numpy's out-of-the-box SVD routine here for simplicity
    u_p, s, u = np.linalg.svd(X, full_matrices=0)

    #Calculate psi and chi squared
    psi_sq=0
    for i in range(len(frequency)):
        for j in range(len(frequency)):
            if independence[i][j] > 0:
                psi_sq+=((frequency[i][j]-independence[i][j])**2)/independence[i][j]
    chi_sq=psi_sq/n

    return u_p, s, u, chi_sq, psi_sq
    
'''
The projections function takes in eigenvectors and observations and returns
lists of each observation's projection onto each eigenvector. While presented
here for MCA, it is a general function for any set of observations and 
vectors.
'''
def projections(observations, evecs):
    
    proj_array=[]
    
    for i in range(len(observations)):
        proj_array.append([])
        
        for j in range(len(evecs)):
            proj_array[i].append(np.dot(observations[i], evecs[j]))
            
    return proj_array
    
'''
The CDT_map function maps an observation into the transformed CDT space. 
The observation is then able to be projected onto individual eigenvectors.
feature_order is the same as returned by the make_CDT function
observation is any observation that can be mapped onto the features
'''
def CDT_map(observation, feature_order):
    
    features={} #Set up dictionary
    for i in range(len(feature_order)):
        features[feature_order[i]]=i
        
    mapped=[0]*len(feature_order)
    for i in range(len(observation)):
        if str(i)+'-'+str(observation[i]) in features:
            mapped[features[str(i)+'-'+str(observation[i])]]=1
        
    return mapped
    
'''
The max_proj function takes in a list of eigenvectors and an observation
(e.g. CDT_map), normalizes the obseration, and returns the greatest 
projection, as well as the magnitude.
individual_order from make_CDT
vector_list from MCA
mapped_obs from CDT_map
'''
def max_proj(vector_list, mapped_obs):
    mapped_obs = mapped_obs/np.linalg.norm(mapped_obs)
    #print individual_order
    
    max_overlap=0
    overlaps=[]
    for i in range(len(vector_list)):
        overlap = np.dot(vector_list[i], mapped_obs)
        overlaps.append(overlap)
        if overlap > max_overlap:
            max_overlap = overlap
            opt_vec = vector_list[i]
            vec_idx = i
            
    return opt_vec, vec_idx, max_overlap, overlaps