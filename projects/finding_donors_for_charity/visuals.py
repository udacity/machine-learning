###########################################
# Suppress matplotlib user warnings
# Necessary for newer version of matplotlib
import warnings
warnings.filterwarnings("ignore", category = UserWarning, module = "matplotlib")
###########################################

import matplotlib.pyplot as pl
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from time import time
from sklearn.metrics import f1_score, accuracy_score

def train_predict(learner, sample_sizes, X_train, y_train, X_test, y_test): 
    """
    Function takes as input a supervised learner 'learner' with a sample
    size 'sample_size' at most the size of 'X_train', and constructs the
    learner, and computes statistics on both training and testing.
    
    inputs:
      - learner: A supervised learner
      - sample_sizes: a list of sample sizes at most the size of X_train
      - X_train: training set of the features
      - y_train: training set of the labels
      - X_test: testing set of the features
      - y_test: testing set of the labels
      
    outputs:
      - results: calculated statistics to be used in a visualization
    """
    
    print "Building {} models. . .".format(learner.__class__.__name__)
    
    # Construct a dictionary to hold all relevant information
    results = {'pred_time' : [], 'train_time' : [], 'accuracy' : [], 'f1' : []}
    
    # For each sample size
    for i, sample in enumerate(sample_sizes):
        
        # Store the result of training time
        start = time()
        learner.fit(X_train[:sample], y_train[:sample])     
        results['train_time'].append(time() - start)
        
        # Store the result of prediction time
        start = time()
        predictions = learner.predict(X_test)
        results['pred_time'].append(time() - start)
        
        # Compute accuracy on test set
        results['accuracy'].append(accuracy_score(y_test, predictions))
        
        # Compute F1 on the test set
        results['f1'].append(f1_score(y_test, predictions))
        
    # Return the results
    return results

def distribution(data, transformed = False):
    """
    Visualization code for displaying skewed distributions of features
    """
    
    # Create figure
    fig = pl.figure(figsize = (11,5));

    # Skewed feature plotting
    for i, feature in enumerate(['capital-gain','capital-loss']):
        ax = fig.add_subplot(1, 2, i+1)
        ax.hist(data[feature], bins = 10, color = '#00A0A0')
        ax.set_title("'%s' Feature Distribution"%(feature), fontsize = 14)
        ax.set_xlabel("Values")
        ax.set_ylabel("Frequency of Occurence")

    # Plot aesthetics
    if transformed:
        fig.suptitle("Log-transformed Distributions of Continuous Census Data Features", \
            fontsize = 16, y = 1.03)
    else:
        fig.suptitle("Skewed Distributions of Continuous Census Data Features", \
            fontsize = 16, y = 1.03)
    
    fig.tight_layout()
    fig.show()


def evaluate(results, accuracy, f1):
    """
    Visualization code to display results of various learners.
    
    inputs:
      - learners: a list of supervised learners
      - stats: a list of dictionaries of the statistic results from 'train_predict()'
      - accuracy: The score for the naive predictor
      - f1: The score for the naive predictor
    """
  
    # Create figure
    fig, ax = pl.subplots(2, 2, figsize = (11,7))

    # Constants
    bar_width = 0.3
    colors = ['#A00000','#00A0A0','#00A000']
    
    # Super loop to plot four panels of data
    for k, learner in enumerate(results.keys()):
        for j, metric in enumerate(['train_time', 'pred_time', 'accuracy', 'f1']):
            for i in np.arange(3):
                
                # Creative plot code
                ax[j/2, j%2].bar(i+k*bar_width, results[learner][i][metric], width = bar_width, color = colors[k])
                ax[j/2, j%2].set_xticks([0.45, 1.45, 2.45])
                ax[j/2, j%2].set_xticklabels(["1%", "10%", "100%"])
                ax[j/2, j%2].set_xlabel("Training set size")
                ax[j/2, j%2].set_xlim((-0.1, 3.0))
    
    # Add unique y-labels
    ax[0, 0].set_ylabel("Training time (in seconds)")
    ax[0, 1].set_ylabel("Prediction time (in seconds)")
    ax[1, 0].set_ylabel("Accuracy score on Testing Set")
    ax[1, 1].set_ylabel("F1 score on Testing Set")
    
    # Add horizontal lines for naive predictors
    ax[1, 0].axhline(y = accuracy, xmin = -0.1, xmax = 3.0, linewidth = 1, color = 'k', linestyle = 'dotted')
    ax[1, 1].axhline(y = f1, xmin = -0.1, xmax = 3.0, linewidth = 1, color = 'k', linestyle = 'dotted')

    # Create patches for the legend
    patches = []
    for i, learner in enumerate(results.keys()):
        patches.append(mpatches.Patch(color = colors[i], label = learner))
    pl.legend(handles = patches, bbox_to_anchor = (-.065, -.2), \
               loc = 'upper center', borderaxespad = 0., ncol = 3, fontsize = 'x-large')
    
    # Aesthetics
    pl.suptitle("Performance Metrics for Three Supervised Learning Models", fontsize = 16, y = 1.03)
    pl.tight_layout()
    pl.show()
    

def feature_plot(importances, X_train, y_train):
    
    # Display the five most important features
    indices = np.argsort(importances)[::-1]
    columns = list(X_train)[:5]
    values = importances[indices][:5]

    # Creat the plot
    fig = pl.figure(figsize = (11,7))
    pl.title("Five Most Relevant Features For Predicting Income", fontsize = 16)
    pl.bar(np.arange(5), values, align="center", color = '#00A000')
    pl.xticks(np.arange(5), columns)
    pl.xlim((-0.5, 4.5))
    pl.ylabel("Normalized Feature Importance Weight", fontsize = 12)
    pl.xlabel("Feature", fontsize = 12)
    pl.show()  