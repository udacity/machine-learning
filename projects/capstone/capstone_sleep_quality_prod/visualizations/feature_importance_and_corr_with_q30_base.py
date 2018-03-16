import matplotlib.pyplot as plt
import numpy as np


# The function which makes multiple horizontal bars plot which represent feature importance and .
def make_horizontal_bars(df,title,plot_size_inches =[7.5, 7.5], plots_adjust=[0.75, 0.25, 0.65]):

    # Making indent of bars
    ind = np.arange(len(df)) * 2

    # Setting width of bars
    width = 0.4

    # Creating a figure and a setting of subplots
    fig, ax = plt.subplots()

    # Setting the size of a plot
    fig.set_size_inches(plot_size_inches[0], plot_size_inches[1])

    # Making another y axis.
    ax2 = ax.twiny()

    # Making a bar represents feature importance
    rects2 = ax2.barh(ind + width, df['feature_importance'], width, color='red',
                      label='Feature importance')

    # Making a bar represents correlation with q30
    rects1 = ax.barh(ind, df['corr_with_q30'], width, color='green', label='Correlation with q30')

    # Setting ticks of feature importance bar
    ax2.set(yticks=ind + (width /2), yticklabels=df['feature_name'], xlabel='Feature importance',
            xlim=[-0.05, 0.05])

    # Setting ticks of correlation bar
    ax.set(xlabel='Correlation with q30', xlim=[-0.5, 0.5])

    # Setting a legend
    plt.legend(loc="upper center", handles=[rects2, rects1], labels=["Feature importance", "Correlation with q30"],
               bbox_to_anchor=(1.35, 1), fancybox=True)

    # Adjusting shape of a plot
    plt.subplots_adjust(top=plots_adjust[0], left=plots_adjust[1], right=plots_adjust[2])

    # Setting a title
    plt.title(title, y=1.08)

    # Showing plot
    plt.show()