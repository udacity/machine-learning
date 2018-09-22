#
import warnings, os, gc, time
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
import pandas as pd
import numpy as np

# Load dataset
previous = pd.read_csv('./dataset/previous_application.csv')

previous.sort_values(by=['SK_ID_CURR', 'SK_ID_PREV', 'AMT_ANNUITY'], inplace=True)
cat_features = [col for col in previous.columns if previous[col].dtype == 'object']
num_features = [col for col in previous.columns if previous[col].dtype != 'object']
all_features = [col for col in previous.columns]
days_features = [col for col in previous.columns if col.find("DAYS")!= -1]
amout_features = [col for col in previous.columns if col.find("AMT_")!= -1]

# Outliers and anomaly
## AMT_CREDIT AMT_CREDIT==NaN
previous.drop(previous[previous['AMT_CREDIT'].isnull()].index, inplace=True)
previous.reset_index(drop=True, inplace=True)
## AMT_DOWN_PAYMENT < 0
## RATE_DOWN_PAYMENT < 0
previous.loc[previous.AMT_DOWN_PAYMENT < 0, 'AMT_DOWN_PAYMENT'] = 0
previous.loc[previous.RATE_DOWN_PAYMENT < 0, 'RATE_DOWN_PAYMENT'] = 0
## SELLERPLACE_AREA < 0
previous['SELLERPLACE_AREA_ANOMALY'] = 0
anomalous_indices = previous[previous['SELLERPLACE_AREA'] < 0].index
previous.loc[anomalous_indices, 'SELLERPLACE_AREA_ANOMALY'] = 1
previous['SELLERPLACE_AREA'].replace(-1, 0, inplace=True)
## DAYS_
previous['DAYS_FIRST_DRAWING_ANOMALY'] = 0
previous['DAYS_FIRST_DUE_ANOMALY'] = 0
previous['DAYS_LAST_DUE_1ST_VERSION_ANOMALY'] = 0
previous['DAYS_LAST_DUE_ANOMALY'] = 0
previous['DAYS_TERMINATION_ANOMALY'] = 0
anomalous_indices = previous[previous.DAYS_FIRST_DRAWING > 0].index
previous.loc[anomalous_indices, 'DAYS_FIRST_DRAWING_ANOMALY'] = 1
previous['DAYS_FIRST_DRAWING'].replace(365243, 0, inplace=True)
anomalous_indices = previous[previous.DAYS_FIRST_DUE > 0].index
previous.loc[anomalous_indices, 'DAYS_FIRST_DUE_ANOMALY'] = 1
previous['DAYS_FIRST_DUE'].replace(365243, 0, inplace=True)
anomalous_indices = previous[previous.DAYS_LAST_DUE_1ST_VERSION > 0].index
previous.loc[anomalous_indices, 'DAYS_LAST_DUE_1ST_VERSION_ANOMALY'] = 1
previous['DAYS_LAST_DUE_1ST_VERSION'].replace(365243, 0, inplace=True)
anomalous_indices = previous[previous.DAYS_LAST_DUE > 0].index
previous.loc[anomalous_indices, 'DAYS_LAST_DUE_ANOMALY'] = 1
previous['DAYS_LAST_DUE'].replace(365243, 0, inplace=True)
anomalous_indices = previous[previous.DAYS_TERMINATION > 0].index
previous.loc[anomalous_indices, 'DAYS_TERMINATION_ANOMALY'] = 1
previous['DAYS_TERMINATION'].replace(365243, 0, inplace=True)
## XNA/XAP
for cat in cat_features:
    previous[cat].replace('XNA', np.nan, inplace=True)
    previous[cat].replace('XAP', np.nan, inplace=True)

# log transform
previous['log_SELLERPLACE_AREA'] = previous['SELLERPLACE_AREA'].map(lambda x: np.log(x + 1))

