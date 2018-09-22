#
import warnings, time, gc
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import Imputer
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score
start = time.time()
RANDOM = 47

data = pd.read_csv('./data_fe.csv')
test = pd.read_csv('./test_fe.csv')

y_train = data['TARGET']
X_train = data.drop(columns = ['SK_ID_CURR', 'TARGET'])
X_test = test.drop(columns = ['SK_ID_CURR'])

csv_lgbm = test[['SK_ID_CURR']].copy()
csv_catb = test[['SK_ID_CURR']].copy()
csv_xgbt = test[['SK_ID_CURR']].copy()
oof_lgbm = data[['SK_ID_CURR', 'TARGET']].copy()
oof_catb = data[['SK_ID_CURR', 'TARGET']].copy()
oof_xgbt = data[['SK_ID_CURR', 'TARGET']].copy()

print('X_train size: {}\nX_test size: {}'.format(X_train.shape, X_test.shape))

del data, test
gc.collect()

# train and predict LGBMClassifier
print('======================================== Start training LGBMClassifier ========================================')
oof_pred = np.zeros(X_train.shape[0])
y_pred = np.zeros(X_test.shape[0])
folds = KFold(n_splits= 5, shuffle=True, random_state=RANDOM)
for n_fold, (train_idx, valid_idx) in enumerate(folds.split(X_train, y_train)):
    size = train_idx.size
    oversample_idx = np.random.choice(size, size//10)
    train_idx = np.append(train_idx, oversample_idx)

    train_x, train_y = X_train.iloc[train_idx], y_train.iloc[train_idx]
    valid_x, valid_y = X_train.iloc[valid_idx], y_train.iloc[valid_idx]

    clf = LGBMClassifier(boosting_type='gbdt', class_weight=None, colsample_bytree=1.0,
                         learning_rate=0.02, max_depth=-1, min_child_samples=20,
                         min_child_weight=40, min_split_gain=0.01, n_estimators=10000,
                         n_jobs=-1, nthread=-1, num_leaves=16, objective=None,
                         random_state=None, reg_alpha=0.08, reg_lambda=0.0, silent=-1,
                         subsample=0.8, subsample_for_bin=200000, subsample_freq=0,
                         verbose=-1)

    clf.fit(train_x, train_y, eval_set=[(train_x, train_y), (valid_x, valid_y)], eval_metric= 'auc', verbose= 100, early_stopping_rounds= 50)
    oof_pred[valid_idx] = clf.predict_proba(valid_x, num_iteration=clf.best_iteration_)[:, 1]
    y_pred += clf.predict_proba(X_test, num_iteration=clf.best_iteration_)[:, 1] / folds.n_splits
    print('Fold %2d AUC : %.6f' % (n_fold + 1, roc_auc_score(valid_y, oof_pred[valid_idx])))
print('Full AUC score %.6f' % roc_auc_score(y_train, oof_pred))

csv_lgbm['TARGET'] = y_pred
csv_lgbm.to_csv('csv_lgbm.csv', index = False)
print('Run time: {:.2f}mins'.format((time.time() - start)/60))

oof_lgbm['PRED'] = oof_pred
oof_lgbm.to_csv('oof_lgbm.csv', index = False)

# train and predict CatBoostClassifier
print('======================================== Start training CatBoostClassifier ========================================')
oof_pred = np.zeros(X_train.shape[0])
y_pred = np.zeros(X_test.shape[0])
folds = KFold(n_splits= 5, shuffle=True, random_state=RANDOM)

# missing values
imputer = Imputer(strategy='median').fit(X_train)
X_train_ = imputer.transform(X_train)
X_test_ = imputer.transform(X_test)

X_train_ = pd.DataFrame(X_train_)
X_test_ = pd.DataFrame(X_test_)

for n_fold, (train_idx, valid_idx) in enumerate(folds.split(X_train_, y_train)):
    size = train_idx.size
    oversample_idx = np.random.choice(size, size//10)
    train_idx = np.append(train_idx, oversample_idx)

    train_x, train_y = X_train_.iloc[train_idx], y_train.iloc[train_idx]
    valid_x, valid_y = X_train_.iloc[valid_idx], y_train.iloc[valid_idx]

    clf = CatBoostClassifier(iterations=3000, border_count=20, l2_leaf_reg=5, depth=7, eval_metric='AUC', use_best_model=True, random_seed=RANDOM)

    clf.fit(train_x, train_y, eval_set=[(train_x, train_y), (valid_x, valid_y)], verbose= 100, early_stopping_rounds= 50)
    oof_pred[valid_idx] = clf.predict_proba(valid_x)[:, 1]
    y_pred += clf.predict_proba(X_test_)[:, 1] / folds.n_splits
    print('Fold %2d AUC : %.6f' % (n_fold + 1, roc_auc_score(valid_y, oof_pred[valid_idx])))
print('Full AUC score %.6f' % roc_auc_score(y_train, oof_pred))

# submit
csv_catb['TARGET'] = y_pred
csv_catb.to_csv('csv_catb.csv', index = False)
print('Run time: {:.2f}mins'.format((time.time() - start)/60))

oof_catb['PRED'] = oof_pred
oof_catb.to_csv('oof_catb.csv', index = False)

# train and predict XGBClassifier
print('======================================== Start training XGBClassifier ========================================')
oof_pred = np.zeros(X_train.shape[0])
y_pred = np.zeros(X_test.shape[0])
folds = KFold(n_splits=5, shuffle=True, random_state=RANDOM)
for n_fold, (train_idx, valid_idx) in enumerate(folds.split(X_train, y_train)):
    size = train_idx.size
    oversample_idx = np.random.choice(size, size//10)
    train_idx = np.append(train_idx, oversample_idx)

    train_x, train_y = X_train.iloc[train_idx], y_train.iloc[train_idx]
    valid_x, valid_y = X_train.iloc[valid_idx], y_train.iloc[valid_idx]

    clf = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1, colsample_bytree=0.7,
                        gamma=0, learning_rate=0.02, max_delta_step=0, max_depth=7, min_child_weight=1, missing=None,
                        n_estimators=2000, n_jobs=-1, nthread=-1, objective='binary:logistic', random_state=0,
                        reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None, silent=True, subsample=0.7)

    clf.fit(train_x, train_y, eval_set=[(train_x, train_y), (valid_x, valid_y)], eval_metric='auc', verbose=100, early_stopping_rounds=50)
    oof_pred[valid_idx] = clf.predict_proba(valid_x)[:, 1]
    y_pred += clf.predict_proba(X_test)[:, 1] / folds.n_splits
    print('Fold %2d AUC : %.6f' % (n_fold + 1, roc_auc_score(valid_y, oof_pred[valid_idx])))
print('Full AUC score %.6f' % roc_auc_score(y_train, oof_pred))

# submit
csv_xgbt['TARGET'] = y_pred
csv_xgbt.to_csv('csv_xgbt.csv', index=False)
print('Run time: {:.2f}mins'.format((time.time() - start)/60))

oof_xgbt['PRED'] = oof_pred
oof_xgbt.to_csv('oof_xgbt.csv', index=False)

# Stacking
data1 = oof_lgbm.copy()
data2 = oof_catb.drop(columns = ['TARGET'])
data3 = oof_xgbt.drop(columns = ['TARGET'])
data1.rename(columns={'PRED':'PRED_lgbm'}, inplace=True)
data2.rename(columns={'PRED':'PRED_catb'}, inplace=True)
data3.rename(columns={'PRED':'PRED_xgbt'}, inplace=True)
data = data1.join(data2.set_index('SK_ID_CURR'), on='SK_ID_CURR')
data = data.join(data3.set_index('SK_ID_CURR'), on='SK_ID_CURR')

test = pd.DataFrame()
test['SK_ID_CURR'] = csv_lgbm['SK_ID_CURR'].copy()
test['PRED_lgbm'] = csv_lgbm['TARGET']
test['PRED_catb'] = csv_catb['TARGET']
test['PRED_xgbt'] = csv_xgbt['TARGET']

y_train = data['TARGET'].copy()
X_train = data.drop(columns = ['SK_ID_CURR', 'TARGET'])
submission = test[['SK_ID_CURR']].copy()
X_test = test.drop(columns = ['SK_ID_CURR'])

# train and predict 2nd level model
print('======================================== Start training 2nd level model ========================================')
oof_pred = np.zeros(X_train.shape[0])
y_pred = np.zeros(X_test.shape[0])
folds = KFold(n_splits= 5, shuffle=True, random_state=RANDOM)
for n_fold, (train_idx, valid_idx) in enumerate(folds.split(X_train, y_train)):
    train_x, train_y = X_train.iloc[train_idx], y_train.iloc[train_idx]
    valid_x, valid_y = X_train.iloc[valid_idx], y_train.iloc[valid_idx]

    clf = CatBoostClassifier(eval_metric='AUC', use_best_model=True)
    clf.fit(train_x, train_y, eval_set=[(train_x, train_y), (valid_x, valid_y)], verbose= 100, early_stopping_rounds= 50)
    oof_pred[valid_idx] = clf.predict_proba(valid_x)[:, 1]

    y_pred += clf.predict_proba(X_test)[:, 1] / folds.n_splits
    print('Fold %2d AUC : %.6f' % (n_fold + 1, roc_auc_score(valid_y, oof_pred[valid_idx])))
print('Full AUC score %.6f' % roc_auc_score(y_train, oof_pred))
submission['TARGET'] = y_pred
print(submission.head())
submission.to_csv('report.csv', index = False)
