import pandas as pd
import sys
from feature_importance_and_corr_with_q30_base import make_horizontal_bars

# Loading the dataset contains feature importance and correlation with q30
df = pd.read_csv("../feature_importance_and_corr_with_q30_f_50_r_0.csv")
df.rename(columns={'Unnamed: 0':'feature_name'},inplace=True)

# Extracting the data of Q43TOTAL and Q42
df = df.loc[df['feature_name'].isin(['Q43TOTAL','Q42'])]

# Sorting values
df.sort_values('feature_importance', ascending=True,inplace=True)

# Setting a title of the plot
title = 'Feature importance and correlation with q30 \n' \
        'of Q43TOTAL and Q42 from final model with top 50 important features.\n'

# Making a plot
make_horizontal_bars(df,title)
