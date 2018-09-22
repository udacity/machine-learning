#
import warnings, os, gc, time
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
import pandas as pd
import numpy as np
from math import log
from tqdm import tqdm

# Load dataset
bureau = pd.read_csv('dataset/bureau.csv')
bureau_bal = pd.read_csv('dataset/bureau_balance.csv')
bureau.sort_values(by=['SK_ID_CURR', 'SK_ID_BUREAU', 'DAYS_CREDIT'], inplace=True)
bureau_bal.sort_values(by=['SK_ID_BUREAU', 'MONTHS_BALANCE'], inplace=True)

cat_features = [col for col in bureau.columns if bureau[col].dtype == 'object']
num_features = [col for col in bureau.columns if bureau[col].dtype != 'object']
days_features = [col for col in bureau.columns if col.find("DAY")!= -1]
amout_features = [col for col in bureau.columns if col.find("AMT_")!= -1]

# bureau_balance Feature engineering
bureau_bal_ = bureau_bal.copy()
bureau_bal_['STATUS'].replace('X', 0, inplace=True)
bureau_bal_['STATUS'].replace('C', 0, inplace=True)
bureau_bal_['STATUS'].replace('0', 0, inplace=True)
bureau_bal_['STATUS'].replace('1', 1, inplace=True)
bureau_bal_['STATUS'].replace('2', 2, inplace=True)
bureau_bal_['STATUS'].replace('3', 3, inplace=True)
bureau_bal_['STATUS'].replace('4', 4, inplace=True)
bureau_bal_['STATUS'].replace('5', 5, inplace=True)
bureau_bal_['MONTHS_BALANCE_abs'] = bureau_bal['MONTHS_BALANCE'].abs() + 1
bureau_bal['STATUS_weight'] = bureau_bal_['STATUS'] / bureau_bal_['MONTHS_BALANCE_abs']

bureau_bal = pd.get_dummies(bureau_bal)
features_months = bureau_bal.groupby(['SK_ID_BUREAU'])['MONTHS_BALANCE'].agg({'max', 'min', 'size'}).reset_index().\
rename(columns={'max': 'BUREAU_BAL_month_bal_max', 'min': 'BUREAU_BAL_month_bal_min', 'size': 'Duration'})

status_features = ['STATUS_0', 'STATUS_1', 'STATUS_2', 'STATUS_3', 'STATUS_4', 'STATUS_5', 'STATUS_C', 'STATUS_X', 'STATUS_weight']
features_status = bureau_bal.groupby(['SK_ID_BUREAU'])[status_features].agg({'sum', 'mean', 'std', pd.DataFrame.kurt}).reset_index()
features_status.columns = pd.Index(['SK_ID_BUREAU']+['BUREAU_BAL_' + e[0] + "_" + e[1] for e in features_status.columns.tolist()[1:]])

# bureau Feature engineering
## Outliers and anomaly
bureau['CREDIT_TYPE'].replace(['Another type of loan', 'Unknown type of loan',\
                               'Loan for working capital replenishment', 'Cash loan (non-earmarked)',\
                               'Real estate loan', 'Loan for the purchase of equipment',\
                               'Loan for purchase of shares (margin lending)', 'Mobile operator loan',\
                               'Interbank credit'], 'Other_loan', inplace=True)

bureau.loc[bureau.DAYS_CREDIT_ENDDATE < -50*365, 'DAYS_CREDIT_ENDDATE'] = np.nan
bureau.loc[bureau.DAYS_ENDDATE_FACT < -50*365, 'DAYS_ENDDATE_FACT'] = np.nan
bureau.loc[bureau.AMT_CREDIT_MAX_OVERDUE > 10000000, 'AMT_CREDIT_MAX_OVERDUE'] = np.nan
bureau.loc[bureau.AMT_CREDIT_SUM > 100000000, 'AMT_CREDIT_SUM'] = np.nan
bureau.loc[bureau.AMT_CREDIT_SUM_DEBT < 0 , 'AMT_CREDIT_SUM_DEBT'] = np.nan
bureau.loc[bureau.AMT_CREDIT_SUM_DEBT > 100000000, 'AMT_CREDIT_SUM_DEBT'] = np.nan
bureau.loc[bureau.AMT_ANNUITY > 10000000 , 'AMT_ANNUITY'] = np.nan

## merge bureau balance by SK_ID_BUREAU
bureau = bureau.merge(features_months, how='outer', on='SK_ID_BUREAU')
bureau = bureau.merge(features_status, how='outer', on='SK_ID_BUREAU')

###################################################################################
## Label encoding
bureau['CREDIT_TYPE'].replace('Consumer credit', 0, inplace=True)
bureau['CREDIT_TYPE'].replace('Credit card', 1, inplace=True)
bureau['CREDIT_TYPE'].replace('Car loan', 2, inplace=True)
bureau['CREDIT_TYPE'].replace('Mortgage', 3, inplace=True)
bureau['CREDIT_TYPE'].replace('Microloan', 4, inplace=True)
bureau['CREDIT_TYPE'].replace('Other_loan', 5, inplace=True)
bureau['CREDIT_TYPE'].replace('Loan for business development', 6, inplace=True)

bureau['CREDIT_CURRENCY'].replace('currency 1', 0, inplace=True)
bureau['CREDIT_CURRENCY'].replace('currency 2', 1, inplace=True)
bureau['CREDIT_CURRENCY'].replace('currency 3', 2, inplace=True)
bureau['CREDIT_CURRENCY'].replace('currency 4', 3, inplace=True)

bureau['CREDIT_ACTIVE'].replace('Closed', 0, inplace=True)
bureau['CREDIT_ACTIVE'].replace('Active', 1, inplace=True)
bureau['CREDIT_ACTIVE'].replace('Sold', 2, inplace=True)
bureau['CREDIT_ACTIVE'].replace('Bad debt', 3, inplace=True)

