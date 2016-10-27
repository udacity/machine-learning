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

def plot_trials(csv):

	data = pd.read_csv(os.path.join("logs", csv), index_col=0, header=0)
	data['avg_net_reward'] = pd.rolling_mean(data['net_reward'], 5)  # compute avg. net reward with window=10

	testing = False
	xlim = 110 if testing else 100

	plt.figure(figsize=(12,8))

	### First plot - rolling net reward
	ax1 = plt.subplot2grid((2,2), (0,0), colspan=2)
	ax1.set_title("Net Reward 5-trial Rolling Mean")
	ax1.set_ylabel("Mean Net Reward")
	ax1.set_xlabel("Trial")
	ax1.set_xlim((5,xlim))
	ax1.set_xticks(np.arange(5, xlim+1, 5))

	ax1.plot(data['avg_net_reward'])

	### Second plot - net reward distribution

	# Data

	ax2 = plt.subplot2grid((2,2), (1,0))
	ax2.set_title("Distribution of Net Reward Across 100 Trials")
	ax2.set_ylabel("Frequency")
	ax2.set_xlabel("Net Reward")


	ax2.hist(data['net_reward'], bins=20, align = 'left', normed = 1, facecolor = 'blue')
	ax2.axvline(x = 0, ymin = 0, ymax = 1, linewidth = 2, color = 'black', linestyle = 'dashed')

	ax2.set_xlim(ax2.get_xlim())

	ax2.axvspan(0,ax2.get_xlim()[1], facecolor='green', alpha=0.7)
	ax2.axvspan(ax2.get_xlim()[0], 0, facecolor = 'red', alpha = 0.7)

	ax2.hist(data['net_reward'], bins=20, align = 'left', normed = 1, facecolor = 'blue')
	ax2.axvline(x = 0, ymin = 0, ymax = 1, linewidth = 2, color = 'black', linestyle = 'dashed')


	### Third plot - successes and failures

	# Data
	index = np.arange(0,4)
	bar_width = 0.40

	successes = []
	failures = []
	for i in [0, 25, 50, 75]:
		trials = data[i:i+25]['success'].value_counts()
		s = 0
		if 1 in trials.keys():
			s = trials[1]
		f = 25 - s
		successes.append(s)
		failures.append(f)

	ax3 = plt.subplot2grid((2,2), (1, 1))
	ax3.set_title("Rate of Success and Failure Per 25 Trials")
	ax3.set_ylabel("Occurences")
	ax3.set_xlabel("Trial Completion by Deadline")
	ax3.set_xlim((-0.05,3.85))
	ax3.set_ylim((0, np.amax(successes) + 10))
	ax3.set_xticks(index + bar_width)
	ax3.set_xticklabels(['Trial 1 to 25', 'Trial 26 to 50', 'Trial 51 to 75', 'Trial 76 to 100'])

	success = ax3.bar(index, successes , width=bar_width, color='green')
	failure = ax3.bar(index + bar_width, failures, width=bar_width, color='red')

	ax3.legend((success, failure), ('Success','Failure'), framealpha = 0.8)

	plt.tight_layout()
	plt.show()