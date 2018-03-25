import pandas as pd
import inspect
import sys


def generate_results(object,exec_func,result_keys,random_states, other_args = {}):
    """

    :param object object:object which contains function to execute.
    :param string exec_func:function name to execute in string
    :param list result_keys:The kind of results you wish to obtain in the form of list.

    result_keys = [
            'random_state',
            'base_clf_accuracy',
            'boosted_clf_accuracy'
    ]

    The function you specify have to return those results in the form of dictionary.

    result_keys = {
            'random_state': 0,
            'base_clf_accuracy': 0.68,
            'boosted_clf_accuracy' 0.7
    }

    :param list random_states: random_states you wish to try in the form of list.
    :param dictionary other_args: args except for random_states in the form of dictionary


    :return:
    """

    func_to_call = getattr(object, exec_func)
    all_res_df = pd.DataFrame([])
    args = other_args
    for random_state in random_states:
        args['random_state'] = random_state
        result = func_to_call(**args)
        values = []
        for value in result_keys:
            values.append(result[value])
        res_df = pd.DataFrame(
            [
                values
            ],
            columns=result_keys
        )
        all_res_df = all_res_df.append(res_df, ignore_index=True)
    return all_res_df

def showing_mean_values(df, column_names):
    """

    Just shows mean values of specified columns

    :param pandas.core.frame.DataFrame df: Pandas dataframe which contains columns you wish to show their mean values.
    :param list column_names: Column names you wish to show their mean values.
    """
    for column in  column_names:
        print "Mean of "+ column + ": {:.4f}".format(df[column].mean())

def summurize_results(df, config):
    """
    Gets summary of results. Currently it only handles "mean",

    :param pandas.core.frame.DataFrame df: Pandas dataframe you wish to summurize its result
    :param dictionary config: The config of how to summarize for each column
    :return pandas.core.frame.DataFrame res_df: Returns summary of the result.
    """
    res_df = pd.DataFrame([])
    for column, each_config in config.iteritems():
        if each_config == 'mean':
            res_df.loc[0,column] = df[column].mean()
    return res_df

