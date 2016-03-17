import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def filter_data(data, condition):
    """
    Remove elements that do not match the condition provided.
    Takes a data list as input and returns a filtered list.
    Conditions should be a list of strings of the following format:
      '<field> <op> <value>'
    where the following operations are valid: >, <, >=, <=, ==, !=
    
    Example: ["Sex == 'male'", 'Age < 18']
    """
    field, op, value = condition.split(" ")
    # convert value into number or strip excess quotes if string
    try:
        value = float(value)
    except:
        value = value.strip("\'\"")
    
    # get booleans for filtering
    if op == ">":
        matches = data[field] > value
    elif op == "<":
        matches = data[field] < value
    elif op == ">=":
        matches = data[field] >= value
    elif op == "<=":
        matches = data[field] <= value
    elif op == "==":
        matches = data[field] == value
    elif op == "!=":
        matches = data[field] != value
    else: # catch invalid operation codes
        raise Exception("Invalid comparison operator. Only >, <, >=, <=, ==, != allowed.")
    
    # filter data and outcomes
    data = data[matches].reset_index()
    return data

def survival_stats(data, outcomes, key, filters = []):
    """
    Print out selected statistics regarding survival, given a feature of
    interest and any number of filters (including no filters)
    """
    # Merge data and outcomes into single dataframe
    all_data = pd.concat([data, outcomes], axis = 1)
    
    # Apply filters to data
    for condition in filters:
        all_data = filter_data(all_data, condition)
    all_data = all_data[[key, 'Survived']]
    
    # Create different plot depending on if key takes string values
    # or numeric values.
    plt.figure(figsize=(8,6))
    if isinstance(all_data[key][0] , str):
        # For strings, collect unique strings and then count number of
        # outcomes for survival and non-survival.
        
        # Summarize dataframe to get counts in each group
        all_data['count'] = 1
        all_data = all_data.groupby([key, 'Survived'], as_index = False).count()
        
        levels = all_data[key].unique()
        n_levels = len(levels)
        bar_width = 0.4
        
        for i in range(n_levels):
            # bars should be paired with non-survived first followed by survived.
            nonsurv_bar = plt.bar(i-bar_width, all_data.loc[2*i]['count'], width = bar_width,
                    color = 'r')
            surv_bar = plt.bar(i, all_data.loc[2*i+1]['count'], width = bar_width,
                    color = 'g')
        
        # add labels to ticks for each group of bars.
        plt.xticks(range(n_levels), levels)
        
        # add legend to plot.    
        plt.legend((nonsurv_bar[0], surv_bar[0]),('Did not survive', 'Survived'), framealpha = 0.8)
        
    else:
        # For numbers, divide the range of data into bins and count
        # number of outcomes for survival and non-survival in each bin.
        
        # Get range of data, split data into bins for reporting.
        min_value = all_data[key].min()
        max_value = all_data[key].max()
        value_range = max_value - min_value
        n_bins = 8
        bin_size = float(value_range) / n_bins
        bins = [i*bin_size + min_value for i in range(n_bins+1)]
        
        # plot the data
        nonsurv_vals = all_data[all_data['Survived'] == 0][key].reset_index(drop = True)
        surv_vals = all_data[all_data['Survived'] == 1][key].reset_index(drop = True)
        plt.hist(nonsurv_vals, bins = bins, alpha = 0.6,
                 color = 'red', label = 'Did not survive')
        plt.hist(surv_vals, bins = bins, alpha = 0.6,
                 color = 'green', label = 'Survived')
        
        # add legend to plot.
        plt.legend(framealpha = 0.8)
        
    # common attributes for plot formatting
    plt.xlabel(key)
    plt.ylabel('Count')
    plt.show()

    # Report number of points with missing values.
    if sum(pd.isnull(all_data[key])):
        nan_outcomes = all_data[pd.isnull(all_data[key])]['Survived']
        print '# of persons with missing values: {}'.format(len(nan_outcomes))
        print '  # that survived: {}'.format(sum(nan_outcomes == 1))
        print '  # that did not survive: {}'.format(sum(nan_outcomes == 0))