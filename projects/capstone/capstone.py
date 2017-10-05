import numpy as np
import pandas as pd
from time import time
from IPython.display import display


# import visuals as vs # I think I cat get it from udacity

all_data = pd.read_csv("hw-spr2007-anon-demographics-1.csv")
# print df.loc[[1]]
# print len(df)
refined_data = all_data[:-(len(all_data) - 76)]
print refined_data
# df.drop(df.index[97:126])
# print df.count
# print df[:-29]



# print data