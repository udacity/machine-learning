import train_and_test
from lib.results_handler import generate_results,summurize_results,showing_mean_values
from lib import li

#Getting final inputs and a target variable
features_final, target_var= train_and_test.get_feature_final_and_target_var()

# Specifying the information of the result I want.
result_columns = [
            'random_state',
            'clf_1_f1_score',
            'clf_1_n_estimators',
            'clf_2_f1_score',
            'clf_2_n_estimators',
            # 'important_features',
            'time'
        ]

# Specifying the argument of the method which executes training and testing except for random_state
other_args = {
    'features_final': features_final,
    'target_var': target_var,
    'f_select_range':[0,25],
    'n_estimators':300}

#Specifing the random_states I with to try
random_states = range(10)

#Executing the training and testing 10 times with 10 different inputs and getting the results
all_res_df = generate_results(train_and_test, 'train_and_measure_performance_3', result_columns, random_states, other_args)

#Preparation for making a summary for the results
result_columns = li.remove(result_columns,['random_state'])

summary_config = {}
for result_column in result_columns:
    summary_config[result_column] = 'mean'

#Combining the result and summary and outputting it to csv
summary_df = summurize_results(all_res_df,summary_config)
all_res_df_with_summary = all_res_df.append(summary_df,ignore_index=True)
all_res_df_with_summary.to_csv("results_rf_rf_f_0_25.csv")

#Printing the results
print all_res_df_with_summary
showing_mean_values(all_res_df, result_columns)

