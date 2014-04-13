# applications of reduced data
execfile('league_table_parsing.py')

# From git hub repo, initialization stuff
# touch README.md
# git init
# git add README.md
# git commit -m "first commit"
# git remote add origin https://github.com/carlosfugazi/LeagueAnalysis.git
# git push -u origin master

# http://www.worldfootball.net/alle_spiele/ita-serie-a-2011-2012/
# http://www.worldfootball.net/alle_spiele/esp-primera-division-2011-2012/
# http://www.worldfootball.net/alle_spiele/fra-ligue-1/
# http://www.worldfootball.net/alle_spiele/bundesliga/


# League dict keys
# 	dict_['League Name'] = LEAGUENAME
# 	dict_['Country'] = COUNTRY
# 	dict_['Years'] = YEARS
# 	dict_['Year1'] = int(YEARS.split('-')[0])
# 	dict_['Year2'] = int(YEARS.split('-')[1])
# 	dict_['N_games'] = len(dict_['Home Team'])
# 	dict_['Matchday,Home Team,Away Team,Goals Home,Goals Away,Points Home,Points Away']

# Teams dict 
# dict_teams[team] = {'points':point_totals[i],
# 		'goal difference':goal_differences[i],
# 		'league position':position, 'goals for':goals_for[i], 
# 		'goals against':goals_against[i], 'home points':points_home[i],
# 		'away points':points_away[i],
# 		'wins':wins[i],'draws':draws[i],'loses':loses[i]}

execfile('gallery_fr/bar_ex.py')

def push_updates_to_github():
	os.system('git push -u origin master')

def plot_ar_logo(sublabel):
	ax = gca()
	ymin, ymax = ax.get_ylim()
	xmin, xmax = ax.get_xlim()
	FS = 90
	OFFSET = 0.1*ymax
	text( xmin+0.5,ymax - 1.3*OFFSET,'{}'.format(sublabel),
		size=30,alpha=0.75,style='italic',weight='bold')
	# text(  xmin+1.5,ymax - OFFSET,'{:10}'.format('$\mathbf{\Lambda rs \Gamma utbolistica}$'),
	# 	size=FS-20,alpha=0.25,horizontalalignment='left')
	text(  xmin+0.5,ymax - OFFSET*0.8,'@',
		size=FS-25,alpha=0.25,horizontalalignment='left')
	text(  xmin+1.55,ymax - 0.85*OFFSET,'{:20}'.format('ArsFutbolistica'),
		size=FS-20,alpha=1.0,horizontalalignment='left',weight='medium',style='italic')
		

def getting_gd_liverpool_figure():
	attr = 'goals against'
	attr2 = 'goals for'
	getting_two_attributes_over_the_years('EPL_list_of_leagues_parsed.txt','Liverpool',attr,attr2)

def getting_gd_arsenal_figure():
	attr = 'goals against'
	attr2 = 'goals for'
	getting_two_attributes_over_the_years('EPL_list_of_leagues_parsed.txt','Arsenal',attr,attr2)

def getting_gd_manu_figure():
	attr = 'goals against'
	# attr = 'goals for'
	getting_attribute_over_the_years('EPL_list_of_leagues_parsed.txt','Manchester United',attr)

def getting_gd_chelsea_figure():
	attr = 'goals against'
	attr2 = 'goals for'
	# getting_attribute_over_the_years('EPL_list_of_leagues_parsed.txt','Chelsea',attr)
	getting_two_attributes_over_the_years('EPL_list_of_leagues_parsed.txt','Chelsea',attr,attr2)


	# runcdm('*/.csv')

