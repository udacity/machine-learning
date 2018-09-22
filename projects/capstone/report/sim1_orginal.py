#
import warnings, time, gc
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, Imputer
from sklearn.linear_model import LogisticRegression
start = time.time()
RANDOM = 47

application_train_ = pd.read_csv('./dataset/application_train.csv')
application_test_ = pd.read_csv('./dataset/application_test.csv')
train_size_ = application_train_.shape[0]
application = pd.concat((application_train_, application_test_)).reset_index(drop=True)

# one-hot encoding
application = pd.get_dummies(application, dummy_na=True)

data = application[:train_size_].copy()
test = application[train_size_:].copy()
test.drop(columns = ['TARGET'], inplace=True)

y_train = data['TARGET'].copy()
X_train = data.drop(columns = ['SK_ID_CURR', 'TARGET'])
submission = test[['SK_ID_CURR']].copy()
X_test = test.drop(columns = ['SK_ID_CURR'])

# missing values
imputer = Imputer(strategy='median').fit(X_train)
X_train = imputer.transform(X_train)
X_test = imputer.transform(X_test)

del data, test, application_train_, application_test_
gc.collect()

print('X_train size: {}\nX_test size: {}'.format(X_train.shape, X_test.shape))

# train and predict
clf = LogisticRegression().fit(X_train, y_train)
y_pred = clf.predict_proba(X_test)[:, 1]

# submit
submission['TARGET'] = y_pred
print(submission.head())
submission.to_csv('csv_sim1_orginal.csv', index = False)
print('Run time: {:.2f}mins'.format((time.time() - start)/60))
