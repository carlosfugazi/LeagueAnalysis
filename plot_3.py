# will show arsenal's defensive record
execfile('applications_on_parsed_data.py')
def getting_gd_arsenal_figure():
	attr = 'goals against'
	attr2 = 'goals for'
	getting_two_attributes_over_the_years('EPL_list_of_leagues_parsed.txt','Arsenal',
		attr,attr2)

def getting_gd_manu_figure():
	attr = 'goals against'
	attr2 = 'goals for'
	getting_two_attributes_over_the_years(
		'EPL_list_of_leagues_parsed.txt','Manchester United',attr,attr2)


def circle_plot(labels,data,team,label):
	import matplotlib
	import numpy as np
	import matplotlib.pyplot as plt

	# Data to be represented
	# ----------
	# labels = ['January', 'Feburary', 'March', 'April', 'May', 'June',
	#           'July', 'August', 'September', 'October', 'November', 'December']
	n = len(labels)
	# data = np.random.uniform(0,1,n)
	# ----------

	# Make figure square and background the same colors as axes (white)
	fig = plt.figure(figsize=(8,6), facecolor='white')

	# Make a new polar axis
	axes = plt.subplot(111, polar=True, axisbelow=True)

	# Put labels on outer 
	T = np.arange(np.pi/n, 2*np.pi, 2*np.pi/n)
	R = np.ones(n)*10
	width = 2*np.pi/n

	# Label background
	bars  = axes.bar(T, R, width=width, bottom=9,
	                 linewidth = 2, facecolor = '0.9', edgecolor='1.00')
	# Labels
	for i in range(T.size):
	    theta = T[n-1-i]+np.pi/n + np.pi/2
	    plt.text(theta, 9.5, labels[i], rotation=180*theta/np.pi-90,
	             family='Helvetica Neue', size=7,
	             horizontalalignment="center", verticalalignment="center")

	# Data
	R = 1 + data*6
	bars = axes.bar(T, R, width=width, bottom=2,
	                linewidth=1, facecolor = '0.75', edgecolor='1.00')
	for i,bar in enumerate(bars):
	    bar.set_facecolor(plt.cm.hot(R[i]/10))

	# Text i the center
	plt.text(1*np.pi/2, 0.05, team,
	         size=16, family='Helvetica Neue Light',
	         horizontalalignment="center", verticalalignment="bottom")
	plt.text(3*np.pi/2, 0.05, label, color="0.50",
	         size=8, family='Helvetica Neue Light',
	         horizontalalignment="center", verticalalignment="top")

	# Set ticks, tick labels and grid
	plt.ylim(0,max(data))
	plt.xticks(T)
	plt.yticks(np.arange(1,max(data),2))

	axes.grid(which='major', axis='y', linestyle='-', color='0.75')
	axes.grid(which='major', axis='x', linestyle='-', color='1.00')
	for theta in T:
	    axes.plot([theta,theta], [4,9], color='w', zorder=2, lw=1)
	axes.set_xticklabels([])
	axes.set_yticklabels([])

	plt.show()

def mode(list1):
	uniques = list(set(list1))
	max_freq = 0
	for unique in uniques:
		if ( list1.count(unique) > max_freq ):
			max_freq         = list1.count(unique)
			max_freq_element = unique
	return max_freq_element