def plot_ar_logo(sublabel,**kwargs):
	ax = gca()

	ymin, ymax = ax.get_ylim()
	xmin, xmax = ax.get_xlim()
	FS = 90
	print xmin, xmax
	print ymin, ymax
	OFFSET = 0.1*ymax
	
	xmin = parse_kwargs('xmin',xmin,**kwargs)
	xmin2= parse_kwargs('xmin2',xmin,**kwargs)
	
	ymax = parse_kwargs('ymax',ymax,**kwargs)
	ymax2 = parse_kwargs('ymax2',ymax-3.3*OFFSET,**kwargs)
	
	OFFSET = parse_kwargs('OFFSET',OFFSET,**kwargs)
	FS   = parse_kwargs('FS',FS,**kwargs)

	text( xmin2,ymax2,'{}'.format(sublabel),
		size=30,alpha=0.75,style='italic',weight='bold')
	
	# text( xmin+0.75,ymax - OFFSET*0.8,'@',
	# 	size=FS-25,alpha=0.25,horizontalalignment='left')
	
	text(  xmin,ymax - 0.85*OFFSET,'@{:20}'.format('ArsFutbolistica'),
		size=FS-20,alpha=1.0,horizontalalignment='left',weight='medium',style='italic')
	text(  xmin-.01,ymax - 0.84*OFFSET,'@{:20}'.format('ArsFutbolistica'),
		size=FS-20,alpha=0.4,horizontalalignment='left',weight='medium',style='italic')	
	
def getting_gd_bayernmunich_figure():
	attr = 'goals against'
	getting_attribute_over_the_years('BL_list_of_leagues_parsed.txt','FC Bayern Muenchen',attr)

def plot_league_team_logo(league_logo_file,team_logo_file,axes1,axes2):
	import Image
	import numpy as np
	import matplotlib.mlab as mlab
	import matplotlib.pyplot as plt
	# league_logo_file = dict_league['Logo file']

	if ( league_logo_file != None ):
		a = axes(axes1,frameon=False)
		im = Image.open(league_logo_file)
		plt.imshow(im, origin='lower',alpha=0.15)
		xticks([])
		yticks([])
		ax = plt.gca()
	

	if (team_logo_file != None ):
		# team_logo_file   = dict_team[team]['logo file']
		#cmap=cmap = plt.cm.Reds
		a = axes(axes2,frameon=False)
		im = Image.open(team_logo_file)
		plt.imshow(im, origin='lower',alpha=0.15)
		xticks([])
		yticks([])


def take_off_right_and_top_axis_lines():
	from mpl_toolkits.axes_grid.axislines import SubplotZero
	ax = SubplotZero(gcf(),111)
	gcf().add_subplot(ax)
	ax = gca()
	for direction in ['right','top']:
		ax.axis[direction].set_visible(False)
	ax = gca()
	ax.minorticks_on()


def take_off_right_and_top_axis_lines_after():
	ax=gca()
	ax.spines["right"].set_visible(False)
	ax.spines["top"].set_visible(False)
	# ax.minorticks_on()

	## the original answer:
	## see  http://old.nabble.com/Ticks-direction-td30107742.html
	#for tick in ax.xaxis.majorTicks:
	#  tick._apply_params(tickdir="out")

	# the OP way (better):
	ax.tick_params(axis='both', direction='out')
	ax.get_xaxis().tick_bottom()   # remove unneeded ticks 
	ax.get_yaxis().tick_left()
 
 
def plot_my_logo(axes1,kwargs=dict(origin='lower',alpha=0.15)):
	import Image
	import numpy as np
	import matplotlib.mlab as mlab
	import matplotlib.pyplot as plt
	a = axes(axes1,frameon=False)
	# team_mod, team_logo_file = find_team_logo_file(team)
	im = Image.open('logo/drawing_final.png')
	plt.imshow(im,**kwargs)
	xticks([])
	yticks([])

def plot_team_logo(team,axes1,kwargs=dict(origin='lower',alpha=0.15)):
	def find_team_logo_file(team):
		fopen = open('logos/team_logo_def.csv','r')
		lines = [ line.strip() for line in fopen.readlines() ]
		fopen.close()

		for line in lines:
			elements = line.split(',')

			if ( get_close_matches(team,[elements[0]]) != [] ):
				print get_close_matches(team,[elements[0]])[0]
				print elements[1]
				break
		return get_close_matches(team,[elements[0]])[0],elements[1]

	import Image
	import numpy as np
	import matplotlib.mlab as mlab
	import matplotlib.pyplot as plt
	a = axes(axes1,frameon=False)
	team_mod, team_logo_file = find_team_logo_file(team)
	im = Image.open(team_logo_file)
	plt.imshow(im,**kwargs )
	xticks([])
	yticks([])

