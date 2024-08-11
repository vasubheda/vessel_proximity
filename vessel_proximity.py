import pandas as pd
import numpy as np
import seaborn as sns
import math

#Loading the Dataset
df=pd.read_csv("sample_data.csv") 

# Creating an empty column
df["proximity_index"]=""

## Making the function of haversine formula
def haversine(lat1, lon1, lat2, lon2):
     
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c


# Sorting the mmsi vessel rows with no interactions and defining the values of proximity index according to it
rough=[]
for i in range(len(df['timestamp'])):
    index=df[(df['timestamp'] == df['timestamp'][i])].index.tolist()
    if len(index)==1:
        index="No Interactions"
    else:
        index=""
    rough.append(index)
df["proximity_index"]=rough


# Dropping the unnecessay rows which have no interactions
index = df[(df['proximity_index'] == 'No Interactions')].index.tolist()
df.drop(index,inplace=True)
df.reset_index(drop=True, inplace=True)


# Using the same functionality to gather the vessel information which has the same timestamps
same_timestamp=[]
for i in range(len(df['timestamp'])):
    index_list = df[(df['timestamp'] == df['timestamp'][i])].index.tolist()
    index_list.pop(0)
    same_timestamp.append(index_list)   
df["proximity_index"]=same_timestamp

df.reset_index(drop=True, inplace=True) ## reseting the index to avoid any irregularities

#Removing all the mmsi numbers which has same timestamps but does not interact with each other
for i in range(len(df["proximity_index"])):
    for mmsi in df["proximity_index"][i]:
        lat1=df["lat"][i]
        lon1=df["lon"][i]
        lat2=df["lat"][mmsi]
        lon2=df["lon"][mmsi]
        dist=haversine(lat1, lon1, lat2, lon2)
        if dist>=0.1:
            df["proximity_index"][i].remove(mmsi)
### Note: We have used the threshold distance value as 100 meters/ 0.1 K.M.

## Replacing the index values with the actual mmsi values
for i in df["proximity_index"]:
    list=i
    for j in range(len(list)):
        list[j]=df["mmsi"][list[j]]
        
# Renaming the column as vessel_proximity and dropping the lat and lon columns
df.rename(columns={'proximity_index':'vessel_proximity'},inplace=True)
df.drop(df[["lat","lon"]],axis=1,inplace=True)

# Properly ordering the columns
column_titles=["mmsi","vessel_proximity","timestamp"]
df=df.reindex(columns=column_titles)

# saving the final result as a csv file
df.to_csv("results.csv",header=True,index=False)