def get_total_goals_againts_by_match(team,plot_ga,legend_bool,color):
	# team = 'Man United'
	# team = 'Arsenal'
	# goals_against = {}
	goals_against_with_wins = []
	files = [ file1.strip() for file1 in (open('EPL_list_of_leagues_parsed.txt','r')).readlines() ]
	years = []
	files = files[-8:]
	for file1 in files:
		dict_league = parse_dict( file1.strip() )
		dict_team   = get_league_table(False,file1)
		# print dict_league['Matchday']
		team_applied = find_similar_team_name(team,file1.strip())
		print dict_league['Year2'],dict_team[team_applied]['league position']
		years.append( dict_league['Year2'])
		for i in range(dict_league['N_games']):
			for j,md in enumerate(dict_league['Matchday']):
				if ( i+1 == md and \
					team_applied in [ dict_league['Home Team'][j],dict_league['Away Team'][j] ] ):
					# print team,team_applied, dict_league['Home Team'][j],dict_league['Away Team'][j] 
					if (team_applied == dict_league['Home Team'][j]):
						goals_against = dict_league['Goals Away'][j]
						goals_for     = dict_league['Goals Home'][j]
						result_points = determine_home_points(dict_league['Goals Home'][j],dict_league['Goals Away'][j])
						oppo_team = dict_league['Away Team'][j]
						oppo_team_pos = dict_team[oppo_team]['league position']
						goals_against_with_wins.append( [ goals_against,goals_for,result_points,
							oppo_team,oppo_team_pos,'Home' ] )
					else:
						goals_against = dict_league['Goals Home'][j]
						goals_for     = dict_league['Goals Away'][j]
						result_points = determine_away_points(dict_league['Goals Home'][j],
							dict_league['Goals Away'][j] )
						oppo_team = dict_league['Home Team'][j]
						oppo_team_pos = dict_team[oppo_team]['league position']
						goals_against_with_wins.append( [ goals_against,goals_for,result_points,
							oppo_team,oppo_team_pos,'Away' ] )
	
	gat = 0; gft = 0; rpt = 0
	gas = []; gfs = []; rps = [];
	teams_defeats = []
	teams_defeats_pos = []
	teams_defeats_diff = []
	teams_wins = []
	teams_wins_pos = []
	teams_wins_diff = []
	for element in goals_against_with_wins:
		gat += element[0]; gas.append( element[0] )
		gft += element[1]; gfs.append( element[1] )
		rpt += element[2]; rps.append( element[2] )
		if (element[2] == 0):
			teams_defeats.append(element[3])
			teams_defeats_pos.append(element[4])
			teams_defeats_diff.append(element[0]-element[1])
		if (element[2] == 3):
			teams_wins.append(element[3])
			teams_wins_pos.append(element[4])
			teams_wins_diff.append(element[1]-element[0])

	print 'Total GA = {}, GF = {}, PTS = {}'.format( gat, gft, rpt )
	print 'Avg/season GA = {}, GF = {}, PTS = {}'.format( 1.0*gat/len(files), 1.0*gft/len(files),
		 1.0*rpt/len(files) )

	print '	{} most lost to {} with {} loses'.format( team_applied, mode(teams_defeats),
		 teams_defeats.count( mode(teams_defeats) ) )
	print '\tAverage position of teams lost to : ', mean(teams_defeats_pos)
	# print teams_defeats_pos
	
	print '	{} most beat {} with {} wins'.format( team_applied, mode(teams_wins),
		 teams_wins.count( mode(teams_wins) ) )
	print '\tAverage position of teams beaten : ', mean(teams_wins_pos)
	# print teams_defeats_pos
	print ' Analyzing margins of victory'
	margins_wins = list(set(teams_wins_diff))
	for element in margins_wins:
		print "\tmargin: {} freq: {}".format(
			element,teams_wins_diff.count(element))
	
	print ' Analyzing margins of losses'
	margins_losses = list(set(teams_defeats_diff))
	for element in margins_losses:
		print "\tmargin: {} freq: {}".format(
			element,teams_defeats_diff.count(element))

	frequencies_ga   = []
	frequencies_wins = []

	gas_uniques = list(set(gas))
	for ga in gas_uniques:
		frequencies_ga.append( gas.count(ga) )
		freq_win = 0
		for i,ga2 in enumerate(gas):
			if ( ga2 == ga and rps[i] == 3 ): freq_win += 1
		frequencies_wins.append(freq_win)
	frequencies_gf      = []
	frequencies_wins_gf = []
	gfs_uniques = list(set(gfs))
	for gf in gfs_uniques:
		frequencies_gf.append( gfs.count(gf) )
		freq_win = 0
		for i,gf2 in enumerate(gfs):
			if ( gf2 == gf and rps[i] == 3 ): freq_win += 1
		frequencies_wins_gf.append(freq_win)
	width = 1.0     # gives histogram aspect to the bar diagram
	freq_offset = 40
	percent_offset = 20
	if ( plot_ga == True ):
		# ax = axes()
		xticks(array(gas_uniques) + (width / 2),gas_uniques)
		# ax.set_xticklabels( gas_uniques )
		# stats_str = [ max()]
		stats_str = "\n Mean = {:.3f}\n Mode = {}".format(mean(gas),mode(gas))
		bar( gas_uniques, frequencies_ga, width, color=color,label='Freq of GA'+stats_str,alpha=1.0,
			edgecolor='w')
		bar( gas_uniques, frequencies_wins, width, color='gray',label='Freq of win',alpha=0.35)
		# title(team)
		if ( legend_bool == True): make_no_frame_legend(loc=0)
		ylim([0,max(frequencies_ga)+freq_offset])
		# text(4,80,'Goals against/match = {:.2f} '.format(mean(gas)),size=30,color=color )
		# print frequencies_wins
		for i,ga in enumerate(gas_uniques):
			text(ga+0.25,frequencies_ga[i]+percent_offset,
				'{1:.0f} pts.'.format( 100*frequencies_wins[i]/frequencies_ga[i],frequencies_wins[i]*3),
				size=20,color=color,style='italic',alpha=0.75)
			text(ga+0.2,frequencies_ga[i]+freq_offset,
				'{:3}'.format( frequencies_ga[i] ), size=30,color=color,alpha=0.5,weight='bold')
		return gas_uniques,frequencies_wins,teams_defeats,teams_defeats_pos,teams_wins,teams_wins_pos
	else:
		# ax = axes()
		xticks(array(gfs_uniques) + (width / 2),gfs_uniques)
		# ax.set_xticklabels( gas_uniques )
		stats_str = "\n Mean = {:.3f}\n Mode = {}".format(mean(gfs),mode(gfs))
		
		bar( gfs_uniques, frequencies_gf, width, color=color,label='Freq of GF'+stats_str,alpha=1.0)
		bar( gfs_uniques, frequencies_wins_gf, width, color='gray',label='Freq of win',alpha=0.5)
		# title(team)
		if ( legend_bool == True):make_no_frame_legend(loc=0)
		ylim([0,max(frequencies_gf)+freq_offset+30])
		# print frequencies_wins_gf
		for i,gf in enumerate(gfs_uniques):
			if ( frequencies_wins_gf[i] != 0):
				text(gf+0.15,frequencies_gf[i]+percent_offset,
					'{:.0f}%'.format( 100*frequencies_wins_gf[i]/frequencies_gf[i]), size=20,color='k' )
			text(gf+0.2,frequencies_gf[i]+freq_offset,
				'{}'.format( frequencies_gf[i] ), size=20,color='k',alpha=0.5)
		return gfs,frequencies_gf,teams_defeats,teams_defeats_pos,teams_wins,teams_wins_pos