def getting_attribute_over_the_years(master_filename,team,attr):
	
	fopen = open(master_filename,'r');
	league_files = [ line.strip() for line in fopen.readlines() ]
	fopen.close()
	clf()

	dict_league      = parse_dict(league_files[0])
	Found_team = False

	if ( dict_league.has_key('Logo file') == False):
		league_logo_file = None
	else:
		league_logo_file = dict_league['Logo file']

#	Found_exact_team_list = []

	for filename in league_files:
		dict_team = get_league_table(False,filename)
		if ( dict_team.has_key(team) == True ):
			Found_team = True
#			Found_exact_team_list.append( Found_team )
			break

	if ( Found_team == False ):
		print "No exact match found for ", team
		print "Attempting to find match"
		for filename in league_files:
			# dict_team = get_league_table(False,filename)
			match = find_similar_team_name(team,filename) 
			if ( match != None ):
				# Found_team = True
				print "Possible match found : ", match
				choice = raw_input('Accept? (y/n)')
				if ( choice.lower() == 'y' ):
					team = match
					Found_team = True
					break
				else:
					pass
	
	if ( Found_team == False ):
		raise ValueError, "Still exact or close match found for "+team

	if ( dict_team[team].has_key('logo file') == False):
		team_logo_file = None
	else:
		team_logo_file = dict_team[team]['logo file']

	plot_league_team_logo(league_logo_file,team_logo_file,[0.0, 0.0, 1-0.5, 1-0.2],[0.35, 0.15, 0.75, 0.65])

	a = axes([0.001, 0.001, 0.999, 0.999],frameon=False)
	kwargs_for_points = {'markerfacecolor':'w','markeredgewidth':2,'linewidth':4}
	
	GA, years = get_attribute_for_range_of_leagues(team,league_files,attr)
	#plot(years,GA,'o-',label=team,**kwargs_for_points)
	kwargs_for_points = {'markerfacecolor':'w','markeredgewidth':2,'linewidth':4}
	
	# gradient_bars(years,GA)
	ymax = 1.5*max(GA)
	#title(attr)
	FS=90
	OFFSET = 0.28*max(GA)
	# symax   = 2.0*max(GA)
	custom_single_bars(years,GA,ymax,0.0,0.0+10)
	
	# text(years[0],1.35*max(GA)-5,team,fontsize=FS,alpha=1.0)
	
	text( years[0]+0.01*max(GA),ymax-1.6*OFFSET,'{}: {}'.format(team,attr[0].upper()+attr[1:]),
		fontsize=FS/4,alpha=0.75,style='italic',weight='bold')
	text( years[0],ymax - OFFSET,'{} '.format('@$\mathbf{\Lambda rs \Gamma utbolistica}$'),
		fontsize=FS-20,alpha=0.25)
	text( years[0]+0.045*max(GA),ymax - 1.1*OFFSET,'{} '.format('$\mathbf{\Lambda rs \Gamma utbolistica}$'),
		fontsize=FS-20,alpha=1.0)
	#make_no_frame_legend(loc=0,ncol=4)
	savefig('test.png')
	show()

def getting_two_attributes_over_the_years(master_filename,team,attr,attr2):
	
	fopen = open(master_filename,'r');
	league_files = [ line.strip() for line in fopen.readlines() ]
	fopen.close()
	clf()

	dict_league      = parse_dict(league_files[0])
	Found_team = False

	if ( dict_league.has_key('Logo file') == False):
		league_logo_file = None
	else:
		league_logo_file = dict_league['Logo file']

#	Found_exact_team_list = []

	for filename in league_files:
		dict_team = get_league_table(False,filename)
		if ( dict_team.has_key(team) == True ):
			Found_team = True