# Feature engineering
## diff features engineering
previous['diff_ANNUITY_APPLICATION'] = previous['AMT_ANNUITY'] - previous['AMT_APPLICATION']
previous['diff_ANNUITY_CREDIT'] = previous['AMT_ANNUITY'] - previous['AMT_CREDIT']
previous['diff_APPLICATION_CREDIT'] = previous['AMT_APPLICATION'] - previous['AMT_CREDIT']
previous['diff_PRICE_PAYMENT'] = previous['AMT_GOODS_PRICE'] - previous['AMT_DOWN_PAYMENT']
previous['diff_PRICE_CREDIT'] = previous['AMT_GOODS_PRICE'] - previous['AMT_CREDIT']
previous['diff_CREDIT_DOWN_PAYMENT'] = previous['AMT_CREDIT'] - previous['AMT_DOWN_PAYMENT']
previous['diff_RATE'] = previous['RATE_INTEREST_PRIMARY'] - previous['RATE_INTEREST_PRIVILEGED']
previous['diff_FIRST_DRAWING_DUE'] = previous['DAYS_FIRST_DRAWING'] - previous['DAYS_FIRST_DUE']
previous['diff_FIRST_DRAWING_LAST_DUE'] = previous['DAYS_FIRST_DRAWING'] - previous['DAYS_LAST_DUE_1ST_VERSION']
previous['diff_LAST_DUE'] = previous['DAYS_LAST_DUE_1ST_VERSION'] - previous['DAYS_LAST_DUE']
previous['diff_TERMINATION_DECISION'] = previous['DAYS_TERMINATION'] - previous['DAYS_DECISION']
previous['diff_TERMINATION_LAST_DUE'] = previous['DAYS_TERMINATION'] - previous['DAYS_LAST_DUE']
previous['diff_TERMINATION_LAST_DUE_1ST'] = previous['DAYS_TERMINATION'] - previous['DAYS_LAST_DUE_1ST_VERSION']

diff_features = ['diff_ANNUITY_APPLICATION', 'diff_ANNUITY_CREDIT', 'diff_APPLICATION_CREDIT',\
                'diff_PRICE_PAYMENT', 'diff_PRICE_CREDIT', 'diff_CREDIT_DOWN_PAYMENT', 'diff_RATE',\
                'diff_FIRST_DRAWING_DUE', 'diff_FIRST_DRAWING_LAST_DUE', 'diff_LAST_DUE',\
                'diff_TERMINATION_DECISION', 'diff_TERMINATION_LAST_DUE', 'diff_TERMINATION_LAST_DUE_1ST']
features_diff = previous.groupby(['SK_ID_CURR'])[diff_features].agg({'max', 'min', 'mean'}).reset_index()
features_diff.columns = pd.Index(['SK_ID_CURR']+["PREVIOUS_" + e[0] + "_" + e[1] for e in features_diff.columns.tolist()[1:]])

## ratio features engineering
previous['ratio_APPLICATION_ANNUITY'] = previous['AMT_APPLICATION'] / (1 + previous['AMT_ANNUITY'])
previous['ratio_CREDIT_APPLICATION'] = previous['AMT_CREDIT'] / (1 + previous['AMT_APPLICATION'])
previous['ratio_CREDIT_ANNUITY'] = previous['AMT_CREDIT'] / (1 + previous['AMT_ANNUITY'])
previous['ratio_DOWN_PAYMENT_PRICE'] = previous['AMT_DOWN_PAYMENT'] / (1 + previous['AMT_GOODS_PRICE'])
previous['ratio_PRICE_ANNUITY'] = previous['AMT_GOODS_PRICE'] / (1 + previous['AMT_ANNUITY'])
previous['ratio_DOWN_PAYMENT_ANNUITY'] = previous['AMT_DOWN_PAYMENT'] / (1 + previous['AMT_ANNUITY'])
previous['ratio_RATE'] = previous['RATE_INTEREST_PRIMARY'] / (1 + previous['RATE_INTEREST_PRIVILEGED'])
previous['ratio_DOWN_PAYMENT_RATE'] = previous['RATE_DOWN_PAYMENT'] / (1 + previous['AMT_DOWN_PAYMENT'])
previous['ratio_AMT_CREDIT_CNT'] = previous['AMT_CREDIT'] / (1 + previous['CNT_PAYMENT'])
previous['ratio_APPLICATION_log_AREA'] = previous['AMT_APPLICATION'] / (1 + previous['log_SELLERPLACE_AREA'])