def circles():
	# clf()
	# circle_plot(gfs,array(freq_gfs)/max(freq_gfs)+2,'Manchester United','Goals for')
	fig = plt.figure(1,figsize=(10,10))
	clf()
	a = axes([0.01,0.01,1-0.01,1-0.01],frameon=True)
	ax = fig.add_subplot(1, 1, 1)
	# ax = gca()
	# 
	# xticks()
	# yticks()
	colors = ['b','g','r','k','c','y','m']
	for i in range(len(gfs)):
		# X = Xs[i]
		if i == 0:
			X=0; Y=0;
		else:
			X = X+2*log(freq_gfs[i-1])
			Y = Y+2*log(freq_gfs[i-1])
		loc = (X, Y)
		print loc
		circ = plt.Circle(loc, radius=log(freq_gfs[i]), color=colors[i])
		# plt.contour(X, Y, (F - G), [0])
		ax.add_patch(circ)

	text(-80,0,'Goals against : {}, freq={}'.format( gfs[0],freq_gfs[0] ),size=30)
	xlim([-30,30])
	ylim([-30,30])
	plt.show()

def test_figure():
	# ax = gca(frameon=False)
	figure(1)
	clf()
	subplot(121)
	# a = axes([0.001, 0.001, 0.999, 0.999],frameon=False)
	gas,gas_f,def_teams,def_teams_pos,w_teams,w_teams_pos = get_total_goals_againts_by_match('Arsenal',True)
	subplot(122)
	# a = axes([0.001, 0.001, 0.999, 0.999],frameon=False)
	gas2,gas_f2,def_teams2,def_teams_pos2,w_teams2,w_teams_pos2 = get_total_goals_againts_by_match('Manchester United',True)

	figure(2)
	clf()

	subplot(121)
	width = 1.0
	bar(array(list(set(def_teams_pos)))-width/2, 
		[def_teams_pos.count(pos) for pos in list(set(def_teams_pos))],color='r',width=width)
	title('Total loses = {}'.format(len(def_teams_pos)))
	subplot(122)
	bar(array(list(set(def_teams_pos2)))-width/2, 
		[def_teams_pos2.count(pos) for pos in list(set(def_teams_pos2))],color='r',width=width)
	title('Total loses = {}'.format(len(def_teams_pos2)))

	figure(3)
	clf()

	subplot(121)
	width = 1.0
	bar(array(list(set(w_teams_pos)))-width/2, 
		[w_teams_pos.count(pos) for pos in list(set(w_teams_pos))],color='r',width=width)
	title('Total Wins = {}'.format(len(w_teams_pos)))
	subplot(122)
	bar(array(list(set(w_teams_pos2)))-width/2, 
		[w_teams_pos2.count(pos) for pos in list(set(w_teams_pos2))],color='r',width=width)
	title('Total Wins = {}'.format(len(w_teams_pos2)))


	# subplot(122)	
	# bar(list(set(def_teams_pos2)))

	# figure(2)
	# clf()
	# subplot(121)
	# get_total_goals_againts_by_match('Arsenal',False)
	# subplot(122)
	# figure(1)
	# gfs,freq_gfs = get_total_goals_againts_by_match('Manchester United',True)
	# clf()

