#
import warnings, time
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
import numpy as np
import pandas as pd
start = time.time()
RANDOM = 47

application_train_ = pd.read_csv('./application_train_final.csv')
application_test_ = pd.read_csv('./application_test_final.csv')
train_size_ = application_train_.shape[0]
application = pd.concat((application_train_, application_test_)).reset_index(drop=True)

features_bureau = pd.read_csv('features_BUREAU_final.csv')
application = application.merge(features_bureau, on='SK_ID_CURR',how='left')

features_previous = pd.read_csv('features_previous_final.csv')
features_previous_CURR = features_previous.groupby(['SK_ID_CURR']).agg({'max', 'min'}).reset_index()
features_previous_CURR.columns = pd.Index(['SK_ID_CURR'] + [e[0] + "_" + e[1] for e in features_previous_CURR.columns.tolist()[1:]])
application = application.merge(features_previous_CURR, on='SK_ID_CURR',how='left')

features_POS = pd.read_csv('features_POS_final.csv')
features_POS_CURR = features_POS.drop(columns = ['SK_ID_PREV'])
features_POS_CURR = features_POS_CURR.groupby(['SK_ID_CURR']).agg({'max', 'min'}).reset_index()
features_POS_CURR.columns = pd.Index(['SK_ID_CURR'] + [e[0] + "_" + e[1] for e in features_POS_CURR.columns.tolist()[1:]])
application = application.merge(features_POS_CURR, on='SK_ID_CURR',how='left')

features_install = pd.read_csv('features_install_final.csv')
features_install_CURR = features_install.drop(columns = ['SK_ID_PREV'])
features_install_CURR = features_install_CURR.groupby(['SK_ID_CURR']).agg({'max', 'min'}).reset_index()
features_install_CURR.columns = pd.Index(['SK_ID_CURR'] + [e[0] + "_" + e[1] for e in features_install_CURR.columns.tolist()[1:]])
application = application.merge(features_install_CURR, on='SK_ID_CURR',how='left')

features_credit = pd.read_csv('features_credit_final.csv')
features_credit_CURR = features_credit.drop(columns = ['SK_ID_PREV'])
features_credit_CURR = features_credit_CURR.groupby(['SK_ID_CURR']).agg({'max', 'min'}).reset_index()
features_credit_CURR.columns = pd.Index(['SK_ID_CURR'] + [e[0] + "_" + e[1] for e in features_credit_CURR.columns.tolist()[1:]])
application = application.merge(features_credit_CURR, on='SK_ID_CURR',how='left')

data = application[:train_size_].copy()
test = application[train_size_:].copy()
test.drop(columns = ['TARGET'], inplace=True)

data.to_csv('data_fe.csv', index = False)
test.to_csv('test_fe.csv', index = False)
print('Run time: {:.2f}mins'.format((time.time() - start)/60))
