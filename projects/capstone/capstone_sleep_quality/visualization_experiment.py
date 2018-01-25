import matplotlib.pyplot as plt
import numpy as np
import sys

# Fixing random state for reproducibility
np.random.seed(19680801)

# The matplotlib.rcdefaults() command will restore the standard matplotlib default settings.
plt.rcdefaults()
# returns matplotlib.figure.Figure object and Axes object or array of Axes objects.
fig, ax = plt.subplots()

# Example data
people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')# define people
# seems to return series which contains five values from zero
y_pos = np.arange(len(people))

performance = 3 + 10 * np.random.rand(len(people))
error = np.random.rand(len(people))# just return 5 random values
print performance
sys.exit()
#Make a horizontal bar plot
# xerr specifies error bars, and ecolor specifies the color of the error bars/
ax.barh(y_pos, performance, xerr=error, align='center',
        color='green', ecolor='black')
ax.set_yticks(y_pos) # it specifies y values
ax.set_yticklabels(people) #specify people y tick labels
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Performance')# lbel for x axis
ax.set_title('How fast do you want to go today?')# specifies title

plt.show()