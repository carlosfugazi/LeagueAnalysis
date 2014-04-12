execfile('applications_on_parsed_data.py')


def get_results_distribution_divided(master_list_file,N):
	
	# fig= figure(1,figsize=(20,10))
	fig_height = 10
	fig_width  = 14
	params = {'backend': 'tk',
	  # 'axes.labelsize': FS,
	  # 'text.fontsize': FS,
	  'font.family':'serif',
	  # 'font.sans-serif':'Verdana',
	  'font.style':'italic',
	  'legend.fontsize': 20,
	  # 'legend.handlelen': 0.01,
	  # 'legend.handletextsep' : 0.01,
	  # 'legend.axespad' : 0.01,
	  # 'legend.frameon': False,
	  #'legend.borderpad': 0.1,
	  #'figure.subplot.left': XX,
	  #'figure.subplot.bottom': YY,
	  # 'xtick.labelsize': FS,
	  # 'ytick.labelsize': FS,
	  # 'text.usetex': True,
	  'figure.figsize': [fig_width+1,fig_height]}
	figure(1); clf()
	rcParams.update(params)
	rcParams.update(params)
	
	fopen = open(master_list_file,'r');
	league_files = [ line.strip() for line in fopen.readlines() ]
	print "Total number of leagues: ", len(league_files)
	years = []
	unique_teams_in_top_N = []
	wins, draws, loses = [], [], []
	total_games = []
	plot_league_team_logo(parse_dict(league_files[0])['Logo file'],
		'logo/drawing_nograd.png',[0.45,0.15,0.65,0.65],[0.0,0.20,0.65,0.65])
	points = []
	a = axes([0.001, 0.001, 0.999, 0.999],frameon=False)
	top_division = []
	tp_years = []
	for file1 in league_files:
		dict_ = get_league_table(False,file1)
		dict_league = parse_dict(file1)
		Nteams = len(dict_.keys())
		point_breakdown = [0]*N
		N_games = max(dict_league['Matchday'])
		pieces = range(1,1+20,N);
		
		for i in range(N):
			for key in dict_:
				if ( dict_[key]['league position'] > (i)*(Nteams)/N and \
					dict_[key]['league position'] <= (i+1)*(Nteams)/N ):
					point_breakdown[i]  += dict_[key]['points']
					if (i == 0):
						top_division.append(key)
						tp_years.append(dict_league['Year2'])
		points.append( point_breakdown )
		years.append(dict_league['Year2'])
	
	parray= array(points)
	kwargs_for_points = {'markerfacecolor':'w','markeredgewidth':2,'linewidth':6,
		'markersize':10}
	colors= ['b','g','r','k','m']
	for i in range(N):
		# label_str = 'Pos. {}-{}'.format(1+i*Nteams/N,(i+1)*Nteams/N)
		label_str = '{}-{}'.format(1+i*Nteams/N,(i+1)*Nteams/N)
		a,b,RR = linreg(array(years)-min(years),parray[:,i] )
		print "Trend slope = {:.2f} pts/year with fit r**2 = {:.3f}".format(a,RR)
		plot(years, b+a*(array(years)-min(years)), '--'+colors[i],linewidth=2)
		plot(years,parray[:,i],colors[i]+'o-',label=label_str,**kwargs_for_points)
		# text(years[-1],parray[-1,i]+5,label_str,size=20,color=colors[i],
		# 	horizontalalignment='right',alpha=0.75,style='italic',weight='bold')

	#make_no_frame_legend(ncol=3,title='Partition of teams by position')
	alphas = linspace(0.1,0.2,len(years)+2)
	ymax = 1.2*max(parray[:,0])
	bar(years[0]-2, ymax, width=1.0, facecolor='gray', edgecolor='white', alpha=alphas[0])
	for i,year in enumerate(years):
		bar(year-1, ymax, width=1.0, facecolor='gray',
			edgecolor='black', alpha=alphas[i+1],linewidth=0.01)
	bar(year,ymax, width=1.0, facecolor='gray', edgecolor='white', alpha=alphas[-1],
		linewidth=0.0)
	#make_no_frame_legend(loc='lower left',ncol=3)
	xlim([min(years)-2,max(years)+1])
	ylim([80,ymax])
	
	for ylab in [150,200,250,300]:
		text(years[0]-0.55,ylab-8,str(ylab),size=30,
			horizontalalignment='right',alpha=0.25,style='italic',weight='bold')
		hlines(ylab-2,years[0],years[-1],linestyle='-',alpha=0.5,color='gray')
	
	for year in years[::3]:
		text(year+0.20,110,str(year),size=30,rotation=80,
			horizontalalignment='right',alpha=0.25,style='italic',weight='bold')
		vlines(year,years[0],years[-1],linestyle='-.',alpha=0.15)
	
	offsets = [-20,10,10,0,10]
	for i,label in enumerate(['Top 4','5-8','9-12','13-16','Bottom 4']):
		ypos = parray[-1,i] + offsets[i]
		text(years[-5],ypos,label,size=30,color=colors[i],alpha=0.5)

	#plot(years,100*array(wins)/array(total_games),'o-',label='wins({},N={})'.format(dict_league['Country'][0:3],N),**kwargs_for_points)
	#plot(years,100*array(draws)/array(total_games),'o-',label='loses({},N={})'.format(dict_league['Country'][0:3],N),**kwargs_for_points)
	#plot(years,100*array(loses)/array(total_games),'o-',label='draws({},N={})'.format(dict_league['Country'][0:3],N),**kwargs_for_points)
	#make_no_frame_legend(loc=0)
	plot_ar_logo('Point totals for Premier League teams divided into quintiles')
	savefig('test.pdf')
	savefig('plot1.png')

	print '| {:20} | {:20} | {:20} |'.format( *(["-"*20]*3))
	print '| {:20} | {:20} | {:20} |'.format("Team","Finishes in top 4",
		"Years achieved")
	print '| {:20} | {:20} | {:20} |'.format( *(["-"*20]*3))
	
	teams_td = list( set(top_division) )
	top_counts = [ top_division.count(element) 
		for element in teams_td ]
	indeces = index_rank_high_to_low(top_counts)
	
	for index in indeces:
		years_td = ' '
		if ( top_division.count(teams_td[index]) <= 3):
			for i in range(len(top_division)):
				if ( top_division[i]==teams_td[index] ):
					years_td = years_td + ', ' + str(tp_years[i])

		print '| {:20} | {: ^20} | {:20} |'.format(\
		 teams_td[index], top_division.count(teams_td[index]), years_td[2:] )
	
	print '| {:20} | {:20} | {:20} |'.format( *(["-"*20]*3))


	# <table border="1">
	# <tr>
	# <td>row 1, cell 1</td>
	# <td>row 1, cell 2</td>
	# </tr>
	# <tr>
	# <td>row 2, cell 1</td>
	# <td>row 2, cell 2</td>
	# </tr>
	# </table>
	print '<table border="1.0" align="center" cellpadding="0" cellspacing="0">'
	print '<tr bgcolor="gray">'
	print '<td> {: ^20} </td><td> {: ^20} </td><td> {: ^20} </td>'.format(\
		'Team', ' # of finishes in top 4 ', ' Years accomplished ' )
	print '</tr>'
	for index in indeces:
		years_td = '  Too many...'
		if ( top_division.count(teams_td[index]) <= 3):
			years_td = ' '
			for i in range(len(top_division)):
				if ( top_division[i]==teams_td[index] ):
					years_td = years_td + ', ' + str(tp_years[i])
		print '<tr>'			
		print '<td> {: ^20} </td><td> {: ^20} </td><td> {: ^20} </td>'.format(\
		teams_td[index], top_division.count(teams_td[index]), years_td[2:] )
		print '</tr>'
	print '</table>'
	return array(points),years,top_division

figure(1)
points, years, tp = get_results_distribution_divided('EPL_list_of_leagues_parsed.txt',5)
#figure(2)
#points, years = get_results_distribution_divided('BL_list_of_leagues_parsed.txt',5)
