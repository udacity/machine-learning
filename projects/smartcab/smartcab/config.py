import argparse
from collections import OrderedDict
import inspect
from agent import smartcab_sim_run_funcs


def categorize_flags(set_flags):
    """
        gives categorized keyword argument dict that functions inside run() can unpack for user-set flags
        :param set_flags: argparse parser output of user-set flags
        :type set_flags: dict
        :rtype dict
        :returns dict of section flags
        """
    user_flags = {cat: {flag: set_flags[flag] for flag in flag_config[cat]} for cat in flag_config}
    return user_flags


def set_all_defaults(parser, *funcs):
    """
    Set default values from function declaration so there's no mix up.

    Warning: Issues may occur if default function values goes from True -> False or vice versa as in argument actions
    in `flags` have to change from 'store_false' to 'store_true' and vice versa :type parser: argparse.ArgumentParser
    """
    assert all(callable(f) for f in funcs)
    assert isinstance(parser, argparse.ArgumentParser)
    defaults = {}
    for f in funcs:
        defaults.update(get_defaults(f))
    parser.set_defaults(**defaults)


def get_defaults(func):
    getargspec = inspect.getargspec
    info = getargspec(func)
    d = len(info.defaults)
    return {k: v for k, v in zip(info.args[-d:], info.defaults)}


flag_categories = ['env', 'agent', 'deadline', 'sim', 'run']
flag_config = dict(
    env={
        'verbose': {
            'names': ('-v', '--verbose'),
            'kwargs': dict(action='store_true', help='generates additional output from the simulation')
        },
        'num_dummies': {
            'names': ('-N', '--num_dummies'),
            'kwargs': dict(type=int, metavar=('INT'), help='number of dummy agents in the environment')
        },
        'grid_size': {
            'names': ('-g', '--grid_size'),
            'kwargs': dict(nargs=2, type=int, metavar=('COLS', 'ROWS'),
                           help='controls the number of intersections = columns * rows')
        }
    },
    agent={
        'learning': {
            'names': ('-l', '--learning'),
            'kwargs': dict(action='store_true', help='forces the driving agent to use Q-learning')
        },
        'epsilon': {
            'names': ('-e', '--epsilon'),
            'kwargs': dict(type=float, metavar=('FLOAT'), help='NO EFFECT without -l: value for the exploration factor')
        },
        'alpha': {
            'names': ('-a', '--alpha'),
            'kwargs': dict(type=float, metavar=('FLOAT'), help='NO EFFECT without -l: value for the learning rate')
        }
    },
    deadline={
        'enforce_deadline': {
            'names': ['-D', '--deadline'],
            'kwargs': dict(action='store_true', dest='enforce_deadline',
                           help='enforce a deadline metric on the driving agent')
        }
    },
    sim={
        'update_delay': {
            'names': ('-u', '--update-delay'),
            'kwargs': dict(type=float, metavar=('SECONDS'), help='time between actions of smartcab/environment')
        },
        'display': {'names': ('-d', '--display'), 'kwargs': dict(action='store_false', help='disable simulation GUI')},
        'log_metrics': {
            'names': ('-L', '--log'),
            'kwargs': dict(action='store_true', dest='log_metrics', help='log trial and simulation results to /logs')
        },
        'optimized': {
            'names': ('-o', '--optimized'),
            'kwargs': dict(action='store_true', help='change the default log file name if optimized')
        }
    },
    run={
        'tolerance': {
            'names': ('-t', '--tolerance'),
            'kwargs': dict(type=float, metavar=('FLOAT'),
                           help='epsilon tolerance before beginning testing after exploration')
        },
        'n_test': {
            'names': ('-n', '--n_test'),
            'kwargs': dict(type=int, metavar=('INT'), help='number of testing trials to perform')
        }
    })
flag_config = OrderedDict(sorted(flag_config.items(), key=lambda t: flag_categories.index(t[0])))


def command_line_parse():
    """gets user-set flags from command line"""
    parser = argparse.ArgumentParser(description='runs the smartcab simulation with various options',
                                     usage='smartcab/agent.py [-h] [-v]'
                                           '\n   env flags:     [-N <dummies> -g <cols> <rows>]'
                                           '\n   drive flags:   [-l [-a <float> -e <float>]'
                                           '\n   deadline flag: [-D]'
                                           '\n   sim flags:     [-dLo -u <delay_secs>]'
                                           '\n   run flags:     [-t <tolerance> -n <tests>]',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    helps = ['environment/world options', 'driving agent options', 'deadline option',
             'simulation options', 'run-time experiment options']
    arg_groups = {key: parser.add_argument_group(text) for key, text in zip(flag_categories, helps)}
    for group in flag_config:
        for arg_name in flag_config[group]:
            d = flag_config[group][arg_name]
            arg_groups[group].add_argument(*d['names'], **d['kwargs'])
    set_all_defaults(parser, *smartcab_sim_run_funcs)
    flat_flags = vars(parser.parse_args())
    flat_flags['grid_size'] = tuple(flat_flags['grid_size'])
    return categorize_flags(flat_flags)