#			Found_exact_team_list.append( Found_team )
			break
	
	if ( Found_team == False ):
		print "No exact match found for ", team
		print "Attempting to find match"
		for filename in league_files:
			# dict_team = get_league_table(False,filename)
			match = find_similar_team_name(team,filename) 
			if ( match != None ):
				# Found_team = True
				print "Possible match found : ", match
				choice = raw_input('Accept? (y/n)')
				if ( choice.lower() == 'y' ):
					team = match
					Found_team = True
					break
				else:
					pass
	
	if ( Found_team == False ):
		raise ValueError, "Still exact or close match found for "+team

	if ( dict_team[team].has_key('logo file') == False):
		team_logo_file = None
	else:
		team_logo_file = dict_team[team]['logo file']

	plot_league_team_logo(league_logo_file,team_logo_file,
		[0.0, -0.25, 1-0.5, 1-0.5],[0.75, 0.75, 0.25, 0.25])

	a = axes([0.001, 0.001, 0.999, 0.999],frameon=False)
	kwargs_for_points = {'markerfacecolor':'w','markeredgewidth':2,'linewidth':4}
	
	GA, years = get_attribute_for_range_of_leagues(team,league_files,attr)
	GF, years = get_attribute_for_range_of_leagues(team,league_files,attr2)
	
	#plot(years,GA,'o-',label=team,**kwargs_for_points)
	kwargs_for_points = {'markerfacecolor':'w','markeredgewidth':2,'linewidth':4}
	
	maxscale = max( max(GA), max(GF))
	# gradient_bars(years,GA)
	# ymax =  2.0*maxscale
	# ymin = -2.0*maxscale
	#title(attr)
	FS=90
	OFFSET = 0.4*maxscale
	ymax   = 1.75*maxscale
	ymin   = -1.75*maxscale
	year_loc = 0.0*maxscale
	custom_single_bars(years,GA,ymax,ymin,year_loc,alpha=0.99)
	custom_single_bars(years,[ -element for element in GF],ymax,ymin,year_loc,
		alpha=0.99)
	
	# text(years[0],1.35*max(GA)-5,team,fontsize=FS,alpha=1.0)
	
	text( years[0]+0.01*max(GA),ymax-1.6*OFFSET,'{}: {}'.format(team,attr[0].upper()+attr[1:]),
		fontsize=FS/4,alpha=0.75,style='italic',weight='bold')
	text( years[0],ymax - OFFSET,'{} '.format('@$\mathbf{\Lambda rs \Gamma utbolistica}$'),
		fontsize=FS-20,alpha=0.25)
	text( years[0]+0.045*max(GA),ymax - 1.1*OFFSET,'{} '.format('$\mathbf{\Lambda rs \Gamma utbolistica}$'),
		fontsize=FS-20,alpha=1.0)

	#make_no_frame_legend(loc=0,ncol=4)
	savefig('test.png')
	show()


def get_league_position(team,abbreviation):
	fopen = open('{}_list_of_leagues_parsed.txt'.format(abbreviation),'r');
	league_files = [ line.strip() for line in fopen.readlines() ]
	print "Total number of leagues: ", len(league_files)
	# team = 'Arsenal'
	positions = []
	years     = []
	original_team = team
	for file1 in league_files:
		dict_ = get_league_table(False,file1)
		dict_league = parse_dict(file1)
		# print dict_['Arsenal'].keys()
		if ( dict_.has_key(team)):
			print team, " final position in ", dict_league['Years'], " was ",\
				dict_[team]['league position']
			positions.append( dict_[team]['league position'] )
			years.append(dict_league['Year2'])
		else:
			near_match = find_similar_team_name(team,file1)
			if ( near_match != None):
				print 'Near match found ({}) for input team ({})'.format(
					near_match,team )
				#if choice == 'y':
				team = near_match
				print team, " final position in ", dict_league['Years'], " was ",\
				dict_[team]['league position']
				positions.append( dict_[team]['league position'] )
				years.append(dict_league['Year2'])
	
	#print years, positions
	#plot(years,positions,label=team)
	plot(years,positions,'-o',label=original_team,
		markersize=10,markeredgecolor='black',markerfacecolor='white'
		,markeredgewidth=2,linewidth=4)
	xlim([min(years)-1,max(years)+1])
	xticks([])
	ylim([0,max(positions)+1])
	#yticks([0]+positions+[max(positions)+1])
	#yticks([])
	#xticks_ = {}
			
	for i,year in enumerate(years):
		text(year-0.25,0-0.45,str(year),color='black',rotation=45,alpha=1.0,
			fontsize=12,style='italic',weight='bold',horizontalalignment='left')
		vlines(year,0,positions[i],linestyle='--',alpha=0.5)
	text(min(years)-1,max(positions),'$\Lambda rs \ \Gamma utbolistica$',alpha=0.24,fontsize=75)
	grid(True)
	# make_no_frame_legend(loc=0)
	#legend(loc=0)
	make_no_frame_legend(loc=0)

