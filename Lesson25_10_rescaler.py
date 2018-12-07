""" quiz materials for feature scaling clustering """
from __future__ import division
### FYI, the most straightforward implementation might 
### throw a divide-by-zero error, if the min and max
### values are the same
### but think about this for a second--that means that every
### data point has the same value for that feature!  
### why would you rescale it?  Or even use it at all?
def featureScaling(arr):
    a = []
    if min(arr) == max(arr):
        return arr
    else:    
        return [ (x - min(arr))/(max(arr) - min(arr)) for x in arr ]

# tests of your feature scaler--line below is input data
data = [115, 140, 175]
print(featureScaling(data))