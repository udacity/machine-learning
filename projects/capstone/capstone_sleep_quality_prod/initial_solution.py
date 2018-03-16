# Importing necessary module and functions
import sys
from lib.results_handler import generate_results,showing_mean_values,summurize_results
import train_and_test

# Getting final inputs and a target variable
features_final, target_var= train_and_test.get_feature_final_and_target_var()

# Specifying information of the result I want.
result_columns = [
            'random_state',
            'base_clf_f1_score',
            'boosted_clf_f1_score'
        ]
# Specifying arguments of the method except for random_state
other_args = {'features_final': features_final, 'target_var': target_var}

# Specifying random_states
random_states = range(10)

# Executing training and testing 10 times with 10 different inputs and getting the results
all_res_df = generate_results(train_and_test, 'initial_train_and_measure_performance', result_columns, random_states,other_args)

# Preparation for making a summary for the results
result_columns.remove('random_state')
summary_config = {}
for result_column in result_columns:
    summary_config[result_column] = 'mean'

# Getting summary for the result
summary_df = summurize_results(all_res_df,summary_config)

# Combining the result and summary and outputting it to csv
all_res_df_with_summary = all_res_df.append(summary_df,ignore_index=True)
all_res_df_with_summary.to_csv("initial_solution_result.csv")

# Printing the results
print all_res_df
showing_mean_values(all_res_df, result_columns)

