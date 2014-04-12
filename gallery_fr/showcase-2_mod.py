#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ----------
# Data to be represented

products = ['Vendor A - Product A', 'Vendor A - Product B', 'Vendor A - Product C',
            'Vendor B - Product A', 'Vendor B - Product B', 'Vendor B - Product C',
            'Vendor C - Product A', 'Vendor C - Product B', 'Vendor C - Product C']

values = np.random.uniform(10,60,len(products))

# ----------

# Choose some nice colors
matplotlib.rc('axes', facecolor = 'white')
matplotlib.rc('axes', edgecolor = '#737373')
matplotlib.rc('axes', linewidth = 1)
matplotlib.rc('ytick', direction='out')
matplotlib.rc('xtick', direction='out')
border_size = 0.01
matplotlib.rc('figure.subplot', left=border_size,right=1.0-border_size,bottom=border_size,top=1-border_size)

# Make figure background the same colors as axes
fig = plt.figure(1,figsize=(8,6), facecolor='none')
clf()
# Remove left and top axes spines
axes1 = plt.subplot(1,1,1)


axes1.spines['right'].set_color('none')
axes1.spines['top'].set_color('none')
axes1.xaxis.set_ticks_position('bottom')
axes1.yaxis.set_ticks_position('left')

# a =  axes()

# axes.set_aspect(2.0)
# Adjust yticks to the number of products
plt.xticks(np.arange(len(products)+1), [])

# Set tick labels color to white
for label in axes1.get_yticklabels()+axes1.get_xticklabels():
    label.set_color('white')

# Set tick labels line width to 1
for line in axes1.get_yticklines() + axes1.get_xticklines():
    line.set_markeredgewidth(1)

# Set axes limits
ymin, ymax = 0, len(products)
xmin, xmax = 0, 60
plt.ylim(xmin,xmax*1.25)
plt.xlim(ymin,ymax )
# axes1.set_axes([0.,ymax,xmin,xmax])

# a = axes([0.001, 0.001, 0.999, 0.999],frameon=False)
# Start with blue colormap
cmap = plt.cm.Blues

for i, label in enumerate(products):

    # Alternate band of light background
    if not i%2:
        # p = patches.Rectangle(
        #     (0, i), xmax, 1, fill=True, transform=axes.transData,
        #     lw=0, facecolor='w', alpha=.1)
        # axes.add_patch(p)
        p = patches.Rectangle(
            (i, 0),  1,xmax, fill=True, transform=axes1.transData,
            lw=0, facecolor='w', alpha=.1)
        axes1.add_patch(p)


    # Product name left to the axes
    plt.text( i+0.5, 1, label[0:4], color="white", size=15,
             horizontalalignment='right', verticalalignment='bottom',rotation='vertical',weight='bold',style='italic')

    # Plot the bar with gradient (1 to .65)
    value = values[i]
    X = np.array([0.65,1]).reshape((1,2))
    # width = 0.
    offset = 0.15
    axes1.imshow(X,extent=(i+.25-offset,i+.75+offset,0,value),cmap=cmap, vmin=0, vmax=1,alpha=0.5)

    plt.text( i+0.70,value+2.0, '%.0f' % value, color="gray", size=15,
             horizontalalignment='right', verticalalignment='center',weight='bold',style='italic')

    # Change colormap every 3 values
    # if i >= 2: cmap = plt.cm.Greenss
    # if i >= 5: cmap = plt.cm.Reds

# Set a nice figure aspect
axes1.set_aspect('auto')

# Write some title & subtitle
# plt.text(1, 10.0, "Vendor benchmarks", color="1.0", fontsize=14)
# plt.text(1,  9.7, "(higher is better)", color="0.75", fontsize=10)

# Done
matplotlib.rc('savefig', facecolor = '#6E838A')
plt.show()
