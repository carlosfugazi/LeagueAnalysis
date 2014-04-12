#
# plot 4
#
execfile('classes.py')

figure(1); clf()
subplot(121)
all_points = []
symbols = ['o']*7 + ['s']*7
icount  = 0
for league_file in ( get_all_EPL_leagues() ):
	# print league_file
	l = League(league_file)
	if ( l.dict_league['Year2'] > 2004):
		l.plot_team_points_evolution('Arsenal',linestyle='-'+symbols[icount] )
		all_points.append( l.dict_teams['Arsenal']['points evolution'])
		icount += 1

make_no_frame_legend(loc=0	, numpoints=1)
Matchdays = 2*len(l.dict_teams.keys())-2
# figure(2); clf()
subplot(122)
print Matchdays

for j in range( Matchdays ):
	sum_points = 0
	for i,points in enumerate(all_points):
		sum_points += points[j]
		plot( [j+1], points[j], 'bo', mfc='none', mec='b', markersize=7.5, alpha=0.5)

	plot( [j+1], sum_points/len(all_points) , 'bo', markersize=7.5)

# tight_layout()