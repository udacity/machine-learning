import train_and_test
from lib.results_handler import generate_results,summurize_results,showing_mean_values
from lib import li

#Getting final inputs and a target variable
features_final, target_var= train_and_test.get_feature_final_and_target_var()

# Specifying the information of the result I want.
result_keys = [
            'random_state',
            'base_clf_f1_score',
            'base_clf_n_estimators',
            'best_clf_f1_score',
            'best_clf_n_estimators',
            #'important_features',
            'time'
        ]

# Specifying arguments of the method except for random_state
other_args = {
    'features_final': features_final,
    'target_var': target_var,
    'f_select_range':[0,25],
    'base_clf_n_estimators': 300,
    'boosting_clf_n_estimators': 10,
    'boosting_clf_learning_rate': 0.05
}

# Specifying the random_states I with to try
random_states = range(10)

# Executing training and testing 10 times with 10 different inputs and getting those results
all_res_df = generate_results(train_and_test, 'train_and_measure_performance_2', result_keys, random_states, other_args)

# Preparation for making a summary for the results
result_keys = li.remove(result_keys,['random_state'])
summary_config = {}
for result_column in result_keys:
    summary_config[result_column] = 'mean'

# Combining the result and summary and outputting it to csv
summary_df = summurize_results(all_res_df,summary_config)
all_res_df_with_summary = all_res_df.append(summary_df,ignore_index=True)
all_res_df_with_summary.to_csv("results_rf_arf_f_0_50.csv")

# Printing the results
print all_res_df_with_summary
showing_mean_values(all_res_df, result_keys)