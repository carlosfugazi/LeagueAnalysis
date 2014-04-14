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

# colors = ['b','r','k','g']
# teams = ['Arsenal','Manchester United','Chelsea','Liverpool']
# for color,all_points_here,team in zip(colors,[ all_points, all_points2, all_points3, all_points4 ],teams):
# 	all_sum_points = []
# 	for j in range( Matchdays ):
# 		sum_points = 0
# 		for i,points in enumerate(all_points_here):
# 			sum_points += points[j]
# 			plot( [j+1], points[j], color+'o', mfc='none', mec=color, markersize=7.5, alpha=0.5)
# 		all_sum_points.append( sum_points )
# 	plot( range(Matchdays), array(all_sum_points)/len(all_points) , color+'o', markersize=7.5, label=team)

# # tight_layout()
# make_no_frame_legend(loc=0,numpoints=121)
# figure(2); clf()
# # subplot(121)
# # all_points = []
# # symbols = ['o']*7 + ['s']*7
# icount  = 0
# for league_file in ( get_all_EPL_leagues() ):
# 	# print league_file
# 	l = League(league_file)
# 	if ( l.dict_league['Year2'] > 2004):
# 		l.plot_team_position_evolution('Arsenal',linestyle='-'+symbols[icount] )
# 		# all_points.append( l.dict_teams['Arsenal']['points evolution'])
# 		icount += 1
# make_no_frame_legend(loc=0,numpoints=1)

# close(2); close(1);
figure(3); clf()

icount    = 0
all_diffs = []
symbols = ['d','s','o','^','>','x','1','2','3','4']
colors  = ['k','b','g','c','m','y']
for league_file in (get_all_EPL_leagues() ):
	l = League(league_file)
	# print color, league_file
	if ( l.dict_league['Year2']> 2009 ):
		points_evolution = l.dict_teams['Arsenal']['points evolution'] 
		# plot(points_evolution)
		max_points = []
		differences_to_first = []
		for i in range(1,Matchdays+1):
			dict_teams = l.get_dict_teams(Matchdays_selected=range(1,i+1))
			# max_point  = 0
			for team in dict_teams:
				if ( dict_teams[team]['league position'] == 1 ):
					max_point = dict_teams[team]['points']
					break
			max_points.append( max_point )
			differences_to_first.append( max_point - dict_teams['Arsenal']['points'])
		
		# line, = plot(range(1,Matchdays+1),points_evolution,'-o')
		# plot(range(2,Matchdays+1),max_points,'-',color=line.get_color())
		# print icount, len(symbols)
		symbolhere = symbols[icount]
		# plot(range(1,len(points_evolution)+1),array(max_points[:len(points_evolution)])-array(points_evolution),
		# 	'-'+symbolhere,label=l.dict_league['Years'],alpha=0.75,color='k',linewidth=1.0,
		# 	mec='k',mfc='none',markersize=7.5,mew=2.0)

		plot(range(1,len(points_evolution)+1),
			array(max_points[:len(points_evolution)])-array(points_evolution),
			'-',label=l.dict_league['Years'],alpha=0.5,
			color=colors[icount],linewidth=3.0,
			mec='k',mfc='none',markersize=2.5,mew=2.0)

		icount += 1
		# break
		all_diffs.append( differences_to_first )
# print max_points
avg_diffs_by_md = []
for i in range(0,Matchdays):
	sum_diffs = 0
	for diff in all_diffs:
		sum_diffs += diff[i]
	# print all_diffs
	avg_diffs_by_md.append(sum_diffs/len(all_diffs))

plot(range(1,Matchdays+1),avg_diffs_by_md,'ro-',mec='r',label='Average since 2009',linewidth=3.0 )
make_no_frame_legend(loc=0,numpoints=1)
xlabel("Matchday",size=25,style='italic')
ylabel("Points behind leader",size=25,fontproperties=prop_font)
ax = gca()
ax.set_title('@arsfutbolistica',size=30,color='blue',fontproperties=prop_font)
# tight_layout()
ylim([0-.1,25])
xticks( range(5,35+5,5) )
take_off_right_and_top_axis_lines_after()	
# ax = gca()
ax.yaxis.grid()
# tight_layout()

plot_team_logo('Arsenal',[0.5,0.0,0.5,0.5],kwargs=dict(alpha=0.15,origin='upper'))
plot_my_logo([0.0,0.5,0.5,0.5],kwargs=dict(alpha=0.15,origin='upper'))#kwargs=dict(alpha=0.15,origin='upper'))


if ( savefigs == True ):
	savefig('finished_plots/arsenal_leader_points.pdf')
	savefig('finished_plots/arsenal_leader_points.png')
