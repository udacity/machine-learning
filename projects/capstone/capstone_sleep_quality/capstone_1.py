import numpy as np
import pandas as pd
from time import time
from sklearn.model_selection import KFold
import sys
# from sklearn.metrics import r2_score
from sklearn.metrics import fbeta_score, accuracy_score
import math

#import files
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier

import pre_process


all_data = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")

# refined_data =  all_data[["qs1","qs2","qs3","NORTHEAST","MIDWEST","SOUTH","WEST","Q1VALUE","Q2VALUE",
#                       "Q2Q1DIF","Q3VALUE","Q4VALUE","Q4Q3DIF","Q4Q3Q2Q1DIFHRS","Q5","Q6","Q6Q5DIF"
#     ,"q7","q8","q9","q10","q11","q12","q13a","q13b","q13c","q13d","q13e","q13f","q13g","EPWORTH",
#                       "q14","q15","q16a","q16c","q16d","q16e","q16f","q17","q18","q19a","q19b",
#                       "q19c","q19d","q20","q21","q22","q23","q24","q25","q26","q27","q28","q29a","q29b","q29c",
#                       "Q29TOTAL","q30","q31","q32","q33","q34","q35","Q36","q3701","q3702","q3703","Q38"
# ,"q3901","q3902","q3903","Q40","q4101","q4102","q4103","Q42","Q43A","Q43B","Q43C","Q43D","Q43E","Q43F","Q43G1"
#     ,"Q43G2","Q43G3","q4401","q4402","q4403","q45","q46","q47","q48","q49","q50","SHEEWORK","SHEEFAMILY","SHEEMOOD"
#     ,"SHEESEX","SHEETOTAL","NSFDISABLE","WEIGHT","HEIGHT","BMI","STOPBAG1","STOPBAG2","IPAQ36","IPAQ38","IPAQ40","IPAQTOTAL"]]

