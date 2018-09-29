#
import warnings, os, gc, time
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
import pandas as pd
import numpy as np
from math import log

# Load dataset
application_train_ = pd.read_csv('./dataset/application_train.csv')
application_test_ = pd.read_csv('./dataset/application_test.csv')
train_size_ = application_train_.shape[0]
application = pd.concat((application_train_, application_test_)).reset_index(drop=True)

# Categorical
## Anomaly
application['CODE_GENDER'].replace('XNA', 'F', inplace=True)

## Target-encoding
cat_features = [col for col in application_train_.columns if application_train_[col].dtype == 'object']
target_encoding = dict.fromkeys(cat_features, 0)
for feature in cat_features:
    cat_ = application[feature].dropna().unique()
    default_percentage = []
    for k, v in enumerate(cat_):
        repay = application[(application[feature] == v) & (application.TARGET == 0)].shape[0]
        default = application[(application[feature] == v) & (application.TARGET == 1)].shape[0]
        default_percentage.append(100 * (default/(repay + default)))
    feature_map = {key:value for (key, value) in zip(cat_, default_percentage)}
    target_encoding[feature] = feature_map
for feat in target_encoding:
    application[feat].replace(target_encoding[feat], inplace=True)

# Numerical
## Anomaly
application['REGION_RATING_CLIENT_W_CITY'].replace(-1, 2, inplace=True)
application.loc[application.AMT_INCOME_TOTAL == 117000000, 'AMT_INCOME_TOTAL'] = 117000
application.loc[application.AMT_REQ_CREDIT_BUREAU_QRT > 100, 'AMT_REQ_CREDIT_BUREAU_QRT'] = np.nan
application.loc[application.OBS_30_CNT_SOCIAL_CIRCLE > 300, 'OBS_30_CNT_SOCIAL_CIRCLE'] = np.nan
application.loc[application.OBS_60_CNT_SOCIAL_CIRCLE > 300, 'OBS_60_CNT_SOCIAL_CIRCLE'] = np.nan
### DAYS_EMPLOYED > 0
### https://www.kaggle.com/c/home-credit-default-risk/discussion/57247
application["DAYS_EMPLOYED"].replace(365243, 0, inplace=True)
## missing value
application['NONLIVINGAPARTMENTS_MODE'].fillna(value=1, inplace=True)

house_features_AVG = [col for col in application.columns if col.find('AVG')!= -1]
house_features_MODE = [col for col in application.columns if col.find('MODE')!= -1]
house_features_MEDI = [col for col in application.columns if col.find('MEDI')!= -1]
house_features = house_features_AVG + house_features_MODE + house_features_MEDI
for _ in house_features:
    application[_].fillna(0.0, inplace=True)

# Handcraft features
application["AGE"] = application["DAYS_BIRTH"].abs()//365
application['AMT_INCOME_TOTAL_K'] = application['AMT_INCOME_TOTAL']//1000
application['Long_employment'] = (application['DAYS_EMPLOYED'] < (-365)*5).astype(int)
application['Age_38up'] = (application['DAYS_BIRTH'] < (-365*38)).astype(int)

# Ratio feature engineering
application['ratio_annuity_income'] = application['AMT_ANNUITY'] / application['AMT_INCOME_TOTAL']
application['ratio_car_to_birth'] = application['OWN_CAR_AGE'] / application['DAYS_BIRTH']
application['ratio_car_to_employ'] = application['OWN_CAR_AGE'] / application['DAYS_EMPLOYED']
application['ratio_children'] = application['CNT_CHILDREN'] / application['CNT_FAM_MEMBERS']
application['ratio_credit_to_annuity'] = application['AMT_CREDIT'] / application['AMT_ANNUITY']
application['ratio_credit_to_goods'] = application['AMT_CREDIT'] / application['AMT_GOODS_PRICE']
application['ratio_credit_to_income'] = application['AMT_CREDIT'] / application['AMT_INCOME_TOTAL']
application['ratio_days_employed'] = application['DAYS_EMPLOYED'] / application['DAYS_BIRTH']
application['ratio_income_credit'] = application['AMT_INCOME_TOTAL'] / application['AMT_CREDIT']
application['ratio_income_per_child'] = application['AMT_INCOME_TOTAL'] / (1 + application['CNT_CHILDREN'])
application['ratio_income_per_person'] = application['AMT_INCOME_TOTAL'] / application['CNT_FAM_MEMBERS']
application['ratio_payment_rate'] = application['AMT_ANNUITY'] / application['AMT_CREDIT']
application['ratio_phone_to_birth'] = application['DAYS_LAST_PHONE_CHANGE'] / application['DAYS_BIRTH']
application['ratio_phone_to_employ'] = application['DAYS_LAST_PHONE_CHANGE'] / application['DAYS_EMPLOYED']

