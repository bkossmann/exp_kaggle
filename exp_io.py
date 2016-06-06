# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 18:18:11 2016

@author: Brad Kossmann
"""

def import_data(start):
    features=[]
    identifier=[]
    keys={}
    print 'importing data range ', start, ' ', start+50000
    
    if start+50000 <= 2528244:
        numlines=50000
    else:
        numlines = 2528244 - start - 1
    
    with open('test.csv','r') as dataset:
        
        for x, i in enumerate(next(dataset).split(',')):
            keys[i]=x # Initialize list of feature names
        for i in range(start):
            next(dataset)
            
        features=( [ next(dataset).strip('\n').replace(' ', '').split(',') for x in range(numlines) ] )
    
    dataset.close()
    
    #Remove unwanted data
        
    remove=['date_time','srch_ci','srch_co','cnt']
    features = zip(*features)
    rem_list=[]
    for i in remove:
        if i in keys:
            rem_list.append(keys[i])
        
    for i in features:
        if '' in i:
            rem_list.append(features.index(i)) #Deal with nulls later
    
    features =[ features[i] for i in range(len(features)) if i not in rem_list ]
    features = zip(*features)
    
    for i in range(len(features)):
        features[i] = [x for x in features[i] ]
        identifier.append(features[i].pop(0))
        
    print 'import complete'
    
    
    return features, identifier
    

    
def export_data(results): #BUG Identifiers not coming out right!!
    out_file=open('results.csv', 'a')
    for key, value in results.iteritems():
        out_file.write(str(key)+','+str(value)+' 1'+'\n')
    out_file.close()