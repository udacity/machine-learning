import pandas as pd
import sys
from feature_importance_and_corr_with_q30_base import make_horizontal_bars

# Loading the dataset contains feature importance and correlation with q30
df = pd.read_csv("../feature_importance_and_corr_with_q30_f_50_r_0.csv")
df.rename(columns={'Unnamed: 0':'feature_name'},inplace=True)

# Extracting the data of Q36,Q38,Q40
df = df.loc[df['feature_name'].isin(['Q36','Q38','Q40'])]

# Sorting values
df.sort_values('corr_with_q30', ascending=True,inplace=True)

# Setting a title of the plot
title = 'Feature importance and correlation with q30 \n' \
        'of Q36,Q38,Q40 from final model with top 50 important features.\n'

# Setting the size of the plot
plot_size_inches = [7.5,5]

# Making a plot
make_horizontal_bars(df,title,plot_size_inches)
