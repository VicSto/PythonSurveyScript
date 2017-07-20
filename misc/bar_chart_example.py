import numpy as np
import matplotlib.pyplot as plt

N = 4
men_means = (20, 35, 30, 35)
men_std = (2, 3, 4, 1)

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, men_means, width, color='r', yerr=men_std)

women_means = (25, 32, 34, 20)
women_std = (3, 5, 2, 3)
rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std)

# add some text for labels, title and axes ticks
ax.set_ylabel('Percentage')
ax.set_title('Bar Chart Question vs. Percentage')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('Q1', 'Q2', 'Q3', 'Q4'))

ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))

plt.show()