def get_percetange_of_points(master_list_file,N):
	fopen = open(master_list_file,'r');
	league_files = [ line.strip() for line in fopen.readlines() ]
	print "Total number of leagues: ", len(league_files)
	percentages = []
	years       = []
	points1     = []
	points2     = []
	unique_teams_in_top_4 = []
	points_match = 0
	for file1 in league_files:
		dict_ = get_league_table(False,file1)
		dict_league = parse_dict(file1)
		Nteams = len(dict_.keys())
		#print dict_league['Year2'],Nteams
		# print dict_['Arsenal'].keys()
		total_points       = 0
		total_partial_high = 0
		total_partial_low  = 0
		N_games = max(dict_league['Matchday'])
		for key in dict_:
			total_points += dict_[key]['points']
			if ( dict_[key]['league position'] <= N ):
				total_partial_high += dict_[key]['points']
				if ( key not in unique_teams_in_top_4 ): unique_teams_in_top_4.append(key)
			else:
				total_partial_low += dict_[key]['points']
		percentages.append( 100.0*total_partial_high/total_points )
		#percentages.append( 100.0*total_partial_high/total_points )
		points1.append( total_partial_high )
		points2.append( total_partial_low  )
		years.append(dict_league['Year2'])
	# print years, positions
	subplot(121)
	normalization = max(dict_league['Matchday'])
	print "# of games per team in league = ", normalization
	print "# of unique teams to finish in top {}: {}".format(N,len(unique_teams_in_top_4))
	print "	teams:", unique_teams_in_top_4
	points_avg_top = array(points1)/(1.0*N*normalization)
	points_avg_bot =array(points2)/((1.0*Nteams-1.0*N)*normalization)
	plot(years,points_avg_top,label='avg. point/game top {}({})'.format(
		N,dict_league['Country']))
	plot(years,points_avg_bot,label='avg. point/game bot. {}({})'.format(
		Nteams-N,dict_league['Country']))
	xticks(years[::2])
	legend(loc='center right')
	subplot(122)
	plot(years,array(percentages),label='avg. % of total points in top {}({})'.format(
		N,dict_league['Country']))
	xticks(years[::2])
	legend(loc=0)
	#yticks([0]+positions+[max(positions)+1])
	#text(min(years)+0.2,mean(positions),'$Ars \ \Gamma utbolistica$',alpha=0.24,fontsize=75)
	# make_no_frame_legend(loc=0)
	#legend(loc=0)
	return points_avg_top,points_avg_bot,years,percentages

