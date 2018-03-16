import train_and_test
from lib.results_handler import generate_results,summurize_results,showing_mean_values
import pandas as pd
import numpy as np
import sys
features_final, target_var= train_and_test.get_feature_final_and_target_var()

# Specifying information of the result I want.
result_keys = [
            'random_state',
            'clf_1_f1_score',
            'clf_1_n_estimators',
            'clf_2_f1_score',
            'clf_2_n_estimators',
            'important_features',
            'time'
        ]

# Specifying the argument of the method which executes training and testing except for random_state
other_args = {
    'features_final': features_final,
    'target_var': target_var,
    'f_select_range':[0,50],
    'n_estimators': 300
}

#Specify random_states you wish to try
random_states = range(1)

#Executing  training and testing 10 times with 10 different inputs and getting the results
all_res_df = generate_results(train_and_test, 'train_and_measure_performance_3', result_keys, random_states, other_args)

# Making pandas dataframe to show all the rows
pd.set_option("display.max_colwidth", 1000)
pd.set_option("display.max_rows", 1000)

# Getting correlations between q30 and the other features
features_to_focus = list(all_res_df['important_features'][0].index)
features_final['q30'] = target_var
features_to_focus.append('q30')
correlations = features_final[features_to_focus].corr()

# Combining feature importance and correlation with q30
feature_importance_and_corr_with_q30 = all_res_df['important_features'][0].to_frame()
feature_importance_and_corr_with_q30['corr_with_q30'] = correlations['q30']
feature_importance_and_corr_with_q30.rename(columns={0:'feature_importance'},inplace=True)

# Showing important features and
print feature_importance_and_corr_with_q30

#Saving correlation between q30 and the other features
feature_importance_and_corr_with_q30.to_csv('feature_importance_and_corr_with_q30_f_100_r_0.csv')







