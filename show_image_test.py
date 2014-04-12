def load_img():
	import matplotlib.pyplot as plt
	import matplotlib.image as mpimg
	import numpy as np
	img = mpimg.imread('logos/Arsenal-icon.png')
	imgplot = plt.imshow(img,alpha=0.1)

def load_image_and_superimpose_plot()
	import Image
	import numpy as np
	import matplotlib.mlab as mlab
	import matplotlib.pyplot as plt

	
	figure(1,frameon=False)
	clf()
	#contour plot test data:
	#a = axes([0.01, 0.01, 0.99, 0.99])

	# plt.figure()

	# im.size[0]=im.size[0]/2.0

	# print im.size[0], im.size[1]/2
	# axes

	a = axes([0.0, 0.0, 1, 1],frameon=False)
	im = Image.open('logos/Arsenal-icon.png')
	plt.imshow(im, origin='lower',alpha=0.1)
	xticks([])
	yticks([])

	a = axes([0.001, 0.001, 0.999, 0.999],frameon=False)
	delta = 0.025
	x = np.arange(-3.0, 3.0, delta)
	y = np.arange(-2.0, 2.0, delta)
	X, Y = np.meshgrid(x, y)
	Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
	Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
	# difference of Gaussians
	Z = 10.0 * (Z2 - Z1)

	#rescale contour plot:
	# XX = im.size[0]*2
	# YY = im.size[1]*2
	# X = X - np.min(X)
	# X = Xdd * XX / np.max(X)
	# Y = Y d- np.min(Y)
	# Y = Y * YY / np.max(Y)
	# plt.contour(X, Y, Z, 20,bg_color='None')

	# plt.show()

	# fig = plt.figure(num=None, figsize=(5, 10), dpi=80, facecolor='y', edgecolor='k')
	# ax = fig.add_subplot(111)
	a.set_axis_bgcolor("none")
	plot(x, x**2 + 2, 'b-o',markersize=1.0)
	xticks([])
	yticks([])
	savefig('test.png')

# import numpy as np
# import matplotlib.pyplot as plt

# plt.figure(figsize=(1,5))
# plt.axis([0,1,-50,200])
# plt.xticks([])
# plt.yticks([-40,180])
# plt.bar(left=0, width=1, bottom=-40, height=220, color='r')
# plt.subplots_adjust(left=0.4, right=0.8)
# plt.savefig("test.png")