def get_results_distribution(master_list_file,N):
	fopen = open(master_list_file,'r');
	league_files = [ line.strip() for line in fopen.readlines() ]
	print "Total number of leagues: ", len(league_files)
	years       = []
	unique_teams_in_top_N = []
	wins, draws, loses = [], [], []
	total_games = []
	for file1 in league_files:
		dict_ = get_league_table(False,file1)
		dict_league = parse_dict(file1)
		Nteams = len(dict_.keys())
		all_wins  = 0
		all_draws = 0
		all_loses = 0
		N_games = max(dict_league['Matchday'])
		for key in dict_:
			if ( dict_[key]['league position'] <= N ):
				all_wins  += dict_[key]['wins']
				all_draws += dict_[key]['draws']
				all_loses += dict_[key]['loses']
		wins.append( all_wins )
		draws.append( all_draws )
		loses.append( all_loses )
		years.append(dict_league['Year2'])
		total_games.append( all_wins + all_draws + all_loses )
	print total_games
	kwargs_for_points = {'markerfacecolor':'w','markeredgewidth':2,'linewidth':4}
	plot(years,100*array(wins)/array(total_games),'o-',label='wins({},N={})'.format(dict_league['Country'][0:3],N),**kwargs_for_points)
	plot(years,100*array(draws)/array(total_games),'o-',label='loses({},N={})'.format(dict_league['Country'][0:3],N),**kwargs_for_points)
	plot(years,100*array(loses)/array(total_games),'o-',label='draws({},N={})'.format(dict_league['Country'][0:3],N),**kwargs_for_points)
	legend(loc=0)
	
	#yticks([0]+positions+[max(positions)+1])
	#text(min(years)+0.2,mean(positions),'$Ars \ \Gamma utbolistica$',alpha=0.24,fontsize=75)
	# make_no_frame_legend(loc=0)
	#legend(loc=0)
	#return points_avg_top,points_avg_bot,years,percentages

def get_figure_points_per_game_and_tendencies_BL_EPL_comp():
	clf()
	colors_ = ['b','g','r','c']
	pavgh, pavgl,years, percentages = get_percetange_of_points(
		'BL_list_of_leagues_parsed.txt',1)
	a, b, RR = linreg(array(years)-min(years),pavgh)
	subplot(121)
	plot( array(years), a*( array(years)-min(years) )+b, colors_[0]+'--')
	print "Linear tendency: Points Top /avg  = {:.2f} + {:.5f}*(Year-{}) ".format(b,a,min(years))
	print "	r**2 =  ",RR
	a, b, RR = linreg(array(years)-min(years),pavgl)
	plot( array(years), a*( array(years)-min(years) )+b, colors_[1]+'--')
	print "Linear tendency: Points Bot /avg  = {:.2f} + {:.5f}*(Year-{}) ".format(b,a,min(years))
	print " r**2 =  ",RR

	subplot(122)
	a, b, RR = linreg(array(years)-min(years),percentages)
	plot( array(years), a*( array(years)-min(years) )+b, colors_[0]+'--')
	print "Linear tendency: % Top  = {:.2f} + {:.5f}*(Year-{}) ".format(b,a,min(years))
	print "	r**2 =  ",RR

	pavgh, pavgl,years, percentages  = get_percetange_of_points('EPL_list_of_leagues_parsed_to_2010.txt',1)
	subplot(121)
	a, b, RR = linreg(array(years)-min(years),pavgh)
	plot( array(years), a*( array(years)-min(years) )+b, colors_[2]+'--')
	print "Linear tendency: Points Top /avg  = {:.2f} + {:.5f}*(Year-{}) ".format(b,a,min(years))
	print "	r**2 =  ",RR
	a, b, RR = linreg(array(years)-min(years),pavgl)
	plot( array(years), a*( array(years)-min(years) )+b, colors_[3]+'--')
	print "Linear tendency: Points Bot /avg  = {:.2f} + {:.5f}*(Year-{}) ".format(b,a,min(years))
	print "	r**2 =  ",RR
	subplot(122)
	a, b, RR = linreg(array(years)-min(years),percentages)
	plot( array(years), a*( array(years)-min(years) )+b, colors_[1]+'--')
	print "Linear tendency: % Top  = {:.2f} + {:.5f}*(Year-{}) ".format(b,a,min(years))
	print "	r**2 =  ",RR

#get_figure_points_per_game_and_tendencies_BL_EPL_comp()
#figure(1)
#clf()
#get_results_distribution('EPL_list_of_leagues_parsed.txt',1)

#get_figure_points_per_game_and_tendencies_BL_EPL_comp()
#figure(2)
#clf()
# get_results_distribution('BL_list_of_leagues_parsed.txt',1)
#get_league_position('Manchester United',None)
#get_league_position('Arsenal',None)
#get_league_position('Chelsea',None)
#get_league_position('Liverpool',None)
