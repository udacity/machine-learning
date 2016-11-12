###########################################
# Suppress matplotlib user warnings
# Necessary for newer version of matplotlib
import warnings
warnings.filterwarnings("ignore", category = UserWarning, module = "matplotlib")
###########################################
#
# Display inline matplotlib plots with IPython
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
###########################################

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import ast


def calculate_safety(data):
	""" Calculates the safety rating of the smartcab during testing. """

	good_ratio = data['good_actions'].sum() * 1.0 / \
	(data['initial_deadline'] - data['final_deadline']).sum()

	if good_ratio == 1: # Perfect driving
		return ("A+", "green")
	else: # Imperfect driving
		if data['actions'].apply(lambda x: ast.literal_eval(x)[4]).sum() > 0: # Major accident
			return ("F", "red")
		elif data['actions'].apply(lambda x: ast.literal_eval(x)[3]).sum() > 0: # Minor accident
			return ("D", "#EEC700")
		elif data['actions'].apply(lambda x: ast.literal_eval(x)[2]).sum() > 0: # Major violation
			return ("C", "#EEC700")
		else: # Minor violation
			minor = data['actions'].apply(lambda x: ast.literal_eval(x)[1]).sum()
			if minor >= len(testing_data)/2: # Minor violation in at least half of the trials
				return ("B", "green")
			else:
				return ("A", "green")


def calculate_reliability(data):
	""" Calculates the reliability rating of the smartcab during testing. """

	success_ratio = data['success'].sum() * 1.0 / len(data)

	if success_ratio == 1: # Always meets deadline
		return ("A+", "green")
	else:
		if success_ratio >= 0.90:
			return ("A", "green")
		elif success_ratio >= 0.80:
			return ("B", "green")
		elif success_ratio >= 0.70:
			return ("C", "#EEC700")
		elif success_ratio >= 0.60:
			return ("D", "#EEC700")
		else:
			return ("F", "red")