ratio_features = ['ratio_APPLICATION_ANNUITY', 'ratio_CREDIT_APPLICATION', 'ratio_CREDIT_ANNUITY',\
                 'ratio_DOWN_PAYMENT_PRICE', 'ratio_PRICE_ANNUITY', 'ratio_DOWN_PAYMENT_ANNUITY',\
                 'ratio_RATE', 'ratio_DOWN_PAYMENT_RATE', 'ratio_AMT_CREDIT_CNT', 'ratio_APPLICATION_log_AREA']
features_ratio = previous.groupby(['SK_ID_CURR'])[ratio_features].agg({'max', 'min', 'mean', 'std'}).reset_index()
features_ratio.columns = pd.Index(['SK_ID_CURR'] +\
                                  ["PREVIOUS_" + e[0] + "_" + e[1] for e in features_ratio.columns.tolist()[1:]])

## multiply features engineering
previous['RATE_INTEREST_PRIMARY'].fillna(1.0, inplace=True)
previous['RATE_INTEREST_PRIVILEGED'].fillna(1.0, inplace=True)
previous['RATE_DOWN_PAYMENT'].fillna(0.0, inplace=True)
previous['AMT_ANNUITY'].fillna(0.0, inplace=True)
previous['AMT_DOWN_PAYMENT'].fillna(0.0, inplace=True)

previous['multiply_ANNUITY_RATE_PRIMARY'] = previous['AMT_ANNUITY'] * previous['RATE_INTEREST_PRIMARY']
previous['multiply_ANNUITY_RATE_PRIVILEGED'] = previous['AMT_ANNUITY'] * previous['RATE_INTEREST_PRIVILEGED']
previous['multiply_DOWN_PAYMENT_RATE'] = previous['AMT_DOWN_PAYMENT'] * previous['RATE_DOWN_PAYMENT']

features_multiply = previous.groupby(['SK_ID_CURR'])\
['multiply_ANNUITY_RATE_PRIMARY', 'multiply_ANNUITY_RATE_PRIVILEGED', 'multiply_DOWN_PAYMENT_RATE'].\
agg({'max', 'min', 'mean', 'std'}).reset_index()
features_multiply.columns = pd.Index(['SK_ID_CURR'] +\
                                  ["PREVIOUS_" + e[0] + "_" + e[1] for e in features_multiply.columns.tolist()[1:]])

# num_avg features engineering
previous['YEARS_LAST_DUE_1ST_VERSION'] = previous['DAYS_LAST_DUE_1ST_VERSION']/365
previous['YEARS_DECISION'] = previous['DAYS_DECISION']/365

num_avg_features = ['AMT_ANNUITY', 'YEARS_LAST_DUE_1ST_VERSION', 'AMT_DOWN_PAYMENT',\
                   'HOUR_APPR_PROCESS_START', 'YEARS_DECISION', 'log_SELLERPLACE_AREA']

features_avg = previous.groupby(['SK_ID_CURR'])[num_avg_features].agg({'mean'}).reset_index()
features_avg.columns = pd.Index(['SK_ID_CURR']+["PREVIOUS_" + e[0] + "_" + e[1] for e in features_avg.columns.tolist()[1:]])

features_previous = features_diff.merge(features_ratio)
features_previous = features_previous.merge(features_multiply)
features_previous = features_previous.merge(features_avg)

features_previous.to_csv('features_previous_final.csv', index=False)