# Aggregation feature engineering
application['external_sources_weighted'] = application.EXT_SOURCE_1 * 2 + application.EXT_SOURCE_2 * 3 + application.EXT_SOURCE_3 * 4
for function_name in ['min', 'max', 'sum', 'mean', 'nanmedian']:
    application['external_sources_{}'.format(function_name)] = eval('np.{}'.format(function_name))(
        application[['EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3']], axis=1)

AGGREGATION_RECIPIES = [
    (['CODE_GENDER', 'NAME_EDUCATION_TYPE'],
     [('AMT_ANNUITY', 'max'), ('AMT_CREDIT', 'max'),
      ('EXT_SOURCE_1', 'mean'), ('EXT_SOURCE_2', 'mean'),
      ('OWN_CAR_AGE', 'max'), ('OWN_CAR_AGE', 'sum')]),
    (['CODE_GENDER', 'ORGANIZATION_TYPE'],
     [('AMT_ANNUITY', 'mean'), ('AMT_INCOME_TOTAL', 'mean'),
      ('DAYS_REGISTRATION', 'mean'), ('EXT_SOURCE_1', 'mean')]),
    (['CODE_GENDER', 'REG_CITY_NOT_WORK_CITY'],
     [('AMT_ANNUITY', 'mean'), ('CNT_CHILDREN', 'mean'), ('DAYS_ID_PUBLISH', 'mean')]),
    (['CODE_GENDER', 'NAME_EDUCATION_TYPE', 'OCCUPATION_TYPE', 'REG_CITY_NOT_WORK_CITY'],
     [('EXT_SOURCE_1', 'mean'), ('EXT_SOURCE_2', 'mean')]),

    (['NAME_EDUCATION_TYPE', 'OCCUPATION_TYPE'],
     [('AMT_CREDIT', 'mean'), ('AMT_REQ_CREDIT_BUREAU_YEAR', 'mean'),
      ('APARTMENTS_AVG', 'mean'), ('BASEMENTAREA_AVG', 'mean'),
      ('EXT_SOURCE_1', 'mean'), ('EXT_SOURCE_2', 'mean'), ('EXT_SOURCE_3', 'mean'),
      ('NONLIVINGAREA_AVG', 'mean'), ('OWN_CAR_AGE', 'mean'), ('YEARS_BUILD_AVG', 'mean')]),
    (['NAME_EDUCATION_TYPE', 'OCCUPATION_TYPE', 'REG_CITY_NOT_WORK_CITY'],
     [('ELEVATORS_AVG', 'mean'), ('EXT_SOURCE_1', 'mean')]),
    (['OCCUPATION_TYPE'],
     [('AMT_ANNUITY', 'mean'), ('CNT_CHILDREN', 'mean'), ('CNT_FAM_MEMBERS', 'mean'),
      ('DAYS_BIRTH', 'mean'), ('DAYS_EMPLOYED', 'mean'),
      ('DAYS_ID_PUBLISH', 'mean'), ('DAYS_REGISTRATION', 'mean'),
      ('EXT_SOURCE_1', 'mean'), ('EXT_SOURCE_2', 'mean'), ('EXT_SOURCE_3', 'mean')])]

groupby_aggregate_names = []
for groupby_cols, specs in (AGGREGATION_RECIPIES):
    group_object = application.groupby(groupby_cols)
    for select, agg in (specs):
        groupby_aggregate_name = '{}_{}_{}'.format('_'.join(groupby_cols), agg, select)
        application = application.merge(group_object[select].agg(agg).reset_index()
                              .rename(index=str, columns={select: groupby_aggregate_name})
                              [groupby_cols + [groupby_aggregate_name]], on=groupby_cols,how='left')
        groupby_aggregate_names.append(groupby_aggregate_name)

# Diff feature engineering
diff_feature_names = []
for groupby_cols, specs in (AGGREGATION_RECIPIES):
    for select, agg in (specs):
        if agg in ['mean','median','max','min']:
            groupby_aggregate_name = '{}_{}_{}'.format('_'.join(groupby_cols), agg, select)
            diff_name = '{}_diff'.format(groupby_aggregate_name)
            abs_diff_name = '{}_abs_diff'.format(groupby_aggregate_name)
            application[diff_name] = application[select] - application[groupby_aggregate_name]
            application[abs_diff_name] = np.abs(application[select] - application[groupby_aggregate_name])
            diff_feature_names.append(diff_name)
            diff_feature_names.append(abs_diff_name)

# Generate new csv
application_train = application[:train_size_].copy()
application_test = application[train_size_:].copy()
application_test.drop(columns = ['TARGET'], inplace=True)
application_train.to_csv('application_train_final.csv', index=False)
application_test.to_csv('application_test_final.csv', index=False)
