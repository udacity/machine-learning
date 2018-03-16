import pandas as pd
import sys
from feature_importance_and_corr_with_q30_base import make_horizontal_bars

# Loading the dataset contains feature importance and correlation with q30 of the final model with top 100 important fetures
df = pd.read_csv("../feature_importance_and_corr_with_q30_f_100_r_0.csv")
df.rename(columns={'Unnamed: 0':'feature_name'},inplace=True)

# Extracting the data of q29a, q29b, q29c
df = df.loc[df['feature_name'].isin(['q29a','q29b','q29c'])]

# Sorting values
df.sort_values('feature_importance', ascending=True,inplace=True)

# Setting a title of the plot
title = 'Feature importance and correlation with q30 \n' \
        'of q29a, q29b, q29c from final model with top 100 important features.\n'

# Setting the size of the plot
plot_size_inches = [7.5,4]

# Making a plot
make_horizontal_bars(df,title,plot_size_inches)