#
# analysis of spanish league competiveness
#
def get_all_Leagues():
	fopen = open('csv_detailed_stats/all_spanish_leagues.txt','r')
	Ls = []
	for line in fopen:
		# print line
		try:
			L = League_detailed(line.strip())
			print L.dict_league['Years'], L.dict_teams['Barcelona']['league position'] 
			Ls.append(L)
		except:
			print line.strip(), "not parsable"
	return Ls

	# print dict_['']
def plot_point_distribution_by_place_for_all_leagues():
	for L in Ls[4:]:
		points = []
		for i in range(len(L.Teams)):
			# print i+1
			for team in L.Teams:
				if ( L.dict_teams[team]['league position'] == i+1 ):
					points.append(L.dict_teams[team]['points'])
		print L.dict_league['Years'], len(L.Teams)
		plot(range(1,1+len(L.Teams)),points,alpha=0.25,label=L.dict_league['Years'])
	make_no_frame_legend()

# take_off_right_and_top_axis_lines()

# plot_point_distribution_by_place_for_all_leagues()
try: print(len(Ls))
except: Ls = get_all_Leagues()

all_points, years = [],[]

for L in Ls[4:-1]:
	points = []
	for i in range(len(L.Teams)):
		# print i+1
		for team in L.Teams:
			if ( L.dict_teams[team]['league position'] == i+1 ):
				points.append(L.dict_teams[team]['points'])
	print L.dict_league['Years'], len(L.Teams), L.dict_league['Champion'], L.dict_teams[L.dict_league['Champion']]['points']
	
	# plot(range(1,1+len(L.Teams)),points,alpha=0.25,label=L.dict_league['Years'])
	all_points.append(points)
	years.append(L.dict_league['Years'])

clf()

# for i,points in enumerate(all_points):
# 	plot(i,points[0],'rd')
# 	plot(i,points[1],'bs')
# 	plot(i,points[2],'g^')
# 	plot(i,points[3],'ko')
plot(arange(len(years)),[ points[0] for points in all_points ],'rd-',label='1st')
plot(arange(len(years)),[ points[1] for points in all_points ],'bs-',label='2nd')
plot(arange(len(years)),[ points[2] for points in all_points ],'g^-',label='3rd')
plot(arange(len(years)),[ points[3] for points in all_points ],'ko-',label='4th')
# this plot needs the logo of the champion club above the first place team, really makes the point that when 
# top 4 are close, more likely to get interesting/non-big-2 champion.
xlim(-1,len(years))
ylim(45,105)
xticks( arange(len(years)), years, rotation=70)
ylabel('Points')
grid(True)
# tight_layout()
make_no_frame_legend(loc='lower left')
# plot_team_logo('Arsenal',[0.5,0.0,0.5,0.5],kwargs=dict(alpha=0.15,origin='lower'))
# plot_my_logo([0.0,0.5,0.5,0.5],kwargs=dict(alpha=0.15,origin='lower'))
# plot_team_logo('Barcelona',[0.3,0.75,0.25,0.25],
# 	kwargs=dict(alpha=0.55,origin='lower'))
# plot_team_logo('Real Madrid',[0.1,0.75,0.25,0.25],
# 	kwargs=dict(alpha=0.55,origin='lower'))
# plot_team_logo('Valencia',[0.5,0.75,0.25,0.25],
# 	kwargs=dict(alpha=0.55,origin='lower'))
# plot_team_logo('La Coruna',[0.7,0.75,0.25,0.25],

# 	kwargs=dict(alpha=0.55,origin='lower'))
rcParams['examples.directory'] = '/Users/a209947/Documents/ArsFut/ArsFut_current'


ax= gca()
from matplotlib.cbook import get_sample_data
from matplotlib._png import read_png
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, \
    AnnotationBbox


def put_team_logo_annotationbbox(filename,xy,xybox=(40., +80.)):
	fn = get_sample_data(filename, asfileobj=False)
	arr_lena = read_png(fn)

	imagebox = OffsetImage(arr_lena, zoom=0.02	)
	# xy = [4, 75]
	ab = AnnotationBbox(imagebox, xy,
	                        xybox=xybox,
	                        xycoords='data',
	                        boxcoords="offset points",
	                        pad=0.0,frameon=False,
	                        arrowprops=dict(arrowstyle="->",alpha=.75,linestyle='dashed',
	                                        connectionstyle="angle,angleA=50,angleB=90,rad=3")
	                        )
	ax.add_artist(ab)


filename = "./logos/2000px-Real_Madrid_CF.png"
for xy in [ [3,80],[5,78] ]:
	put_team_logo_annotationbbox(filename,xy)

filename = "./logos/2000px-FCB.png"
for xy in [ [0,74], [1,79] ]:
	put_team_logo_annotationbbox(filename,xy)

filename = "./logos/Valencia_Cf_Logo_original.png"
for xy in [ [4,75], [6,77] ]:
	put_team_logo_annotationbbox(filename,xy)
# filename,xy= "./logos/Valencia_Cf_Logo_original.png"
# put_team_logo_annotationbbox(filename,xy)
filename,xy= "./logos/2000px-RC_Deportivo_La_Coruna_logo.png", [2,69]
put_team_logo_annotationbbox(filename,xy,xybox=(40,140))

plot_team_logo('LaLiga',[0.5,0.0,0.5,0.5],kwargs=dict(alpha=0.15,origin='lower'))
take_off_right_and_top_axis_lines_after()
