import time
from collections import OrderedDict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Metric(object):
    """Named sequence of x and y values, with optional plotting helpers."""

    def __init__(self, name):
        self.name = name
        self.reset()

    def collect(self, x, y):
        self.xdata.append(x)
        self.ydata.append(y)

    def plot(self, ax):
        self.plot_obj, = ax.plot(self.xdata, self.ydata, 'o-', label=self.name)

    def refresh(self):
        self.plot_obj.set_data(self.xdata, self.ydata)

    def reset(self):
        self.xdata = []
        self.ydata = []


class Reporter(object):
    """Collect metrics, analyze and report summary statistics."""

    def __init__(self, metrics=[], live_plot=False):
        self.metrics = OrderedDict()
        self.live_plot = live_plot

        for name in metrics:
            self.metrics[name] = Metric(name)

        if self.live_plot:
            if not plt.isinteractive():
                plt.ion()
            self.plot()

        print "Reporter.__init__(): Initialized with metrics: {}".format(metrics)  # [debug]

    def collect(self, name, x, y):
        if not name in self.metrics:
            self.metrics[name] = Metric(name)
            if self.live_plot:
                self.metrics[name].plot(self.ax)
                self.ax.legend()  # add new metric to legend
            print "Reporter.collect(): New metric added: {}".format(name)  # [debug]
        self.metrics[name].collect(x, y)
        if self.live_plot:
            self.metrics[name].refresh()

    def plot(self):
        if not hasattr(self, 'fig') or not hasattr(self, 'ax'):
            self.fig, self.ax = plt.subplots()
            for name in self.metrics:
                self.metrics[name].plot(self.ax)
            #self.ax.set_autoscalex_on(True)
            #self.ax.set_autoscaley_on(True)
            self.ax.grid()
            self.ax.legend()
        else:
            for name in self.metrics:
                self.metrics[name].refresh()
        self.refresh_plot()

    def refresh_plot(self):
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.draw()

    def show_plot(self):
        if plt.isinteractive():
            plt.ioff()
        self.plot()
        plt.show()

    def summary(self):
        return [pd.Series(metric.ydata, index=metric.xdata, name=name) for name, metric in self.metrics.iteritems()]

    def reset(self):
        for name in self.metrics:
            self.metrics[name].reset()
            if self.live_plot:
                self.metrics[name].refresh()


def test_reporter():
    plt.ion()
    rep = Reporter(metrics=['reward', 'flubber'], live_plot=True)
    for i in xrange(100):
        rep.collect('reward', i, np.random.random())
        if i % 10 == 1:
            rep.collect('flubber', i, np.random.random() * 2 + 1)
            rep.refresh_plot()
        time.sleep(0.01)
    rep.plot()
    summary = rep.summary()
    print "Summary ({} metrics):-".format(len(summary))
    for metric in summary:
        print "Name: {}, samples: {}, type: {}".format(metric.name, len(metric), metric.dtype)
        print "Mean: {}, s.d.: {}".format(metric.mean(), metric.std())
        #print metric[:5]  # [debug]
    plt.ioff()
    plt.show()


if __name__ == '__main__':
    test_reporter()
