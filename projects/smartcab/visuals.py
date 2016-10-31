###########################################
# Suppress matplotlib user warnings
# Necessary for newer version of matplotlib
import warnings
warnings.filterwarnings("ignore", category = UserWarning, module = "matplotlib")
###########################################

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import ast

def plot_trials(csv):
	""" Plots the data from logged metrics during a simulation."""

	data = pd.read_csv(os.path.join("logs", csv))
	
	# Create additional features
	data['average_reward'] = pd.rolling_mean(data['net_reward'] / (data['initial_deadline'] - data['final_deadline']), 10)
	data['success_rate'] = pd.rolling_mean(data['success']*100, 10)  # compute avg. net reward with window=10
	data['good_actions'] = data['actions'].apply(lambda x: ast.literal_eval(x)[0])
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
	data['gamma'] = data['parameters'].apply(lambda x: ast.literal_eval(x)['g']) 


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
	ax.set_ylabel("Parameter Value")
	ax.set_xlabel("Trial Number")
	ax.set_xlim((1, len(training_data)))
	ax.set_ylim((0, 1.05))

	ax.plot(training_data['trial'], training_data['epsilon'], color='blue', label='Exploration factor')
	ax.plot(training_data['trial'], training_data['alpha'], color='green', label='Learning factor')
	ax.plot(training_data['trial'], training_data['gamma'], color='red', label='Discount factor')

	ax.legend(bbox_to_anchor=(0.5,1.15), fancybox=True, ncol=3, loc='upper center', fontsize=10)


	###############
	### Violations Plot
	###############

	actions = training_data[['trial','minor','major','minor_acc','major_acc']].dropna()
	maximum = actions[['minor','major','minor_acc','major_acc']].values.max()
	
	ax = plt.subplot2grid((6,6), (0,0), colspan=3, rowspan=4)
	ax.set_title("10-Trial Rolling Relative Frequency of Bad Actions")
	ax.set_ylabel("Relative Frequency")
	ax.set_xlabel("Trial Number")

	ax.set_ylim((0, maximum))
	ax.set_xlim((10, len(training_data)))

	ax.set_yticks(np.linspace(0, maximum+0.01, 10))
	#ax.set_yticks(np.round([0, maximum/4, maximum/2, 3*maximum/4, maximum],2))

	ax.plot(actions['trial'], actions['minor'], color='orange', label='Minor Violation')
	ax.plot(actions['trial'], actions['major'], color='red', label='Major Violation')
	ax.plot(actions['trial'], actions['minor_acc'], color='gray', label='Minor Accident', linewidth=2, )
	ax.plot(actions['trial'], actions['major_acc'], color='black', label='Major Accident', linewidth=2)

	ax.legend(loc='upper right', fancybox=True, fontsize=10)


	###############
	### Rolling Success-Rate plot
	###############
	ax = plt.subplot2grid((6,6), (4,0), colspan=4, rowspan=2)
	ax.set_title("10-Trial Rolling Rate of Success")
	ax.set_ylabel("Rate of Success")
	ax.set_xlabel("Trial Number")
	ax.set_xlim((10, len(training_data)))
	ax.set_ylim((-5, 105))
	ax.set_yticks(np.arange(0, 101, 20))
	ax.set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])

	# Create plot-specific data
	trial = training_data.dropna()['trial']
	rate = training_data.dropna()['success_rate']

	# Rolling success rate
	ax.plot(trial, rate, label="Success Rate", color='blue')

	# Best-fit
	ax.plot(np.unique(trial), np.poly1d(np.polyfit(trial, \
		rate, 1))(np.unique(trial)), label="Success Trend", \
		color='green')

	ax.legend(loc='lower right', fancybox=True, fontsize=10)

	###############
	### Test results
	###############

	ax = plt.subplot2grid((6,6), (4,4), colspan=2, rowspan=2)
	ax.axis('off')

	if len(testing_data) > 0:
		safety_rating = testing_data['good_actions'].sum() * 100.0 /(testing_data['initial_deadline'].sum() - testing_data['final_deadline'].sum())
		success_rating = testing_data['success'].sum() * 100.0 / len(testing_data)

		# Write success rate

		ax.text(0.40, .9, "{} testing trials simulated.".format(len(testing_data)), fontsize=14, ha='center')
		ax.text(0.40, 0.7, "Safety Rating:", fontsize=16, ha='center')
		ax.text(0.40, 0.45, "{:.2f}%".format(safety_rating), fontsize=36, ha='center', color='green')
		ax.text(0.40, 0.25, "Success Rating:", fontsize=16, ha='center')
		ax.text(0.40, 0, "{:.2f}%".format(success_rating), fontsize=36, ha='center', color='green')

	else:
		ax.text(0.35, 0.30, "Simulation completed\nwithout testing.", fontsize=24, ha='center', style='italic')	


	plt.tight_layout()
	plt.show()