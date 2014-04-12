#
# plot 4
#
execfile('classes.py')

figure(1); clf()
subplot(121)
all_points, all_points2, all_points3, all_points4 = [], [], [], []
symbols = ['o']*7 + ['s']*7
icount  = 0
for league_file in ( get_all_EPL_leagues() ):
	# print league_file
	l = League(league_file)
	if ( l.dict_league['Year2'] > 2004):
		l.plot_team_points_evolution('Arsenal',linestyle='-'+symbols[icount] )
		all_points.append( l.dict_teams['Arsenal']['points evolution'])
		all_points2.append( l.dict_teams['Manchester United']['points evolution'])
		all_points3.append( l.dict_teams['Chelsea']['points evolution'])
		all_points4.append( l.dict_teams['Liverpool']['points evolution'])
		icount += 1

make_no_frame_legend(loc=0	, numpoints=1)
Matchdays = 2*len(l.dict_teams.keys())-2
# figure(2); clf()
subplot(122)
print Matchdays

colors = ['b','r','k','g']
teams = ['Arsenal','Manchester United','Chelsea','Liverpool']
for color,all_points_here,team in zip(colors,[ all_points, all_points2, all_points3, all_points4 ],teams):
	all_sum_points = []
	for j in range( Matchdays ):
		sum_points = 0
		for i,points in enumerate(all_points_here):
			sum_points += points[j]
			plot( [j+1], points[j], color+'o', mfc='none', mec=color, markersize=7.5, alpha=0.5)
		all_sum_points.append( sum_points )
	plot( range(Matchdays), array(all_sum_points)/len(all_points) , color+'o', markersize=7.5, label=team)

# tight_layout()
make_no_frame_legend(loc=0,numpoints=121)
figure(2); clf()
# subplot(121)
# all_points = []
# symbols = ['o']*7 + ['s']*7
icount  = 0
for league_file in ( get_all_EPL_leagues() ):
	# print league_file
	l = League(league_file)
	if ( l.dict_league['Year2'] > 2004):
		l.plot_team_position_evolution('Arsenal',linestyle='-'+symbols[icount] )
		# all_points.append( l.dict_teams['Arsenal']['points evolution'])
		icount += 1
