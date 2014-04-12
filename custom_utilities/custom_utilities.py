#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy import sqrt
from matplotlib import rcParams
import sys, os, time
from numpy import array,shape,floor,mod
from matplotlib.pylab import clf, ion, plot, legend, xlabel, ylabel, title, grid, draw,xlim,ylim
#from mdbeamer import parse_markdown_to_beamer
from re import search as string_search


def linreg(X, Y):
    """
    Summary
        Linear regression of y = ax + b
    Usage
        a, b, RR = linreg(list, list)
    Returns coefficients to the regression line "y=ax+b" from x[] and y[], and R^2 Value
    """
    if len(X) != len(Y):  raise ValueError, 'unequal length'
    N = len(X)
    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in map(None, X, Y):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    a, b = (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det
    meanerror = residual = 0.0
    for x, y in map(None, X, Y):
        meanerror = meanerror + (y - Sy/N)**2
        residual = residual + (y - a * x - b)**2
    RR = 1 - residual/meanerror
    ss = residual / (N-2)
    Var_a, Var_b = ss * N / det, ss * Sxx / det
    #print "y=ax+b"
    #print "N= %d" % N
    #print "a= %g \\pm t_{%d;\\alpha/2} %g" % (a, N-2, sqrt(Var_a))
    #print "b= %g \\pm t_{%d;\\alpha/2} %g" % (b, N-2, sqrt(Var_b))
    #print "R^2= %g" % RR
    #print "s^2= %g" % ss
    return a, b, RR

def find_string_delimeters(init,last,str1):
	result = string_search(r'{}(.*){}'.format(*[init,last]), str1)
	try: 
		return result.group(1)
	except:
		return ''
def runcmd(cmdstring,**kwargs):
	"""
	silent (def: False) Not verbose
	result (def: False) Switch for command execution result return
	"""
	silent = parse_kwargs('silent',False,**kwargs)
	result_bool = parse_kwargs('result',False,**kwargs)
	if silent==True: print "Executing: "+cmdstring
	result = os.system(cmdstring)
	if ( result_bool == True): 
		return result

def printfile(filename):
	infile = open(filename,'r')
	i = 1;
	for line in infile:
		print "%4i : "% i,line.strip('\n'); i += 1
	infile.close()

def send_email_file(name,namepath):
	emailcmd='thunderbird -compose to="chiquete@lanl.gov",subject="'+name+ \
		'",body="autosent",attachment="file://'+os.path.realpath(namepath)+'"' 
	failure = os.system(emailcmd)
	print "File path : ", namepath

def load_data_file(filename,**kwargs):
	"""
	===============================
	Data file structure as follows:
	===============================
	'''
		# description , ...
		# symbol	  , ...
		# format	  , ...
		# unit		  , ...
		# latex		  , ...
		# end		  , ...
		dummy		  , DATA BLOCK
		# source
	'''
	Note: 
		Footer is not read, only categories written above.
	"""
	#def process_line(line,separator):
	#elements = line.split(separator)
	separator = parse_kwargs('separator',',',**kwargs)
	fopen = open(filename,'r')
	header = []
	for line in fopen:
		if (line.find('#') != -1):
			header.append(line.strip())
		else:
			break
	fopen.close()
	
	desc = []; symbols = []; units = []; eqns = []; formats=[];
	for line in header:
		elements = line.split(separator)
		category = elements[0].lower()
		if (category.find('description') != -1):
			desc = elements[1:]
		elif (category.find('symbol') != -1):
			symbols =  elements[1:]
		elif (category.find('unit') != -1):
			units =  elements[1:]
		elif (category.find('latex') != -1):
			eqns =  elements[1:]
		elif (category.find('format') != -1):
			formats =  elements[1:]
	#print header
	#print desc, symbols
	#print units, eqns
	print formats
	
	fopen = open(filename,'r')
	datas = []
	for line in fopen:
		if (line.find('#') != -1):
			pass
		else:
			elements = line.split(separator)
			formatted_elements = []
			for i in range(1,len(elements)):
				if (formats[i-1]   == 'float'  ):
					formatted_elements.append(float(elements[i]))
				elif (formats[i-1] == 'string' ):
					formatted_elements.append(elements[i])
				elif (formats[i-1] == 'integer'):
					formatted_elements.append(int(elements[i]))
			datas.append(formatted_elements)
	fopen.close()
	return datas,desc,symbols,units,eqns
	
def producefiguretex(strings1,m,n,**kwargs):
	"""
	strings for eps files, m - rows, n - columns
	  The kwargs are as follows:
		         'label' : ['']
		       'caption' : ['']
		      'file_loc' : [None]
		    'label_indv' : [False]
		        'labels' : [None]
	"""
	
	label_str = parse_kwargs('label','',**kwargs)
	caption_str = parse_kwargs('caption','',**kwargs)
	file_name = parse_kwargs('file_loc',None,**kwargs)
	label_indv = parse_kwargs('label_indv',False,**kwargs)
	label_specific = parse_kwargs('labels',None,**kwargs)
	
	labelalphabet_str = ['a','b','c','d','e','f','g','h','i','j','k','l']
	
	if len(strings1) == m*n:
		cs = n*'c';
		tex_output = r"""
			\begin{figure}[t]
			\begin{centering}
			\begin{tabular}{%s} """ % cs
		rows=''
		if n > 1:
			for i in range(m):
				for j in range(n):
					if j == 0: 
						rows = rows+r"""\includegraphics[width = %2.3f\textwidth]{%s} """ % (float(1.0/n),strings1[j+i*n])
					elif j == n-1: 
						rows= rows+ r""" & \includegraphics[width = %2.3f\textwidth]{%s} \\ """ % (float(1.0/n),strings1[j+i*n])
					else:
						rows= rows+ r""" & \includegraphics[width = %2.3f\textwidth]{%s} """ % (float(1.0/n),strings1[j+i*n])
				if (label_indv == True):
					row_label = ''
					for j in range(n-1):
						k = i*n+j
						if (label_specific != None): row_label = row_label + '(%s) %s & ' % (labelalphabet_str[k],label_specific[k])
						else: row_label = row_label + '(%s) & ' % (labelalphabet_str[k])
					k = i*n+n-1
					row_label = row_label + '(%s) \\ ' % (labelalphabet_str[k])
					if (label_specific != None): row_label = row_label + '(%s) %s \\ ' % (labelalphabet_str[k],label_specific[k])
					else: row_label = row_label + '(%s) \\ ' % (labelalphabet_str[k])
					rows = rows+row_label
		elif n == 1:
			rows = rows+r"\includegraphics[width = \textwidth]{%s}" % (strings1[0])
		tex_output = tex_output + r"""%s 
			\end{tabular}
			\caption{%s}\label{%s}
			\end{centering}
			\end{figure} """ % (rows,caption_str,label_str)
		if (file_name != None):
			fopen = open('%s' % (file_name),'w')
			fopen.write(tex_output)
			fopen.close()
		# for line in tex_output:
		print tex_output

		return tex_output
	else:
		print "Error strings not long enough."
		return ''

def beamerslide(type_of, title):
	"""
	Type 1 - Simple slide with itemized list inside block
	Type 2 - Two column slide with itemized list on left and 
	"""

def prepare_powerpoint_plot(**kwargs):
	"""
	Customizes the appearance of plot output from matplotlib to powerpoint style. 
	Keyword variables are 
	The kwargs are as follows:
		          'size' : [12.5]
		            'FS' : [44  ]
		            'XX' : [0.15]
		            'YY' : [0.10]
		   'legend_size' : [FS-4]
		   'linewidth'   : [3.0]
		   aspect_ratio (SIZE,SIZE*aspect )  = parse_kwargs('aspect',1.0,**kwargs)
	
	FS:   'axes.labelsize': FS,
	      'text.fontsize':  FS,
	      'legend.fontsize': FS,
	    ...
	      'xtick.labelsize': FS,
	      'ytick.labelsize': FS,
	"""

	SIZE = parse_kwargs('size',12.5,**kwargs)
	LW = parse_kwargs('linewidth',3.0,**kwargs)
	inches_per_pt = 1.0/72.27    # Convert pt to inch
	fig_width_pt  = int(SIZE/inches_per_pt)
	# golden_mean = (sqrt(5)-1.0)/2.0         # Aesthetic ratio
	aspect_ratio  = parse_kwargs('aspect',1.0,**kwargs)
	fig_width     = fig_width_pt*inches_per_pt  # width in inches
	fig_height    = fig_width*aspect_ratio      # height in inches
	fig_size      = [fig_width+1,fig_height]

	FS = parse_kwargs('FS',  44,**kwargs)
	XX = parse_kwargs('XX',0.15,**kwargs)
	YY = parse_kwargs('YY',0.10,**kwargs)
	LEGEND_FS = parse_kwargs('legend_size', FS-4.0, **kwargs)
	
	params = \
		{ 'backend': 'ps',
		'axes.labelsize': FS,
		'text.fontsize': FS,
		'legend.fontsize': LEGEND_FS,
		'legend.handlelen': 0.01,
		'legend.handletextsep' : 0.01,
		'legend.axespad' : 0.05,
		'legend.frameon': False,
		'lines.linewidth': LW,
		#'legend.borderpad': 0.1,
		'figure.subplot.left': XX,
		'figure.subplot.bottom': YY,
		'figure.subplot.top': 0.95,
		'ytick.major.pad':10,
		'xtick.major.pad':20,
		'xtick.labelsize': FS,
		'ytick.labelsize': FS,
		'text.usetex': False,
		'figure.figsize': fig_size}
	rcParams.update(params)

def preparelatexplot(**kwargs):
	"""
	Customizes the appearance of plot output from matplotlib to LaTeX style. Keyword variables are 
	The kwargs are as follows:
		          'size' : [5.5]
		            'FS' : [18]
		            'XX' : [0.1]
		            'YY' : [0.1]
		   'legend_size' : [FS+2]
	
	FS:   'axes.labelsize': FS,
	      'text.fontsize': FS,
	      'legend.fontsize': FS+2,
	    ...
	      'xtick.labelsize': FS,
	      'ytick.labelsize': FS,
	"""
	SIZE = parse_kwargs('size',5.5,**kwargs)
	
	inches_per_pt = 1.0/72.27    # Convert pt to inch
	fig_width_pt= int(SIZE/inches_per_pt)
	golden_mean = (sqrt(5)-1.0)/2.0         # Aesthetic ratio
	fig_width = fig_width_pt*inches_per_pt  # width in inches
	fig_height = fig_width*golden_mean      # height in inches
	fig_size =  [fig_width+1,fig_height]
	#FS = 18; XX = .1; YY = .1
	FS = parse_kwargs('FS',18,**kwargs)
	XX = parse_kwargs('XX',0.1,**kwargs)
	YY = parse_kwargs('YY',0.1,**kwargs)
	LEGEND_FS = parse_kwargs('legend_size', FS+2, **kwargs)
	
	params = {'backend': 'ps',
	  'axes.labelsize': FS,
	  'text.fontsize': FS,
	  'legend.fontsize': LEGEND_FS,
	  'legend.handlelen': 0.01,
	  'legend.handletextsep' : 0.01,
	  'legend.axespad' : 0.01,
	  'legend.frameon': False,
	  #'legend.borderpad': 0.1,
	  #'figure.subplot.left': XX,
	  #'figure.subplot.bottom': YY,
	  'xtick.labelsize': FS,
	  'ytick.labelsize': FS,
	  'text.usetex': True,
	  'figure.figsize': fig_size}
	rcParams.update(params)
	rcParams.update(params)

def cycle_colors_for_plot(i):
	plot_colors = ['b','g','r','c','m','y','k','w']
	return plot_colors[mod(i,len(plot_colors))]

def index_rank_high_to_low(list1): # move to custompy
	list_ranked_indices = [ i[0] for i in sorted(enumerate(list1),
		key=lambda x:x[1]) ]
	list_ranked_indices = list_ranked_indices[::-1]
	return list_ranked_indices

def index_rank_low_to_high(list1): # move to custompy
	list_ranked_indices = [i[0] for i in sorted(enumerate(list1),
		key=lambda x:x[1])]
	#list_ranked_indices = list_ranked_indices[::-1]
	return list_ranked_indices

def cycle_bw_linestyles(i):
	dashes = ['k-',    # solid line style
		'k--',         # dashed line style
		'k-.',         # dash-dot line style
		'k:',          # dotted line style
		'k.']          # point marker
		
	return dashes[mod(i,len(dashes))]

def format_python_double(float1):
	return ('{:18.16e}'.format(float1)).replace('e','d')

def plot_movie(x,t,u,NN,**kwargs):
	"""
	     x  | Spatial coordinate vector,  len (Nx)
	     t  | Temporal coordinate vector, len (Nt)
	  data  | The data in matrix form,    len (Nt,Nx)
	    NN  | integer giving interval of plotting.
	
	"""
	N,M = shape(u)
	clf()
	ion()
	line, = plot(x,u[0,:],'k-',label=parse_kwargs('label','$Wave$ $equation:$ $BW$',**kwargs),
		linewidth=2)
	plot(x,u[0,:],color='gray',alpha=0.75)
	line.axes.set_ylim(parse_kwargs('miny',-1,**kwargs),parse_kwargs('maxy',1,**kwargs))
	legend(loc=0)
	xlabel(parse_kwargs('xlabel','$x$',**kwargs))
	ylabel(parse_kwargs('ylabel','$u$',**kwargs))
	grid(True)
	for i in range(0,N,N/NN):
		title('$t={}$'.format(t[i]))
		line.set_ydata(u[i,:])
		plot(x,u[i,:],color='gray',alpha=0.2)
		xlim([min(x),max(x)])
		draw()
	line.set_ydata(u[-1,:])
	
	title('$t={}$'.format(t[-1]))

def f_p_dbl(float1):
	return format_python_double(float1)

def parse_kwargs(key,default_value,**kwargs):
	if kwargs.has_key(key):
		value1 = kwargs.get(key)
		#print "Empty=",empty
	else: 
		value1 = default_value
	return value1
	
def rld(filename, **kwargs):
	"""
	  The kwargs are as follows:
		           'sep' : [None]
		        'header' : [False]
		          'data' : [True]
	"""
	file1 = open(filename,'r')
	separator = parse_kwargs('sep',None,**kwargs)
	header_bool = parse_kwargs('header',False,**kwargs)
	data_bool = parse_kwargs('data',True,**kwargs)
	# Nold = Nnew
	i = 0
	#header = ['a']
	data	= []
	header  = []
	if ( data_bool == True):
		for line1 in file1:
			#if ( i == 0): print line1,line1[0]
			if (line1.strip()[0] != '#'):
				#print line1
				if (separator == None):
					elements1=line1.split()
				else:
					elements1=line1.split(',')
				datanum=[]
				Nnew = len(elements1)
				if (i == 0):
					Nold = Nnew
				if ( Nnew != Nold) :
					break
				for element1 in elements1:
					datanum.append( float(element1) )
				data.append(datanum)
				Nold = Nnew
				i = i + 1
			else:
				header.append(line1.strip().strip('#'))
		if ( header_bool == False ): 
			return array(data)
		else:
			if ( header == []): print "No header to data file"
			return array(data), header
	else:
		for line1 in file1:
			#if ( i == 0): print line1,line1[0]
			if (line1.strip()[0] != '#'):
				pass
			else:
				header.append(line1.strip().strip('#'))
		if ( header == []): print "No header to data file"
		return header

def call_default_latex_plot_style():
	preparelatexplot(size=15,FS=27,legend_size= 20)

def create_latex_figure(filenm,frac,caption,label,**kwargs):
	filename = parse_kwargs('filename',None,**kwargs)
	tex_output = []
	tex_output.append('\\begin{figure}[t]')
	tex_output.append('\t\\centering')
	tex_output.append('\t\includegraphics[width = {}\\textwidth]{{{}}}'.format( 
		frac,filenm) )
	tex_output.append('\t\caption{{{}}}\label{{{}}}'.format(*[caption,label]))
	tex_output.append('\end{figure}')

	if ( filename != None): fopen = open(filename,'w')
	for line in tex_output:
		print line
		if ( filename != None): fopen.write(line+'\n')
	if ( filename != None): fopen.close()
	return tex_output

def create_latex_table(table_entries,Ncol,Nrow,header,justification,caption,label,**kwargs):
	def create_row(row):
		Ncol = len(row)
		return "\t\t"+(("{} & "*(Ncol-1))+"{} \\\ ").format(*row)
	filename = parse_kwargs('filename',None,**kwargs)
	verbose  = parse_kwargs('verbose', True, **kwargs )
	subheader = parse_kwargs('subheader', None, **kwargs )
	hlines    = parse_kwargs('hlines',None,**kwargs)
	
	for table_element in table_entries:
		if ( Ncol != len(table_element) ):
			print "Table elements (",len(table_element),") do not match Ncol = ", Ncol
			break
	if ( header        == None        ): header = ['']*Nrow
	if ( justification == None        ): justification = 'c'*Ncol
	lines = []
	justify = {}
	if ( caption != None or label != None ):
		lines.append( "\\begin{table}[H]")
		lines.append( "\t \centering")
	lines.append( "\t \\begin{{tabular}}{{ {} }}".format(justification) )
	# lines.append( "\t\t \hline")
	lines.append( create_row(header) )
	if ( subheader != None): lines.append( create_row(subheader) )
	lines.append( "\t\t \hline")
	for i in range(Nrow):
		if ( hlines != None ):
			if ( i in hlines): lines.append( "\t\t \hline")
		lines.append( create_row(table_entries[i]) )
	lines.append( '\t \\end{tabular}')
	if ( caption != None or label != None ):
		lines.append( '\caption{{ {} }}\label{{{}}}'.format(*[caption,label]))
		lines.append( "\\end{table}")
	if ( filename != None): fopen = open(filename,'w')
	for line in lines: 
		if ( verbose == True ): print line
		if ( filename != None): fopen.write(line+'\n')
	if ( filename != None): fopen.close()
	return lines

def make_no_frame_legend(**kwargs): # move to custompy
	leg = legend(**kwargs);
	leg.draw_frame(False);

def scan_for_kwargs(function,**kwargs):
	function_str = parse_kwargs('func',(str(function).split()[1]).strip(),**kwargs)
	#print function_str
	runcmd('grep -n "def %s(" *.py > temp.txt' % function_str)
	fopen = open('temp.txt','r')
	files, lines, func_declares = [], [], []
	for line in fopen:
		splitline1= line.split(':')
		files.append(splitline1[0])
		lines.append(splitline1[1])
		func_declares.append(splitline1[2])
	fopen.close()
	
	for i in range(len(files)):
		function_lines = []
		fopen = open(files[i],'r')
		liness = fopen.readlines()
		for line in liness[int(lines[i]):]:
			if (line[0] == '\t' or line[0] == ' '):
				function_lines.append(line.strip())
			else:
				break
		fopen.close()
		
		print "  File: ", files[i], "func :", function_str
		print "  The kwargs are as follows:"
		j  = 0
		for line in function_lines:
			if ( line.find('parse_kwargs') != -1 and line.find('#') == -1):
				str1 = (line.split('parse_kwargs')[1]).split(',')
				print "\t\t %15s : [%s]" % (str1[0][1:],str1[1])
				j += 1
	return 

def run_fortran_program(files,output,**kwargs):
	"""
	  The kwargs are as follows:
		       'folder'  : [None]
		       'logfile' : [None]
		       'timeout' : [None]
		        'repeat' : [False]
		        'result' : [False]
		        'debug'  : [False]
	"""
	
	original_folder = os.path.realpath('./')
	folder  	    = parse_kwargs('folder' ,None,**kwargs)
	logfile 	  	= parse_kwargs('logfile',None,**kwargs)
	timeout 		= parse_kwargs('timeout',None,**kwargs)
	repitition		= parse_kwargs('repeat',False,**kwargs)
	result_bool     = parse_kwargs('result',False,**kwargs)
	#print "resc = ", result_bool
	file1 = ''
	for file2 in files:
		file1 += ' '+file2
	if ( folder != None):
		os.chdir(folder)
	cmd = 'gfortran %s -o %s -w' % (file1,output) 
	
	print len(cmd)*"="
	print cmd
	print "		Repeat=", repitition
	print len(cmd)*"*"
	
	if ( repitition == True): 
		compile_result = os.system(cmd); compile_result = os.system(cmd)
	else:
		compile_result = os.system(cmd)
	 
	if ( compile_result == 0 ):
		if ( logfile == None ): 
			cmd = './{}'.format(output)
		else:
			# cmd = 'unbuffer hexdump {} | ./{}'.format(*[logfile,output])
			cmd = 'unbuffer ./{} | tee {}'.format(*[output,logfile])
		if ( timeout == None): 
			exe_result = runcmd(cmd,result=result_bool)
		else:
			exe_result = timeout_command(cmd,timeout)
	else:
		print "***************** Compilation failed *******************"
	os.chdir(original_folder)
	
	if ( result_bool == True):
		return [compile_result, exe_result]

def timeout_command_subprocess(command, timeout):
	"""call shell-command and either return its output or kill it
	if it doesn't normally exit within timeout seconds and return None"""
	import subprocess, datetime, os, time, signal
	
	cmd = command.split(" ")
	print "Command : ", command
	start = datetime.datetime.now()
	process = subprocess.Popen(cmd, stdout=None, stderr=subprocess.PIPE)
	while process.poll() is None:
		time.sleep(0.1)
		now = datetime.datetime.now()
		if (now - start).seconds > timeout:
			process.terminate()
			print "		Program did not Finish"
			return 1
			return None
	return 0

def timeout_command(command,timeout):
	"""
	Input command (string)
		  timeout (float or integer)
	Relies on perl.
	"""
	perl_timeout_command = "perl -e 'alarm shift @ARGV; exec @ARGV'"
	cmd = "{} {} {}".format(*[ perl_timeout_command, timeout, command ])
	runcmd(cmd)

def readlivedata(filename):
	"""
	 Program reads an array of data that has MxN dimensions. Error if unfinished or whatever. 
	"""
	from scipy.io.array_import import read_array
	from numpy import shape
	#f = 
	data = read_array(filename)
#	try Nt, Nx = shape(data)
		
	#m = data[0,1:N_x+1]
	#t = data[1:Nt,0]
	#f = data[1:Nt,1:N_x];
	#f = f.T
	return data

def format_time(time_elapsed,**kwargs):
	raw_bool = parse_kwargs('raw',False,**kwargs)
	if ( raw_bool == False ):
		if ( time_elapsed <= 1.0):
			#print "Elapsed time is %1.4f" % (time_elapsed)
			return "Elapsed time is %5.3f" % (time_elapsed)
		else:
			labels = [ 'days','hours', 'minutes', 'seconds' ]
			values = [ 60*60*24,60*60,60,1 ] 
			#print values
			str_time = 'Elapsed time : '
			total_time = time_elapsed
			for i in range(len(values)):
				#print round(values[i],0),labels[i]
				if (floor(total_time/values[i]) != 0.):
					str_time = str_time + str( floor(total_time/values[i]) ) + ' ' + labels[i] + ' ' 
				total_time = total_time - values[i]*floor(total_time/values[i])
			return str_time
	else:
		return str(time_elapsed)

def print_matrix(MM,filename):
	fopen = open(filename,'w')
	N,M = shape(MM)
	for i in range( N ):
		row = ''
		for j in range( M-1 ):
			row = row+"%3.16e" % ( MM[i,j] )+'\t'
		row = row + "%3.16e" % ( MM[i,M-1] )+'\n'
		fopen.write(row)
	fopen.close()

def time1():
	global _time_init
	_time_init = time.time()

def time2(**kwargs):
	global _time_init
	print format_time(time.time()-_time_init,**kwargs)
	return time.time()-_time_init

def find_functions_in_file(file1):
	file1open = open(file1,'r')
	i = 1
	for line in file1open.readlines():
		if (line[0:3] == 'def'):
			print "Line = %4i : %s" % (i, (line.split('def')[1]).strip())
		i += 1

def print_title_output(title_str,**kwargs):
	"""
	The kwargs are as follows:
		         'level' : [0]
		         'type1' : ['body']
	"""
	level = parse_kwargs('level',0,**kwargs)
	type1 = parse_kwargs('type1','body',**kwargs)
	if (type1 == 'Begin'):
		N = len("%s= Beginning of %s %10s" % (level*'\t',title_str, "="))
		print "%s%s" % (level*'\t',"="*N)
		print "%s= Beginning of %s %10s" % (level*'\t',title_str, "=")
		print "%s%s" % (level*'\t',"="*N)
	elif (type1 == 'End'):
		N = len("%s= End of %s %10s" % (level*'\t',title_str, "="))+6
		print "%s%s" % (level*'\t',"="*N)
		print "%s= End of %s %10s" % (level*'\t',title_str, "=")
		print "%s%s" % (level*'\t',"="*N)
	elif (type1 == 'topbody'):
		print "%s %s" % (level*'\t',title_str)
	elif (type1 == 'subtitle'):
		N = len("%s= Beginning of %s %10s" % (level*'\t',title_str, "="))
		#print N
		level=level+1
		N1 =(N-len(title_str))/2
		print "%s%s%s%s" % (level*'\t','*'*N1,title_str,'*'*N1)
	else:
		level=level+1
		print "%s %s" % (level*'\t',title_str)

if __name__ == "__main__":
    print "Modules loaded"
    
    #runcmd('sudo cp ~/shared/CustomPython/custom_utilities.py /usr/lib/python2.6/')
    #runcmd('sudo cp ~/shared/CustomPython/custom_utilities.pyc /usr/lib/python2.6/')
    #from sys.
    #fib(int(sys.argv[1]))
