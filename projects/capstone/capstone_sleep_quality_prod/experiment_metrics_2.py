import numpy as np
import sys
from sklearn.metrics import fbeta_score,precision_score,recall_score,accuracy_score, roc_auc_score

def experiment_metrics_2():

    # Making a uniform distribution of 4 classes
    y_true = []
    value_list = [1, 2, 3, 4]
    for i in range(250):
        for value in value_list:
            y_true.append(value)
    y_true = np.array(y_true)

    # Making a model which always predicts 2
    predictions = []
    for i in range(1000):
        predictions.append(2)
    predictions = np.array(predictions)

    # Testing and storing the result
    print "accuracy: {:.4f}".format(accuracy_score(y_true, predictions))
    print "precision(micro): {:.4f}".format(precision_score(y_true, predictions,average='micro'))
    print "recall(micro): {:.4f}".format(recall_score(y_true, predictions, average='micro'))
    print "f1 score(micro): {:.4f}".format(fbeta_score(y_true, predictions, 1, average='micro'))

    print "precision(macro): {:.4f}".format(precision_score(y_true, predictions, average='macro'))
    print "recall(macro): {:.4f}".format(recall_score(y_true, predictions, average='macro'))
    print "f1 score(macro): {:.4f}".format(fbeta_score(y_true, predictions, 1, average='macro'))

experiment_metrics_2()