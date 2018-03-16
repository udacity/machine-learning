import pandas as pd
import numpy as np
import sys
from sklearn.metrics import fbeta_score,precision_score,recall_score,accuracy_score, roc_auc_score


# Loading the dataset
df = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")
true_labels = np.array(df['q30'])


def experiment_metrics():
    # Making a model which always predicts 2
    predictions = []
    for i in range(1000):
        predictions.append(2)
    predictions = np.array(predictions)

    # Testing and storing the result
    print "accuracy: {:.4f}".format(accuracy_score(true_labels, predictions))
    print "precision(micro): {:.4f}".format(precision_score(true_labels, predictions,average='micro'))
    print "recall(micro): {:.4f}".format(recall_score(true_labels, predictions, average='micro'))
    print "f1 score(micro): {:.4f}".format(fbeta_score(true_labels, predictions, 1, average='micro'))

    print "precision(macro): {:.4f}".format(precision_score(true_labels, predictions, average='macro'))
    print "recall(macro): {:.4f}".format(recall_score(true_labels, predictions, average='macro'))
    print "f1 score(macro): {:.4f}".format(fbeta_score(true_labels, predictions, 1, average='macro'))

experiment_metrics()