#
import warnings, os, gc, time
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
import pandas as pd
import numpy as np

# Load dataset
install = pd.read_csv('dataset/installments_payments.csv')

#
install['diff_early_pay'] = install['DAYS_INSTALMENT'] - install['DAYS_ENTRY_PAYMENT']
install['diff_AMT_pay'] = install['AMT_INSTALMENT'] - install['AMT_PAYMENT']

install['ratio_early_pay'] = install['diff_early_pay'] / (1 + install['DAYS_ENTRY_PAYMENT'])
install['ratio_AMT_pay'] = install['diff_AMT_pay'] / (1 + install['AMT_INSTALMENT'])

features_diff = install.groupby(['SK_ID_CURR', 'SK_ID_PREV'])['diff_early_pay', 'diff_AMT_pay'].agg({'max', 'min', 'mean'}).reset_index()
features_diff.columns = pd.Index(['SK_ID_CURR', 'SK_ID_PREV']+["INSTALL_" + e[0] + "_" + e[1] for e in features_diff.columns.tolist()[2:]])

features_ratio = install.groupby(['SK_ID_CURR', 'SK_ID_PREV'])['ratio_early_pay', 'ratio_AMT_pay'].\
agg({'max', 'min', 'mean', 'std'}).reset_index()
features_ratio.columns = pd.Index(['SK_ID_CURR', 'SK_ID_PREV'] +\
                                  ["INSTALL_" + e[0] + "_" + e[1] for e in features_ratio.columns.tolist()[2:]])

#
features_install = features_diff.merge(features_ratio)
features_install.to_csv('features_install_final.csv', index=False)
