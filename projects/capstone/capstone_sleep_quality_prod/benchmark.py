
import sys
import train_and_test
from lib.results_handler import generate_results,summurize_results

# Getting final inputs and a target variable
features_final, target_var= train_and_test.get_feature_final_and_target_var(benchmark=True)

# Specifying information of the result you want.
result_keys = ['f1_score','random_state']

# Specifying arguments of the method except for random_state
other_args = {'features_final':features_final,'target_var': target_var}

# Specifying random_states
random_states = range(10)

# Executing the training and testing 10 times with 10 different inputs and getting the results

all_res_df = generate_results(train_and_test, 'benchmark_train_and_measure_performance', result_keys, random_states,other_args)
result_keys.remove('random_state')

# Preparation for making a summary for the results
summary_config = {}
for result_column in result_keys:
    summary_config[result_column] = 'mean'

# Getting summary of the result
summary_df = summurize_results(all_res_df,summary_config)

# Combining the result and summary and outputting it to csv
all_res_df_with_summary = all_res_df.append(summary_df,ignore_index=True)
all_res_df_with_summary.to_csv("benchmark_results.csv")

# Printing the results
print all_res_df_with_summary
print "Mean of f1_score: {:.4f}".format(all_res_df['f1_score'].mean())