columns_config = {
    'qs1':{#age
        'conversion':{
            'values':{
                '_NaN':'_mean'
            },
            # 'log_trans': True
        },
        'continuous': True,
        'available_types':['int','int64','float','float64'],

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
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q2VALUE':{
        'conversion': {
            'values': {
                9998:'_mean',
                9999:'_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q2Q1DIF':{
    #     recalculate
    #     'recalculation':{
    #         'subtraction':('Q2VALUE','Q1VALUE')
    #     },
        # 'conversion':{
        #     'log_trans':True
        # },
        'conversion': {
            'values': {
                '_NaN':'_mean',
                9998:'_mean',
                9999:'_mean'
            },
            # 'abs':True,
            # 'log_trans': True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q3VALUE':{
        'conversion': {
            'values': {
                9998:'_mean',
                9999:'_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q4VALUE':{
        'conversion': {
            'values': {
                9998:'_mean',
                9999:'_mean'
            },
            # 'log_trans': True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q4Q3DIF':{
    #     recalculate
    #     'recalculation':{
    #         'subtraction':('Q4VALUE','Q3VALUE')
    #     },
        # 'conversion':{
        #     'log_trans':True
        # },
        'conversion': {
            'values': {
                '_NaN':'_mean',
                9998:'_mean',
                9999:'_mean'
            },
            #'abs':True,
            # 'log_trans': True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q3Q1DIF':{
        'conversion': {
            # 'values': {
            #     '_Nan':'_mean',
            #     # 9998:'_mean',
            #     # 9999:'_mean'
            # },
            #'abs':True,
            # 'log_trans': True
        },
        'continuous': True,
    },
    'Q4Q2DIF':{
        'conversion': {
            # 'values': {
            #     '_Nan':'_mean',
            #     # 9998:'_mean',
            #     # 9999:'_mean'
            # },
            #'abs':True,
            # 'log_trans': True
        },
        'continuous': True,
    },
    'Q4Q2DIFQ3Q1DIFTOTAL':{
        'conversion': {
            # 'values': {
            #     '_Nan':'_mean',
            #     # 9998:'_mean',
            #     # 9999:'_mean'
            # },
            #'abs':True,
            # 'log_trans': True
        },
        'continuous': True,
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
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q6':{
        'conversion': {
            'values': {
                '_NaN':'_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q6Q5DIF':{
        # 'recalculation': {
        #     'subtraction': ('Q6', 'Q5')
        # },
        'conversion': {
            'values': {
                '_NaN': '_mean',
            },
            #'abs': True,
            # 'log_trans': True
        },
        'continuous': True,
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
            },
            # 'log_trans': True
        },
        'continuous': True,
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
        'continuous': True,
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
        'continuous': True,
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
        'continuous': True,
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
        'continuous': True,
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
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q36':{
        'conversion': {
            'values': {
                98:'_mean',
                99:'_mean',
                '_NaN':'_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
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
            },
            # 'log_trans':True
        },
        'continuous': True,
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
            },
            # 'log_trans':True
        },
        'continuous': True,
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
    'Q36Q38Q40TOTAL':{

    },
    'Q42':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q43A':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q43B':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
            #'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q43C':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q43D':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },

    'Q43E': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },

    'Q43F': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q43G1': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
            # 'log_trans': True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q43G2': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q43G3': {#ok1
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q43TOTAL':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
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
    'q51': {
        'conversion': {
            '_NaN': 94
        },
        'available_values': [1, 2, 3, 4, 5, 96, 98, 99],# i guess there is a mistake in the questionaries. consider removing
        'one_hot_encoding': True
    },
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
        'continuous': True,
        # 'one_hot_encoding': True,
        'available_types':['int','float','float64']
    },
    'SHEEFAMILY': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'SHEESOCIAL': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'SHEEMOOD': {#ok1
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'SHEESEX': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'SHEETOTAL': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            },
            # 'log_trans': True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'NSFDISABLE': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            },
            # 'log_trans': True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'WEIGHT': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'HEIGHT': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            },
            # 'log_trans': True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'BMI': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            },
            # 'log_trans': True
        },
        'continuous': True,
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
        'continuous': True,
        'available_types':['int64','float','float64']
    },
    'IPAQ36': {
        'conversion': {
            'values': {
                '_NaN': '_mean',
                98: '_mean',
                99: '_mean'
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'IPAQ38': {
        'conversion': {
            'values': {
                '_NaN': '_mean',
                98: '_mean',
                99: '_mean'
            },
            # 'log_trans':True

        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'IPAQ40': {
        'conversion': {
            'values': {
                '_NaN': '_mean',
                98: '_mean',
                99: '_mean',
            },
            # 'log_trans':True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'IPAQTOTAL': {
        'conversion': {
            'values': {
                '_NaN': 94,
                98: '_mean',
                99: '_mean'
            },
            # 'log_trans': True
        },
        'continuous': True,
        'available_types':['int','float','float64']
    }
}