figure(1,figsize=(12,10))


team = 'Arsenal'
# plot_team_logo(team,axes1)

clf()
a = axes([0,0.5,1,0.5],frameon=False)
ymax = 250
for i in range(0,6,1):
	bar(i,ymax,width=1.0,alpha=0.80-0.15*i,color='gray',edgecolor='white')

gas,gas_f,def_teams,def_teams_pos,w_teams,w_teams_pos = get_total_goals_againts_by_match(
	team,True,False,'b')
xticks([])
xlim([0,6])
ylim([0,ymax])
FS = 90
for i in range(0,5,1):
	text(i+0.3,200,str(i),rotation=0,size=70,color='black',alpha=0.5,weight='bold',style='italic')
text(3.25,180,'Conceded goals/match',size=40,alpha=0.4,family='sans-serif',horizontalalignment='center')
text(5.4,150,'# of matches since 2005',size=40,alpha=0.4,family='sans-serif',
	rotation='vertical',horizontalalignment='center')
text(5.65,130,'with points generated from wins',size=20,alpha=0.4,family='sans-serif',
	rotation='vertical',horizontalalignment='center')
# plot_ar_logo('Goals against frequencies')s
plot_my_logo([0.0,0.51,0.5,0.5])
plot_team_logo(team, [0.5,0.5,0.5,0.5])

team2 = 'Manchester United'
plot_team_logo(team2,[0.5,0.0,0.5,0.5])

a = axes([0,0.0,1,0.5],frameon=False)
ymax = 230
for i in range(0,6,1):
	bar(i,ymax,width=1.0,alpha=0.80-0.15*i,color='gray',edgecolor='white')

gas2,gas_f2,def_teams2,def_teams_pos2,w_teams2,w_teams_pos2 = get_total_goals_againts_by_match(
	team2,True,False,'r')
xticks([])

ylim([ymax,0])
xlim([0,6])

# plot_ar_logo('Goals against frequencies\nand win %',
# 		xmin2=1.80,xmin=1.0,OFFSET=20,ymax=230,FS=80,ymax2=170)
plot_ar_logo('',xmin2=1.80,xmin=1.0,OFFSET=20,ymax=230,FS=80,ymax2=170)
savefig('blog/plot_3.png')