columns_config = {
    'qs1':{
        'conversion':{
            'values':{
                '_NaN':'_mean'
            },
         },
        'continuous': True,
    },
    'qs2':{
        'conversion': {
            'values':{
                '_NaN':94
            }
        },
        'one_hot_encoding': True,
    },
    'qs3':{
        'conversion': {
            'values':{
                '_NaN':94
            }
        },
        'one_hot_encoding': True,
    },
    'NORTHEAST':{
        'conversion': {
            'values':{
                '_NaN':0
            }
        },
    },
    'MIDWEST':{
        'conversion': {
            'values': {
                '_NaN':0
            }
        },
    },
    'SOUTH':{
        'conversion': {
            'values': {
                '_NaN':0
            }
        },
    },
    'WEST':{
        'conversion': {
            'values': {
                '_NaN':0
            }
        },
    },
    'Q1VALUE':{
        'conversion': {
            'values': {
                9998:'_mean',
                9999:'_mean'
            },
        },
        'continuous': True,
    },
    'Q2VALUE':{
        'conversion': {
            'values': {
                9998:'_mean',
                9999:'_mean'
            },
        },
        'continuous': True,
    },
    'Q2Q1DIF':{
        'conversion': {
            'values': {
                '_NaN':'_mean',
                9998:'_mean',
                9999:'_mean'
            },
        },
        'continuous': True
    },
    'Q3VALUE':{
        'conversion': {
            'values': {
                9998:'_mean',
                9999:'_mean'
            },
        },
        'continuous': True,
    },
    'Q4VALUE':{
        'conversion': {
            'values': {
                9998:'_mean',
                9999:'_mean'
            },
        },
        'continuous': True,
    },
    'Q4Q3DIF':{
        'conversion': {
            'values': {
                '_NaN':'_mean',
                9998:'_mean',
                9999:'_mean'
            },
        },
        'continuous': True,
        'available_types':['int','float','float64']
    },
    'Q3Q1DIF':{
        'conversion': {
        },
        'continuous': True,
    },
    'Q4Q2DIF':{
        'conversion': {
        },
        'continuous': True,
    },
    'Q4Q2DIFQ3Q1DIFTOTAL':{
        'conversion': {
        },
        'continuous': True,
    },
    'Q5':{
        'conversion': {
            'values': {
                '_NaN':'_mean'
            },
        },
        'continuous': True,
    },
    'Q6':{
        'conversion': {
            'values': {
                '_NaN':'_mean'
            },
        },
        'continuous': True
    },
    'Q6Q5DIF':{
        'conversion': {
            'values': {
                '_NaN': '_mean',
            },
        },
        'continuous': True
    },
    'q7':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True,
    },
    'q8':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True,
    },
    'q9':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True,
    },
    'q10':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q11':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q12':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q13a':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q13b':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q13c':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q13d':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q13e':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q13f':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q13g':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'EPWORTH':{
        'conversion': {
            'values': {
                '_NaN':'_mean'
            },
        },
        'continuous': True,
    },
    'q14':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q15':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q16a':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q16c':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q16d':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q16e':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q16f':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q17':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q18':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q19a':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q19b':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q19c':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q19d':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q20':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q21':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q22':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q23':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q24':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q25':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q26':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q27':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q28':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
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
    },
    'Q29TOTAL':{
        'conversion': {
            'values': {
                98:'_mean',
                99:'_mean'
            }
        },
        'continuous': True,
    },
    'q30':{
        'conversion': {
            'values': {
                1:4,
                2:3,
                3:2,
                4:1
            }
        },
        'is_target_variable': True
    },
    'q31':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q32':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q33':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q34':{
        'conversion': {
            'values': {
                '_NaN':94
            }
        },
        'one_hot_encoding': True
    },
    'q35':{
        'conversion': {
            'values': {
                '_NaN':'_mean',
                996:'_mean',
                998:'_mean',
                999:'_mean'
            },
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
        },
        'continuous': True,
    },
    'q3701':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q3702':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q3703':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },

    'Q38':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },

    'q3901': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q3902': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q3903': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'Q40':{
        'conversion': {
            'values': {
                98:'_mean',
                99:'_mean',
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },
    'q4101':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q4102':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q4103':{
        'conversion': {
            'values': {
                '_NaN':94
            },
            'astype': 'int64'
        },
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
        },
        'continuous': True,
    },
    'Q43A':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },
    'Q43B':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },
    'Q43C':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },
    'Q43D':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },

    'Q43E': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },

    'Q43F': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },
    'Q43G1': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
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
        },
        'continuous': True,
    },
    'Q43G3': {
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },
    'Q43TOTAL':{
        'conversion': {
            'values': {
                98: '_mean',
                99: '_mean',
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },
    'q4401': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q4402': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q4403': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q45': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'one_hot_encoding': True
    },
    'q46': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'one_hot_encoding': True
    },
    'q47': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'one_hot_encoding': True
    },
    'q48': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'one_hot_encoding': True
    },
    'q49': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'one_hot_encoding': True
    },
    'q50': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'one_hot_encoding': True
    },
    'q51': {
        'conversion': {
            '_NaN': 94
        },
        'one_hot_encoding': True
    },
    'q53': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'one_hot_encoding': True
    },
    'q54': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'one_hot_encoding': True
    },
    'q55': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
        'one_hot_encoding': True
    },
    'q56': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
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
        'one_hot_encoding': True
    },
    'q5702': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q5703': {
        'conversion': {
            'values': {
                '_NaN': 94
            },
            'astype': 'int64'
        },
        'one_hot_encoding': True
    },
    'q5704': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
    },
    'q58': {
        'conversion': {
            'values': {
                '_NaN': 94
            }
        },
    },
    'SHEEWORK': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
    },
    'SHEEFAMILY': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
    },
    'SHEESOCIAL': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
    },
    'SHEEMOOD': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
    },
    'SHEESEX': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
    },
    'SHEETOTAL': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },
    'NSFDISABLE': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },
    'WEIGHT': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
    },
    'HEIGHT': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },
    'BMI': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            },
        },
        'continuous': True,
    },
    'STOPBAG1': {
        'conversion': {
            'values': {
                '_NaN': 0
            }
        },
    },
    'STOPBAG2': {
        'conversion': {
            'values': {
                '_NaN': '_mean'
            }
        },
        'continuous': True,
    },
    'IPAQ36': {
        'conversion': {
            'values': {
                '_NaN': '_mean',
                98: '_mean',
                99: '_mean'
            },
        },
        'continuous': True,
    },
    'IPAQ38': {
        'conversion': {
            'values': {
                '_NaN': '_mean',
                98: '_mean',
                99: '_mean'
            },

        },
        'continuous': True,
    },
    'IPAQ40': {
        'conversion': {
            'values': {
                '_NaN': '_mean',
                98: '_mean',
                99: '_mean',
            },
        },
        'continuous': True,
    },
    'IPAQTOTAL': {
        'conversion': {
            'values': {
                '_NaN': 94,
                98: '_mean',
                99: '_mean'
            },
        },
        'continuous': True,
    }
}



