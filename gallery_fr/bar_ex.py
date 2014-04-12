from pylab import *

def basic():
	n = 12
	X = np.arange(n)
	Y1 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)
	Y2 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)

	axes([0.025,0.025,0.95,0.95])
	bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
	bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

	for x,y in zip(X,Y1):
	    text(x+0.4, y+0.05, '%.2f' % y, ha='center', va= 'bottom')

	for x,y in zip(X,Y2):
		text(x+0.4, -y-0.05, '%.2f' % y, ha='center', va= 'top')

	xlim(-.5,n), xticks([])
	ylim(-1.25,+1.25), yticks([])

	# savefig('../figures/bar_ex.png', dpi=48)
	show()

def custom_single_bars(X,Y1,ymax,ymin,label_loc,**kwargs):
	def gradient_bar(XX,YY,**kwargs):
		alpha_here = parse_kwargs('alpha',1.0,**kwargs)
		for i, x in enumerate(XX):
			value = YY[i]
			X = np.array([1,0.65]).reshape((1,2))
			# width = 0.
			offset = 0.15
			if (value < 0.0 ):
				# offset = -0.15
				cmap = plt.cm.Reds
			else:
				cmap = plt.cm.Blues
			
			plt.imshow(X,extent=(x+.25-offset,x+.75+offset,0,value),
				cmap=cmap, vmin=0, vmax=1,aspect='auto',alpha=alpha_here)
	# n = 12
	# X = np.arange(n)
	# Y1 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)
	# Y2 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)

	# axes([0.025,0.025,0.95,0.95])
	# axes([0.0,0.0,1.,1.])
	
	gradient_bar(X,Y1,**kwargs);
	# bar(X, Y1, facecolor='red', edgecolor='gray', alpha=1.0)

	scaleX = 0.01*abs( (max(X)-min(X)) )
	scaleY = 0.01*abs( (max(Y1)-min(Y1)) )
	#bar(X, -Y2, facecolor='gray', edgecolor='white')

	for x,y in zip(X,Y1):
		if ( y < 0 ):
			scaleY1 = -25*scaleY
		else:
			scaleY1 = scaleY
		text(x+3.5*scaleX, y+scaleY1, '%.0f' % abs(y), ha='center', va= 'bottom',fontsize=20,\
			weight='bold',style='italic',alpha=0.75)

	#for x,y in zip(X,Y2):
	#	text(x+0.4, -y-0.05, '%.2f' % y, ha='center', va= 'top')
	# ymin = -60*scaleY + min(Y1)
	# , ymax, max(Y1)*2.0
	#ymin, ymax = 0.0, max(Y1)*2.0
	# ymin = 0.0
	xlim( min(X)-1*scaleX,max(X)+10*scaleX), xticks([])
	ylim(ymin,ymax), yticks([])
	for x in X:
		text(x + 1 -1.0*scaleX,label_loc,str(x),color='black',rotation='vertical',alpha=0.25,
			fontsize=20,style='italic',weight='bold',horizontalalignment='right')
	# savefig('../figures/bar_ex.png', dpi=48)
	show()

def gradient_bars_example(producs,values):
	import numpy as np
	import matplotlib
	import matplotlib.pyplot as plt
	import matplotlib.patches as patches

	# ----------
	# Data to be represented

	# products = ['Vendor A - Product A', 'Vendor A - Product B', 'Vendor A - Product C',
	#             'Vendor B - Product A', 'Vendor B - Product B', 'Vendor B - Product C',
	#             'Vendor C - Product A', 'Vendor C - Product B', 'Vendor C - Product C']

	# values = np.random.uniform(10,60,len(products))

	# ----------

	# Choose some nice colors

	matplotlib.rc('axes', facecolor = 'none')
	matplotlib.rc('axes', edgecolor = '#737373')
	matplotlib.rc('axes', linewidth = 1)
	matplotlib.rc('ytick', direction='out')
	matplotlib.rc('xtick', direction='out')
	border_size = 0.01
	matplotlib.rc('figure.subplot', left=border_size,right=1.0-border_size,bottom=border_size,top=1-border_size)

	# Make figure background the same colors as axes
	# fig = plt.figure(1,figsize=(8,6), facecolor='none')
	# clf()
	# Remove left and top axes spines

	axes1 = plt.subplot(1,1,1)
	# axes1.set_axes([0.001, 0.001, 0.999, 0.999],frameon=False)
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

	# 
	# Start with blue colormap
	cmap = plt.cm.Blues

	for i, label in enumerate(products):

	    # Alternate band of light background
	    if not i%2:
	        # p = patches.Rectangle(
	        #     (0, i), xmax, 1, fill=True, transform=axes.transData,
	        #     lw=0, facecolor='w', alpha=.1)
	        # axes.add_patch(p)
	        # p = patches.Rectangle(
	        #     (i, 0),  1,xmax, fill=True, transform=axes1.transData,
	        #     lw=0, facecolor='w', alpha=.1)
	        # axes1.add_patch(p)
	        pass


	    # Product name left to the axes
	    plt.text( i+0.5, 1, label[0:4], color="white", size=15,
	             horizontalalignment='right', verticalalignment='bottom',rotation='vertical',weight='bold',style='italic')

	    # Plot the bar with gradient (1 to .65)
	    value = values[i]
	    X = np.array([0.65,1]).reshape((1,2))
	    # width = 0.
	    offset = 0.15
	    axes1.imshow(X,extent=(i+.25-offset,i+.75+offset,0,value),cmap=cmap, vmin=0, vmax=1,alpha=0.75)

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

#clf()
#X1= linspace(1997,2011,15)
#Y1=linspace(40,56,15)
#custom_single_bars(X1,Y1,15)