## diff features engineering
bureau['diff_DAYS_CREDIT'] = bureau['DAYS_CREDIT_UPDATE'] - bureau['DAYS_CREDIT']
bureau['diff_ENDDATE'] = bureau['DAYS_CREDIT_ENDDATE'] - bureau['DAYS_ENDDATE_FACT']
bureau['diff_OVERDUE_UPDATE'] = bureau['DAYS_CREDIT_UPDATE'] - bureau['CREDIT_DAY_OVERDUE']
bureau['diff_CREDIT_DEBT'] = bureau['AMT_CREDIT_SUM'] - bureau['AMT_CREDIT_SUM_DEBT']
bureau['diff_ANNUITY_OVERDUE'] = bureau['AMT_ANNUITY'] - bureau['AMT_CREDIT_SUM_OVERDUE']
bureau['diff_ANNUITY_MAX_OVERDUE'] = bureau['AMT_ANNUITY'] - bureau['AMT_CREDIT_MAX_OVERDUE']
bureau['diff_ANNUITY_CREDIT_SUM'] = bureau['AMT_ANNUITY'] - bureau['AMT_CREDIT_SUM']
bureau['diff_ANNUITY_CREDIT_SUM_DEBT'] = bureau['AMT_ANNUITY'] - bureau['AMT_CREDIT_SUM_DEBT']

diff_features = ['diff_DAYS_CREDIT', 'diff_ENDDATE', 'diff_OVERDUE_UPDATE', 'diff_CREDIT_DEBT',\
                 'diff_ANNUITY_OVERDUE', 'diff_ANNUITY_MAX_OVERDUE', 'diff_ANNUITY_CREDIT_SUM',\
                 'diff_ANNUITY_CREDIT_SUM_DEBT']

features_diff = bureau.groupby(['SK_ID_CURR'])[diff_features].agg({'max', 'min', 'mean', 'median'}).reset_index()
features_diff.columns = pd.Index(['SK_ID_CURR']+["BUREAU_" + e[0] + "_" + e[1] for e in features_diff.columns.tolist()[1:]])

## ratio/multiply features engineering
bureau['ratio_CREDIT_OVERDUE'] = bureau['DAYS_CREDIT'] /(1 + bureau['CREDIT_DAY_OVERDUE'])
bureau['ratio_OVERDUE'] = bureau['AMT_CREDIT_SUM_OVERDUE'] /(1 + bureau['AMT_CREDIT_MAX_OVERDUE'])
bureau['ratio_OVERDUE_DEBT'] = bureau['AMT_CREDIT_SUM_OVERDUE'] /(1 + bureau['AMT_CREDIT_SUM_DEBT'])
bureau['ratio_OVERDUE_ANNUITY'] = bureau['AMT_CREDIT_SUM_OVERDUE'] /(1 + bureau['AMT_ANNUITY'])
bureau['ratio_OVERDUE_CREDIT'] = bureau['AMT_CREDIT_SUM_OVERDUE'] /(1 + bureau['AMT_CREDIT_SUM'])
bureau['ratio_CREDIT_LIMIT_ANNUITY'] = bureau['AMT_CREDIT_SUM_LIMIT'] /(1 + bureau['AMT_ANNUITY'])
bureau['ratio_DEBT'] = bureau['AMT_CREDIT_SUM_DEBT'] /(1 + bureau['AMT_CREDIT_SUM'])
bureau['ratio_DEBT_LIMIT'] = bureau['AMT_CREDIT_SUM_DEBT'] /(1 + bureau['AMT_CREDIT_SUM_LIMIT'])
bureau['ratio_LIMIT_SUM'] = bureau['AMT_CREDIT_SUM_LIMIT'] /(1 + bureau['AMT_CREDIT_SUM'])

bureau['multiply_OVERDUE'] = bureau['CREDIT_DAY_OVERDUE'] * bureau['AMT_CREDIT_MAX_OVERDUE']
bureau['multiply_PROLONG_OVERDUE'] = bureau['CNT_CREDIT_PROLONG'] * bureau['AMT_CREDIT_MAX_OVERDUE']

ratio_features = ['ratio_CREDIT_OVERDUE', 'ratio_OVERDUE', 'ratio_OVERDUE_DEBT', 'ratio_OVERDUE_ANNUITY',\
                  'ratio_OVERDUE_CREDIT', 'ratio_CREDIT_LIMIT_ANNUITY', 'ratio_DEBT', 'ratio_DEBT_LIMIT',\
                  'ratio_LIMIT_SUM']
multiply_features = ['multiply_OVERDUE', 'multiply_PROLONG_OVERDUE']

features_ratio = bureau.groupby(['SK_ID_CURR'])[ratio_features + multiply_features].agg({'max', 'var'}).reset_index()
features_ratio.columns = pd.Index(['SK_ID_CURR'] + ['BUREAU_' + e[0] + "_" + e[1] for e in features_ratio.columns.tolist()[1:]])

## Other numerical features
bureau_ = bureau.drop(columns = diff_features + ratio_features + multiply_features + ['SK_ID_BUREAU'])
features_numerical = bureau_.groupby(['SK_ID_CURR']).agg({'max', 'mean'}).reset_index()
features_numerical.columns = pd.Index(['SK_ID_CURR'] + ['BUREAU_numerical_' + e[0] + "_" + e[1] for e in features_numerical.columns.tolist()[1:]])
features_BUREAU = features_diff.merge(features_ratio, on='SK_ID_CURR',how='left')
features_BUREAU = features_BUREAU.merge(features_numerical, on='SK_ID_CURR',how='left')
features_BUREAU.to_csv('features_BUREAU_final.csv', index=False)
