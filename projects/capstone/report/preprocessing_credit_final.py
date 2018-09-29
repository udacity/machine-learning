#
import warnings, os, gc, time
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
import pandas as pd
import numpy as np

# Load dataset
credit = pd.read_csv('dataset/credit_card_balance.csv')

# Anomaly and outliers
credit.fillna(0, inplace=True)
credit['AMT_DRAWINGS_ATM_CURRENT'].replace(-6827.31, 0, inplace=True)
credit['AMT_DRAWINGS_CURRENT'].replace(-519.57, 0, inplace=True)
credit['AMT_DRAWINGS_CURRENT'].replace(-1687.50, 0, inplace=True)
credit['AMT_DRAWINGS_CURRENT'].replace(-6211.62, 0, inplace=True)

# Drawings features engineering
credit['AMT_CNT_ratio_ATM_CURRENT'] = credit['AMT_DRAWINGS_ATM_CURRENT'] / (1 + credit['CNT_DRAWINGS_ATM_CURRENT'])
credit['AMT_CNT_ratio_CURRENT'] = credit['AMT_DRAWINGS_CURRENT'] / (1 + credit['CNT_DRAWINGS_CURRENT'])
credit['AMT_CNT_ratio_OTHER_CURRENT'] = credit['AMT_DRAWINGS_OTHER_CURRENT'] / (1 + credit['CNT_DRAWINGS_OTHER_CURRENT'])
credit['AMT_CNT_ratio_POS_CURRENT'] = credit['AMT_DRAWINGS_POS_CURRENT'] / (1 + credit['CNT_DRAWINGS_POS_CURRENT'])

features_drawings = credit.groupby(['SK_ID_CURR', 'SK_ID_PREV'])\
['AMT_DRAWINGS_ATM_CURRENT', 'CNT_DRAWINGS_ATM_CURRENT', 'AMT_DRAWINGS_CURRENT', 'CNT_DRAWINGS_CURRENT',\
'AMT_DRAWINGS_OTHER_CURRENT', 'CNT_DRAWINGS_OTHER_CURRENT', 'AMT_DRAWINGS_POS_CURRENT', 'CNT_DRAWINGS_POS_CURRENT',\
'AMT_CNT_ratio_POS_CURRENT', 'AMT_CNT_ratio_ATM_CURRENT', 'AMT_CNT_ratio_CURRENT', 'AMT_CNT_ratio_OTHER_CURRENT'].\
agg({'max', 'min', 'mean', 'std'}).reset_index()
features_drawings.columns = pd.Index(['SK_ID_CURR', 'SK_ID_PREV']+["CREDIT_" + e[0] + "_" + e[1] for e in features_drawings.columns.tolist()[2:]])

# Time-related features engineering
features_time = credit.groupby(['SK_ID_CURR', 'SK_ID_PREV'])['MONTHS_BALANCE'].\
agg({'max', 'min', 'mean', 'size'}).reset_index().\
rename(columns={'max': 'CREDIT_month_bal_max', 'min': 'CREDIT_month_bal_min',
                'mean': 'CREDIT_month_bal_mean', 'size': 'CREDIT_Duration'})

features_DPD = credit.groupby(['SK_ID_CURR', 'SK_ID_PREV'])['SK_DPD', 'SK_DPD_DEF'].\
agg({'max', 'min', 'mean'}).reset_index()
features_DPD.columns = pd.Index(['SK_ID_CURR', 'SK_ID_PREV']+["CREDIT_" + e[0] + "_" + e[1] for e in features_DPD.columns.tolist()[2:]])

# diff features engineering
credit['diff_PAYMENT_REGULARITY'] = credit['AMT_PAYMENT_TOTAL_CURRENT'] - credit['AMT_INST_MIN_REGULARITY']
credit['diff_RECEIVABLE'] = credit['AMT_RECEIVABLE_PRINCIPAL'] - credit['AMT_RECIVABLE']

features_diff = credit.groupby(['SK_ID_CURR', 'SK_ID_PREV'])['diff_PAYMENT_REGULARITY', 'diff_RECEIVABLE'].agg({'max', 'min', 'mean'}).reset_index()
features_diff.columns = pd.Index(['SK_ID_CURR', 'SK_ID_PREV']+["CREDIT_" + e[0] + "_" + e[1] for e in features_diff.columns.tolist()[2:]])

# ratio features engineering
credit['AMT_ratio_PAYMENT_CURRENT'] = credit['AMT_PAYMENT_CURRENT'] / (1 + credit['AMT_PAYMENT_TOTAL_CURRENT'])
credit['AMT_ratio_RECIVABLE'] = credit['AMT_RECIVABLE'] / (1 + credit['AMT_TOTAL_RECEIVABLE'])
credit['ratio_BALANCE_LIMIT'] = credit['MONTHS_BALANCE'] / (1 + credit['AMT_CREDIT_LIMIT_ACTUAL'])

features_ratio = credit.groupby(['SK_ID_CURR', 'SK_ID_PREV'])\
['AMT_ratio_PAYMENT_CURRENT', 'AMT_ratio_RECIVABLE', 'ratio_BALANCE_LIMIT'].agg({'max', 'min', 'mean', 'std'}).reset_index()
features_ratio.columns = pd.Index(['SK_ID_CURR', 'SK_ID_PREV'] + ["CREDIT_" + e[0] + "_" + e[1] for e in features_ratio.columns.tolist()[2:]])

# CUM features engineering
features_CUM = credit.groupby(['SK_ID_CURR', 'SK_ID_PREV'])['CNT_INSTALMENT_MATURE_CUM'].\
agg({'max', 'min', 'mean'}).reset_index().\
rename(columns={'max': 'CREDIT_CNT_INSTALMENT_MATURE_CUM_max', 'min': 'CREDIT_CNT_INSTALMENT_MATURE_CUM_min',
                'mean': 'CREDIT_CNT_INSTALMENT_MATURE_CUM_mean'})

features_credit = features_drawings.merge(features_time)
features_credit = features_credit.merge(features_DPD)
features_credit = features_credit.merge(features_diff)
features_credit = features_credit.merge(features_ratio)
features_credit = features_credit.merge(features_CUM)

features_credit.to_csv('features_credit_final.csv', index=False)
