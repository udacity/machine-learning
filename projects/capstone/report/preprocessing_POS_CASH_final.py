#
import warnings, os, gc, time
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
import pandas as pd
import numpy as np

# Load dataset
pos_cash = pd.read_csv('dataset/POS_CASH_balance.csv')

# my Aggregation
pos_cash['DPD_diff'] = pos_cash['SK_DPD'] - pos_cash['SK_DPD_DEF']
pos_cash['CNT_diff'] = pos_cash['CNT_INSTALMENT'] - pos_cash['CNT_INSTALMENT_FUTURE']

features_time = pos_cash.groupby(['SK_ID_CURR', 'SK_ID_PREV'])['MONTHS_BALANCE'].agg({'max', 'min', 'mean', 'size'}).reset_index().\
rename(columns={'max': 'month_bal_max', 'min': 'month_bal_min', 'mean': 'month_bal_mean', 'size': 'Duration'})

features_DPD = pos_cash.groupby(['SK_ID_CURR', 'SK_ID_PREV'])['SK_DPD', 'SK_DPD_DEF'].agg({'max', 'min', 'mean'}).reset_index()
features_DPD.columns = pd.Index(['SK_ID_CURR', 'SK_ID_PREV']+[e[0] + "_" + e[1] for e in features_DPD.columns.tolist()[2:]])

features_diff = pos_cash.groupby(['SK_ID_CURR', 'SK_ID_PREV'])['DPD_diff', 'CNT_diff'].agg({'max', 'min', 'mean'}).reset_index()
features_diff.columns = pd.Index(['SK_ID_CURR', 'SK_ID_PREV']+[e[0] + "_" + e[1] for e in features_diff.columns.tolist()[2:]])

features_CNT = pos_cash.groupby(['SK_ID_CURR', 'SK_ID_PREV'])['CNT_INSTALMENT', 'CNT_INSTALMENT_FUTURE'].agg({'max', 'min', 'mean'}).reset_index()
features_CNT.columns = pd.Index(['SK_ID_CURR', 'SK_ID_PREV']+[e[0] + "_" + e[1] for e in features_CNT.columns.tolist()[2:]])

features_POS = features_time.merge(features_DPD)
features_POS = features_POS.merge(features_diff)
features_POS = features_POS.merge(features_CNT)

features_POS.to_csv('features_POS_final.csv', index=False)