columns_config = {
    'qs1':{#age
        'conversion':{
            'values':{
                '_NaN':'_mean'
            }

        },
        'available_types':['int','int64','float','float64']

    },
    'qs2':{#emplyment_status
        'conversion': {
            'values':{
                '_NaN':94
            }
        },
        'one_hot_encoding': True,
        'available_values':[1,2,3,4,98,99]
    },
    'qs3':{ #gender
        'conversion': {
            'values':{
                '_NaN':94
            }
        },
        'one_hot_encoding': True,
        'available_values':[1,2]
    },
    'NORTHEAST':{#ok1
        'conversion': {
            'values':{
                '_NaN':0
            }
        },
        'available_values':[1]
    },
    'MIDWEST':{
        'conversion': {
            'values': {
                '_NaN':0
            }
        },
        'available_values':[1]
    },
    'SOUTH':{
        'conversion': {
            'values': {
                '_NaN':0
            }
        },
        'available_values':[1]
    },
    'WEST':{
        'conversion': {
            'values': {
                '_NaN':0
            }
        },
        'available_values':[1]
    },
    'Q1VALUE':{
        'conversion': {
            'values': {
                9998:'_mean',
                9999:'_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q2VALUE':{
        'conversion': {
            'values': {
                9998:'_mean',
                9999:'_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q2Q1DIF':{
    #     recalculate
        'recalculation':{
            'subtraction':('Q2VALUE','Q1VALUE')
        },
        'available_types':['int','float','float64']
    },
    'Q3VALUE':{
        'conversion': {
            'values': {
                9998:'_mean',
                9999:'_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q4VALUE':{
        'conversion': {
            'values': {
                9998:'_mean',
                9999:'_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q4Q3DIF':{
    #     recalculate
        'recalculation':{
            'subtraction':('Q4VALUE','Q3VALUE')
        },
        'available_types':['int','float','float64']
    },
    # 'Q4Q3Q2Q1DIFHRS':{
    #     'recalculation': {
    #         'subtraction': ('Q2VALUE', 'Q1VALUE')
    #     }
    # },make a new colum for this
    'Q5':{
        'conversion': {
            'values': {
                '_NaN':'_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q6':{
        'conversion': {
            'values': {
                '_NaN':'_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q6Q5DIF':{
        'recalculation': {
            'subtraction': ('Q6', 'Q5')
        },
        'available_types':['int','float','float64']
    },
    'q7':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True,
        'available_values':[1,2,3,4,5,98,99]
    },
    'q8':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True,
        'available_values':[1,2,3,4,5,98,99]
    },
    'q9':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True,
        'available_values':[1,2,3,4,5,98,99]
    },
    'q10':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True,
        'available_values':[1,2,3,4,5,98,99]
    },
    'q11':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True,
        'available_values':[1,2,3,4,98,99]
    },
    'q12':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True,
        'available_values':[1,2,3,4,98,99]
    },
    'q13a':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values':[0,1,2,3,98,99],
        'one_hot_encoding': True
    },
    'q13b':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [0, 1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q13c':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [0, 1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q13d':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [0, 1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q13e':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [0, 1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q13f':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [0, 1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q13g':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [0, 1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'EPWORTH':{
        'conversion': {
            'values': {
                '_NaN':'_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'q14':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 98, 99],
        'one_hot_encoding': True
    },
    'q15':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 98, 99],
        'one_hot_encoding': True
    },
    'q16a':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q16c':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q16d':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q16e':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q16f':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q17':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 5, 6, 7, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q18':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 5, 6, 7, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q19a':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'one_hot_encoding': True
    },
    'q19b':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'one_hot_encoding': True
    },
    'q19c':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'one_hot_encoding': True
    },
    'q19d':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'one_hot_encoding': True
    },
    'q20':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 98, 99],
        'one_hot_encoding': True
    },
    'q21':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 98, 99],
        'one_hot_encoding': True
    },
    'q22':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 98, 99],
        'one_hot_encoding': True
    },
    'q23':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 98, 99],
        'one_hot_encoding': True
    },
    'q24':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'one_hot_encoding': True
    },
    'q25':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'one_hot_encoding': True
    },
    'q26':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 98, 99],
        'one_hot_encoding': True
    },
    'q27':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 4, 5, 98, 99],
        'one_hot_encoding': True
    },
    'q28':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'one_hot_encoding': True
    },
    'q29a':{
        'conversion': {
            'values': {
                '_NaN':'_mean',
                98:'_mean',
                99:'_mean',
                97: 0.5
            },
            'astype': 'int64'
        },
        'available_types':['int64','float','float64'],
        # 'one_hot_encoding': True

    },
    'q29b':{
        'conversion': {
            'values': {
                '_NaN':'_mean',
                98:'_mean',
                99:'_mean',
                97: 0.5
            },
            'astype': 'int64'
        },
        'available_types':['int64','float','float64'],
        # 'one_hot_encoding': True
    },
    'q29c':{
        'conversion': {
            'values': {
                '_NaN':'_mean',
                98:'_mean',
                99:'_mean',
                97: 0.5
            },
            'astype': 'int64'
        },
        'available_types':['int64','float','float64'],
        # 'one_hot_encoding': True
    },
    'Q29TOTAL':{
        'conversion': {
            'values': {
                98:'_mean',
                99:'_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'q30':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'is_target_variable': True
        # 'one_hot_encoding': True
    },
    'q31':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'one_hot_encoding': True
    },
    'q32':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'one_hot_encoding': True
    },
    'q33':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'one_hot_encoding': True
    },
    'q34':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'available_values': [1, 2, 3, 4, 98, 99],
        'one_hot_encoding': True
    },
    'q35':{#ok1
        'conversion': {
            'values': {
                '_NaN':'_mean',
                996:'_mean',
                998:'_mean',
                999:'_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q36':{
        'conversion': {
            'values': {
                98:'_mean',
                99:'_mean',
                '_NaN':'_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'q3701':{#ok1?
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q3702':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q3703':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },

    'Q38':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },

    'q3901': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q3902': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q3903': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'Q40':{
        'conversion': {
            'values': {
                98:'_mean',
                99:'_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'q4101':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q4102':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q4103':{#ok1
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'Q42':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q43A':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q43B':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q43C':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q43D':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },

    'Q43E': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },

    'Q43F': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q43G1': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q43G2': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'Q43G3': {#ok1
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'q4401': {#ok1
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q4402': {#ok1
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q4403': {#ok1
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 98, 99],
        'one_hot_encoding': True
    },
    'q45': {#ok1
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 3, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q46': {#ok1
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 3, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q47': {#ok1
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 3, 4, 5, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q48': {#ok1
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 3, 4, 5, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q49': {#ok1
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 3, 4, 96, 98, 99],
        'one_hot_encoding': True
    },
    'q50': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 3, 4, 5, 96, 98, 99],
        'one_hot_encoding': True
    },
    # 'q51': {
    #     'conversion': {
    #         '_NaN': 94
    #     },
    #     'available_values': [1, 2, 3, 4, 5, 96, 98, 99],# i guess there is a mistake in the questionaries. consider removing
    #     'one_hot_encoding': True
    # },
    'q53': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 3, 4, 5, 6, 98],
        'one_hot_encoding': True
    },
    'q54': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 98],
        'one_hot_encoding': True
    },
    'q55': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 3, 4, 5, 98, 99],
        'one_hot_encoding': True
    },
    'q56': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 98, 99],
        'one_hot_encoding': True
    },
    'q5701': {
        'conversion': {
            'values': {
                '_NaN': 94,
                9 : 94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 4, 5, 6, 7, 8, 95, 98, 99],
        'one_hot_encoding': True
    },
    'q5702': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 4, 5, 6, 7, 8, 95, 98, 99],
        'one_hot_encoding': True
    },
    'q5703': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'available_values': [1, 2, 3, 4, 5, 6, 7, 8, 95, 98, 99],
        'one_hot_encoding': True
    },
    'q5704': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 3, 4, 5, 6, 7, 8, 95, 98, 99]
    },
    'q58': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'available_values': [1, 2, 98, 99],
    },
    'SHEEWORK': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        # 'one_hot_encoding': True,
        'available_types':['int','float','float64']
    },
    'SHEEFAMILY': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'SHEESOCIAL': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'SHEEMOOD': {#ok1
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'SHEESEX': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'SHEETOTAL': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'NSFDISABLE': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'WEIGHT': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'HEIGHT': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'BMI': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'STOPBAG1': {
        'conversion': {
            'values': {
                '_NaN': 0
            }
        },
        'available_values': [1],
    },
    'STOPBAG2': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'available_types':['int64','float','float64']
    },
    'IPAQ36': {
        'conversion': {
            'values': {
                '_NaN': '_mean',
                98: '_mean',
                99: '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'IPAQ38': {
        'conversion': {
            'values': {
                '_NaN': '_mean',
                98: '_mean',
                99: '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'IPAQ40': {
        'conversion': {
            'values': {
                '_NaN': '_mean',
                98: '_mean',
                99: '_mean'
            }
        },
        'available_types':['int','float','float64']
    },
    'IPAQTOTAL': {
        'conversion': {
            'values': {
                '_NaN': 94,
                98: '_mean',
                99: '_mean'
            }
        },
        'available_types':['int','float','float64']
    }




}


#drop target values, set a target value
# features = all_data.drop('q30', axis = 1)
# sleep_quality = all_data['q30']


#make a preprocess object
pre_process_obj = pre_process.PreProcess(all_data,columns_config)

#convert values and extract data
pre_process_obj.convert_values_and_extract_data()

#recalculation of certain columns because some of the columms are consisted of
pre_process_obj.recalculation()

result = pre_process_obj.are_valid_data()
print result
sys.exit()

#get inputs and outputs


pre_process_obj.df, sleep_quality = pre_process_obj.get_inputs_and_outputs()






#apply one hot encoding
pre_process_obj.apply_one_hot_encoding()

#get final features
features_final = pre_process_obj.df


# import GridSearchCV, make_scorer, train_test_split and metrics
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.cross_validation import train_test_split
from sklearn.metrics import fbeta_score, accuracy_score


# Split the 'features' and 'sleep_quality' data into training and testing sets
random_state = 0
test_size = 0.2
X_train, X_test, y_train, y_test = train_test_split(features_final,
                                                    sleep_quality['q30'],
                                                    test_size = test_size,
                                                    random_state = random_state)

# print X_train
# print X_test
# print y_train
# print y_test
# sys.exit()

# made AdaBoost classifier, and find the best parameters
clf = AdaBoostClassifier(random_state = random_state)
parameters = {'n_estimators': [100, 150, 200], 'learning_rate': [0.5,1.5, 2]}
scorer = make_scorer(accuracy_score)
grid_obj = GridSearchCV(clf, parameters, scoring = scorer )
grid_fit = grid_obj.fit(X_train, y_train)


best_clf = grid_fit.best_estimator_
predictions = (clf.fit(X_train, y_train)).predict(X_test)
best_predictions = best_clf.predict(X_test)
print "Unoptimized model\n------"
print "\nOptimized Model\n------"
print "Accuracy score on testing data: {:.4f}".format(accuracy_score(y_test, predictions))
print "Final accuracy score on the testing data: {:.4f}".format(accuracy_score(y_test, best_predictions))



# result = pre_process_obj.are_valid_data()

# print result
# print first_refined_df['q3701'].dtypes
# pre_process_obj.df['q3701'] = pre_process_obj.df['q3701'].astype(int)
# print pre_process_obj.df['q3701']
# print first_refined_df['q3701'].dtypes
# pre_process_obj.apply_one_hot_encoding()
# not_in_actual, not_in_expected = pre_process_obj.validate_one_hot_encoding()
# print not_in_actual
# print not_in_expected
# print list(pre_process_obj.df)
# print len(list(pre_process_obj.df))
# print result
sys.exit()
# pd.set_option("display.max_colwidth", 1000)
#
# pd.set_option("display.max_rows", 1000)
# refined_data.to_csv("check.csv")


sys.exit()

one_hot_encoded_data = pre_process.apply_one_hot_encode(refined_data,columns_info)

pd.set_option("display.max_colwidth", 1000)

pd.set_option("display.max_rows", 1000)
# print one_hot_encoded_data
# one_hot_encoded_data.to_csv("check.csv")
sys.exit()
# print type(refined_data)
# print refined_data


# features =  all_data[["q34","q35"]]
# qualities_of_sleep = all_data["q30"]
# TODO: Train the supervised model on the training set using .fit(X_train, y_train)
random_state = 0


clf = AdaBoostClassifier(random_state = random_state)
X_train, X_test, y_train, y_test = train_test_split(features,
                                                    qualities_of_sleep,
                                                    test_size = 0.2,
                                                    random_state = random_state)

clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
# print predictions
print accuracy_score(y_test,predictions)
# TODO: Extract the feature importances using .feature_importances_
# importances = model.feature_importances_

# Plot
# vs.feature_plot(importances, X_train, y_train)
