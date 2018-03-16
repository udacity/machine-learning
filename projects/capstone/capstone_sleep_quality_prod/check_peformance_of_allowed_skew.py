# Importing necessary modules and functions
import sys
from lib.results_handler import generate_results,showing_mean_values,summurize_results
import train_and_test
from lib import li

# Getting final inputs and a target variable
features_final, target_var= train_and_test.get_feature_final_and_target_var()

# Specifying information of the result I want.
result_keys = [
            'random_state',
            'base_clf_accuracy',
            'boosted_clf_accuracy'
        ]
# Specifying arguments of the method except for random_state
other_args = {'features_final': features_final, 'target_var': target_var}

# Specifing random_states
random_states = range(10)

# Executing training and testing 10 times with 10 different inputs and getting those results
all_res_df = generate_results(train_and_test, 'initial_train_and_measure_performance', result_keys, random_states,other_args)

# Preparation for making a summary for the results
result_keys.remove('random_state')
summary_config = {}
for result_column in result_keys:
    summary_config[result_column] = 'mean'

# Getting a summary of the result
summary_df = summurize_results(all_res_df,summary_config)

# Combining the result and summary and outputting it to csv
all_res_df_with_summary = all_res_df.append(summary_df,ignore_index=True)
all_res_df_with_summary.to_csv("allowed_skews_check_results.csv")

# Printing the results
print all_res_df
showing_mean_values(all_res_df, result_keys)