def plot_trials(csv):
	""" Plots the data from logged metrics during a simulation."""

	data = pd.read_csv(os.path.join("logs", csv))

	if len(data) < 10:
		print "Not enough data collected to create a visualization."
		print "At least 20 trials are required."
		return
	
	# Create additional features
	data['average_reward'] = pd.rolling_mean(data['net_reward'] / (data['initial_deadline'] - data['final_deadline']), 10)
	data['reliability_rate'] = pd.rolling_mean(data['success']*100, 10)  # compute avg. net reward with window=10
	data['good_actions'] = data['actions'].apply(lambda x: ast.literal_eval(x)[0])
	data['good'] = pd.rolling_mean(data['good_actions'] * 1.0 / \
		(data['initial_deadline'] - data['final_deadline']), 10)
	data['minor'] = pd.rolling_mean(data['actions'].apply(lambda x: ast.literal_eval(x)[1]) * 1.0 / \
		(data['initial_deadline'] - data['final_deadline']), 10)
	data['major'] = pd.rolling_mean(data['actions'].apply(lambda x: ast.literal_eval(x)[2]) * 1.0 / \
		(data['initial_deadline'] - data['final_deadline']), 10)
	data['minor_acc'] = pd.rolling_mean(data['actions'].apply(lambda x: ast.literal_eval(x)[3]) * 1.0 / \
		(data['initial_deadline'] - data['final_deadline']), 10)
	data['major_acc'] = pd.rolling_mean(data['actions'].apply(lambda x: ast.literal_eval(x)[4]) * 1.0 / \
		(data['initial_deadline'] - data['final_deadline']), 10)
	data['epsilon'] = data['parameters'].apply(lambda x: ast.literal_eval(x)['e']) 
	data['alpha'] = data['parameters'].apply(lambda x: ast.literal_eval(x)['a']) 


	# Create training and testing subsets
	training_data = data[data['testing'] == False]
	testing_data = data[data['testing'] == True]

	plt.figure(figsize=(12,8))


	###############
	### Average step reward plot
	###############
	
	ax = plt.subplot2grid((6,6), (0,3), colspan=3, rowspan=2)
	ax.set_title("10-Trial Rolling Average Reward per Action")
	ax.set_ylabel("Reward per Action")
	ax.set_xlabel("Trial Number")
	ax.set_xlim((10, len(training_data)))

	# Create plot-specific data
	step = training_data[['trial','average_reward']].dropna()

	ax.axhline(xmin = 0, xmax = 1, y = 0, color = 'black', linestyle = 'dashed')
	ax.plot(step['trial'], step['average_reward'])


	###############
	### Parameters Plot
	###############

	ax = plt.subplot2grid((6,6), (2,3), colspan=3, rowspan=2)

	# Check whether the agent was expected to learn
	if csv != 'sim_no-learning.csv':
		ax.set_ylabel("Parameter Value")
		ax.set_xlabel("Trial Number")
		ax.set_xlim((1, len(training_data)))
		ax.set_ylim((0, 1.05))

		ax.plot(training_data['trial'], training_data['epsilon'], color='blue', label='Exploration factor')
		ax.plot(training_data['trial'], training_data['alpha'], color='green', label='Learning factor')

		ax.legend(bbox_to_anchor=(0.5,1.19), fancybox=True, ncol=2, loc='upper center', fontsize=10)

	else:
		ax.axis('off')
		ax.text(0.52, 0.30, "Simulation completed\nwith learning disabled.", fontsize=24, ha='center', style='italic')	


	###############
	### Bad Actions Plot
	###############
	
	actions = training_data[['trial','good', 'minor','major','minor_acc','major_acc']].dropna()
	maximum = (1 - actions['good']).values.max()
	
	ax = plt.subplot2grid((6,6), (0,0), colspan=3, rowspan=4)
	ax.set_title("10-Trial Rolling Relative Frequency of Bad Actions")
	ax.set_ylabel("Relative Frequency")
	ax.set_xlabel("Trial Number")

	ax.set_ylim((0, maximum + 0.01))
	ax.set_xlim((10, len(training_data)))

	ax.set_yticks(np.linspace(0, maximum+0.01, 10))

	ax.plot(actions['trial'], (1 - actions['good']), color='black', label='Total Bad Actions', linestyle='dotted', linewidth=3)
	ax.plot(actions['trial'], actions['minor'], color='orange', label='Minor Violation', linestyle='dashed')
	ax.plot(actions['trial'], actions['major'], color='orange', label='Major Violation', linewidth=2)
	ax.plot(actions['trial'], actions['minor_acc'], color='red', label='Minor Accident', linestyle='dashed')
	ax.plot(actions['trial'], actions['major_acc'], color='red', label='Major Accident', linewidth=2)
	
	ax.legend(loc='upper right', fancybox=True, fontsize=10)


	###############
	### Rolling Success-Rate plot
	###############
	
	ax = plt.subplot2grid((6,6), (4,0), colspan=4, rowspan=2)
	ax.set_title("10-Trial Rolling Rate of Reliability")
	ax.set_ylabel("Rate of Reliability")
	ax.set_xlabel("Trial Number")
	ax.set_xlim((10, len(training_data)))
	ax.set_ylim((-5, 105))
	ax.set_yticks(np.arange(0, 101, 20))
	ax.set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])

	# Create plot-specific data
	trial = training_data.dropna()['trial']
	rate = training_data.dropna()['reliability_rate']

	# Rolling success rate
	ax.plot(trial, rate, label="Reliability Rate", color='blue')


	###############
	### Test results
	###############

	ax = plt.subplot2grid((6,6), (4,4), colspan=2, rowspan=2)
	ax.axis('off')

	if len(testing_data) > 0:
		safety_rating, safety_color = calculate_safety(testing_data)
		reliability_rating, reliability_color = calculate_reliability(testing_data)

		# Write success rate
		ax.text(0.40, .9, "{} testing trials simulated.".format(len(testing_data)), fontsize=14, ha='center')
		ax.text(0.40, 0.7, "Safety Rating:", fontsize=16, ha='center')
		ax.text(0.40, 0.42, "{}".format(safety_rating), fontsize=40, ha='center', color=safety_color)
		ax.text(0.40, 0.27, "Reliability Rating:", fontsize=16, ha='center')
		ax.text(0.40, 0, "{}".format(reliability_rating), fontsize=40, ha='center', color=reliability_color)

	else:
		ax.text(0.36, 0.30, "Simulation completed\nwith testing disabled.", fontsize=20, ha='center', style='italic')	

	plt.tight_layout()
	plt.show()