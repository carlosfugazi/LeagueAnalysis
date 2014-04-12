# League table parsing
from difflib import get_close_matches
import time

_BL_league_file_test = 'csv_data/BL_2009_2010.csv'
_EPL_league_file_test = 'csv_data/EPL_2009_2010.csv'

execfile('custom_utilities/custom_utilities.py')
#def index_rank_high_to_low(list1): # move to custompy
#	list_ranked_indices = [i[0] for i in sorted(enumerate(list1),
#		key=lambda x:x[1])]
#	list_ranked_indices = list_ranked_indices[::-1]
#	return list_ranked_indices

#def index_rank_low_to_high(list1): # move to custompy
#	list_ranked_indices = [i[0] for i in sorted(enumerate(list1),
#		key=lambda x:x[1])]
#	#list_ranked_indices = list_ranked_indices[::-1]
#	return list_ranked_indices
def logout():
	update_all_master_lists()
	make_pdf_ideas()
	git_backup()
	package_project()
	# "pandoc -o ideas_{}.pdf ideas_for_ars_futbolistica_graphs.md".format(
	# 	time.strftime('%Y_%m_%d'))

def package_project():
	print " BACKING UP TO TAR.GZ"
	files = '*.csv *.txt *.py *.ods *.xls *.md */*.svg */*.csv */*.py */*.txt */*.png */*.xls */*.ods */*.md'
	runcmd('tar -cvf "ArsFut_{}.tar" {}'.format( time.strftime('%Y_%m_%d'),files ))
	runcmd('gzip ArsFut_{}.tar'.format( time.strftime('%Y_%m_%d')))

def mode(list1):
	uniques = list(set(list1))
	max_freq = 0
	for unique in uniques:
		if ( list1.count(unique) > max_freq ):
			max_freq         = list1.count(unique)
			max_freq_element = unique
	return max_freq_element

def git_backup():
	runcmd('git add *.csv *.txt *.py *.md *.svg */*.svg */*.csv */*.py */*.txt */*.md')
	runcmd('git commit -a')
	
def update_all_master_lists():
	for abbreviation in ['EPL','BL','SerieA','LaLiga','Ligue1']:
		runcmd('ls csv_data/{0}*.csv > {0}_list_of_leagues_parsed.txt'.format(abbreviation))
		print abbreviation
		runcmd('cat {0}_list_of_leagues_parsed.txt'.format(abbreviation))

def make_pdf_ideas():
	runcmd("pandoc -o ideas_{}.pdf ideas_for_ars_futbolistica_graphs.md".format(
		time.strftime('%Y_%m_%d')) )

def parse_matrix_of_results_test():
	fopen = open('EPL_raw_matrix_2011-2012.csv','r')
	lines = [ line.strip('\n') for line in fopen.readlines() ]
	fopen.close()
	#
	# get teams
	#
	teams   = []
	results_strs = []
	for line in lines[1:]:
		teams.append(line.split(',')[0])
		results_for_team = [ 
			element.replace('\xe2\x80\x93','-') for element in line.split(',')[1:] ]
		results_strs.append( results_for_team )
	
	#print len(results[0]),results[0]
	j = 1
	points = 0
	for i,result in enumerate(results_strs[j]):
		if ( i == j ): 
			pass
		else:
			target_team_goals = int(result.split('-')[0])
			opponent_team_goals =  int(result.split('-')[1])
			points += determine_home_points(target_team_goals,opponent_team_goals)
	#print "home pts = ", points 	
	for i, result in enumerate(results_strs):
		result = result[j]
		if (i == j):
			pass
		else:
			target_team_goals = int(result.split('-')[0])
			opponent_team_goals =  int(result.split('-')[1])
			points += determine_away_points(target_team_goals,opponent_team_goals)
	
	#print "away pts = ", points
	#print target_team_goals > opponent_team_goals
	#print  len(lines[1].split(',')), [ str(element) for element in 
		#lines[1].split(',') ]
	print "Total points ", points, " for ", teams[j]
	
def analyze_file_name(filename):
	year1 = int( filename.replace('.csv','').split('_')[-2] )
	year2 = int( filename.replace('.csv','').split('_')[-1] )
	if ( filename.find('EPL') != -1 ):
		return 'EPL','English Premier League','England',year1, year2
	elif ( filename.find('LaLiga') != -1 ):
		return 'LaLiga','La Liga','Spain',year1, year2
	elif ( filename.find('BL') != -1 ):
		return 'BL','Bundesliga','Germany',year1, year2
	elif ( filename.find('Ligue1') != -1 ):
		return 'Ligue1','Ligue 1','France',year1, year2	
	elif ( filename.find('SerieA') != -1 ):
		return 'SerieA','Seria A','Italy',year1, year2
	
def test_matchday_raw_html_style():
	matchday_raw_html_style('XLS_data/BL_raw_matchday_html_2010_2011.csv')	


def matchday_raw_html_style(filename):	
	# England : http://www.worldfootball.net/alle_spiele/eng-premier-league-2011-2012/
	# Spain   : http://www.worldfootball.net/alle_spiele/esp-primera-division-2011-2012/
	"""
	format: (note that csv is needed for string separation)
		LEAGUE NAME, COUNTRY, YEAR1-YEAR2
		Matchday,Home Team,Away Team,Goals Home,Goals Away,Points Home,Points Away
		[INT],[STR],[STR],[INT],[INT],[INT],[INT]
	...

	"""
	# filename = 'XLS_data/BL_raw_matchday_html_2010_2011.csv'
	
	LEAGUE_ABBRV, LEAGUE_NAME, COUNTRY, YEAR1, YEAR2 = analyze_file_name(filename)
	strings_categories = ['Matchday', 'Date', 'Result']
	#fopen = open('XLS_data/EPL_raw_matchday_html_2011_2012.csv','r')
	fopen = open(filename,'r')
	lines = fopen.readlines()
	fopen.close()
	#fopen 
	#fopen = open('csv_data/EPL_2011_2012.csv','w')
	#fopen.write('{},{},{}-{}\n'.format('English Premier League','England',2011,2012))
	
	fopen = open('csv_data/{}_{}_{}.csv'.format(LEAGUE_ABBRV,YEAR1,YEAR2),'w')
	fopen.write('{},{},{}-{}\n'.format(LEAGUE_NAME,COUNTRY,YEAR1,YEAR2))
	
	
	fopen.write('Matchday,Home Team,Away Team,Goals Home,Goals Away,Points Home,Points Away\n')
	for line in lines:
		if ( line.find('Round') != -1 ):
			#print 'Matchday ', line.split('.')[0]
			current_match_day = int(line.split('.')[0])
		if ( line.split(',')[0].find(':') != -1 ):
			elements = line.split(',')
			result_str = elements[4]
			home_goals = ((result_str.split(' (')[0]).split(':'))[0]
			away_goals = ((result_str.split(' (')[0]).split(':'))[1]
			fopen.write( '{},{},{},{},{},{},{}\n'.format(current_match_day, elements[1],elements[3],
				home_goals,away_goals,\
				determine_home_points(home_goals,away_goals),
				determine_away_points(home_goals,away_goals) ) )
	fopen.close()
	#print current_match_day 
	
def find_similar_team_name(team,league_file):
	dict_teams= get_league_table(False,league_file)
	# print get_close_matches(team,dict_teams.keys())[0]
	try:
		match = get_close_matches(team,dict_teams.keys())[0]
	except:
		match = None
	return match

def modify_team_name_to_match(team,league_file,**kwargs):
	auto = parse_kwargs('auto',False,**kwargs)
	match = find_similar_team_name(team,league_file)
	dict_team = get_league_table(False,league_file)
	if ( dict_team.has_key(team) != True ):
		if ( auto == False and match != None ): 
			choice = raw_input('Accept new choice [{}] for [{}], (y/n) : '.format(match,team))
			if ( choice == 'y'):
				return match
			else:
				return team
		elif ( auto == True and match != None ):
			return match
		else:
			return team
	else:
		return team

def get_attribute_as_function_of_league_year(team,league_file,attr):
	dict_league = parse_dict(league_file)
	dict_team = get_league_table(False,league_file)
	match = modify_team_name_to_match( team,league_file, auto=True )
	if ( dict_team.has_key(match) == True ):
		return dict_team[match][attr], dict_league['Year2']
	else:
		return None, None

def get_attribute_for_range_of_leagues(team,league_files,attr):
	attrs = []
	years = []
	for file1 in league_files:
		attr_, year_ = get_attribute_as_function_of_league_year(team,file1,attr)
		if ( attr_ != None ): 
			attrs.append(attr_);
			years.append(year_);
	return attrs, years 

def return_type(str1, type1):
	if (type1 == 'str' ): return str(str1)
	elif (type1 == 'int' ): return int(str1)
	elif (type1 == 'float' ): return float(str1)

def obtain_unique_elements(list1):
	uniques = [ list1[0] ]
	for element in list1:
		if ( element not in uniques ):
			uniques.append( element )
	return uniques

def parse_master_BL_9697_0910_list():
	parse_master_general_list('master_BL_list_9697_0910.csv','BL',
		'Bundesliga','Germany')

def parse_master_EPL_9697_0910_list():
	parse_master_general_list('master_EPL_list_9697_0910.csv','EPL',
		'English Premier League','England')

def parse_master_general_list(file_master,league_code,league_name,country):
	def formatted_line(line_old):
		elements = line_old.split(',')
	fopen = open(file_master,'r')
	lines= fopen.readlines()
	fopen.close()
	# print (lines[0]).split(',')
	seasons = []
	for line in lines[1:]:
		season = line.split(',')[0]
		if ( season not in seasons ): seasons.append(season)
	print league_code+" Seasons found: ", seasons
	# old format  0 Season,1 Matchday,2 ,3 Home Team,4 Away Team,5 Goals Home, 6 Goals Away
	for season in seasons:
		# print season.split('/'), season
		fopen = open("csv_data/"+league_code+"_{}_{}.csv".format(*season.split('/')),'w')
		season_lines = []
		for line in lines[1:]:
			if ( line.find(season) != -1 ):
				season_lines.append(line)
		fopen.write('{},{},{}-{}\n'.format(
			*([league_name,country]+season.split('/'))))
		# new format
		fopen.write('Matchday,Home Team,Away Team,Goals Home,Goals Away,Points Home,Points Away\n')
		for i,line in enumerate(season_lines):
			elements = line.split(',')
			home_goals,away_goals = int(elements[5]),int(elements[6])
			pts_home, pts_away = determine_home_points(home_goals,away_goals), determine_away_points(home_goals,away_goals)
			elements_to_write = [int(elements[1]), elements[3], elements[4], home_goals,away_goals, pts_home, pts_away ]
			fopen.write('{},{},{},{},{},{},{}\n'.format(*elements_to_write))
		#  Matchday,Home Team,Away Team,Goals Home,Goals Away,Points Home,Points Away
		#  EX of new formatting 1,Aston Villa,West Ham United,3,0,3,0
		fopen.close()

def parse_dict(filename):
	"""
	format: (note that csv is needed for string separation)
		LEAGUE NAME, COUNTRY, YEAR1-YEAR2
		Matchday,Home Team,Away Team,Goals Home,Goals Away,Points Home,Points Away
		[INT],[STR],[STR],[INT],[INT],[INT],[INT]
	...

	"""
	dict_ = {}
	fopen = open(filename,'r')
	lines = fopen.readlines()
	fopen.close()

	lines = [ line.strip() for line in lines ]
	LEAGUENAME = lines[0].split(',')[0]
	COUNTRY    = lines[0].split(',')[1]
	YEARS      = lines[0].split(',')[2]
	dict_['League Name'] = LEAGUENAME
	dict_['Country'] = COUNTRY
	dict_['Years'] = YEARS
	dict_['Year1'] = int(YEARS.split('-')[0])
	dict_['Year2'] = int(YEARS.split('-')[1])

	header_line = lines[1]
	header_keys = header_line.split(',')
	header_types = ['int','str','str','int','int','int','int']
	
	HEADERSTRINGS = 2

	for header in header_keys:
		dict_[header] = []
	for line in lines[HEADERSTRINGS:]:
		line_elements = line.split(',')
		for i,header in enumerate(header_keys):
			dict_[header].append( return_type(line_elements[i],header_types[i]) )
	# print header
	dict_['N_games'] = len(dict_['Home Team'])
	
	fopen = open('logos/league_logo_def.csv','r')
	# print LEAGUENAME
	# runcmd('cat logos/league_logo_def.csv')
	# stop

	lines = fopen.readlines()
	fopen.close()
	for i,line in enumerate(lines):
		if ( line.find(LEAGUENAME) != -1 ):
			logo_file = line.split(',')[1]
			dict_['Logo file'] = logo_file.strip()
			break
		

	# dict_['logo']    = 
	# dict_['Total_away_points']
	return dict_

def list_matches(team,opponent_teams,filename):
	def get_res_symbol_and_points(home_goal,away_goal):
		if ( home_goal > away_goal ):
			return 'W',3
		elif ( home_goal == away_goal ):
			return 'D',1
		else:
			return 'L',0

	dict_ = parse_dict(filename)
	# print dict_.keys()
	dict_teams = get_league_table(False,filename)
	# print opponent_teams
	if ( opponent_teams == None):
		opponent_teams = dict_teams.keys()
		opponent_teams.remove(team)
	i = 0
	test_str1 = "\n\tMatchday {:2} Res. {} : {:20} {} - {} {:>20}".format(0, 'L', dict_['Home Team'][i], dict_['Goals Home'][i], 
						dict_['Goals Away'][i], dict_['Away Team'][i])

	print '='*(len(test_str1)+7)
	print "Matches against the specified opposition for {}".format(team)
	print "\t# of opponent teams", len(opponent_teams)
	# print "	", opponent_teams
	pts_total = 0
	print '-'*(len(test_str1)+7)
	for i,matchday in enumerate(dict_['Matchday']):
		if ( team == dict_['Away Team'][i] or team == dict_['Home Team'][i]):
			for opponent in opponent_teams:
				if ( opponent in [dict_['Away Team'][i],dict_['Home Team'][i]] and 
					opponent is not team ):
					if ( team == dict_['Away Team'][i]):
						team_goal = dict_['Goals Away'][i]
						opponent_goal = dict_['Goals Home'][i]
					else:
						team_goal = dict_['Goals Home'][i]
						opponent_goal = dict_['Goals Away'][i]
					res, pts = get_res_symbol_and_points(team_goal,opponent_goal)
					pts_total += pts
					print "\tMatchday {:2} Res. {} : {:20} {} - {} {:>20}".format(matchday, res, dict_['Home Team'][i], dict_['Goals Home'][i], 
						dict_['Goals Away'][i], dict_['Away Team'][i])
	print "\t\tTotal points against this opposition: ", pts_total
	print '-'*(len(test_str1)+7)
	print '='*(len(test_str1)+7)
	print '\n'
	# print str1

def determine_home_points(home_goals,away_goals):
	if ( home_goals > away_goals ):
		return 3
	elif ( home_goals == away_goals ):
		return 1
	elif ( home_goals < away_goals ):
		return 0

def determine_away_points(home_goals,away_goals):
	if ( home_goals > away_goals ):
		return 0
	elif ( home_goals == away_goals ):
		return 1
	elif ( home_goals < away_goals ):
		return 3

def tally_points_gd(dict_,team,Matchdays_selected=None):
	N_games = dict_['N_games']
	points          = 0
	goal_difference = 0
	goals_for       = 0
	goals_against   = 0
	points_away     = 0
	points_home     = 0
	wins  = 0
	draws = 0
	loses = 0
	total_points_per_match, goals_for_per_match, goals_diff_per_match = [], [], []
	for i in range(N_games):
		Matchday = dict_['Matchday'][i]
		if ( Matchdays_selected == None ):
			select_match = True
		else:
			select_match = ( Matchday in Matchdays_selected ) 

		if ( select_match == True and dict_['Home Team'][i] == team ):
			# print dict_['Matchday'][i]
			home_goals, away_goals = dict_['Goals Home'][i], dict_['Goals Away'][i]
			points_match = determine_home_points(home_goals,away_goals)
			points = points + points_match
			goal_difference = goal_difference + (home_goals-away_goals)
			goals_for += home_goals
			goals_against -= away_goals
			points_home += points_match
			total_points_per_match.append( points)
			goals_for_per_match.append(    goals_for )
			goals_diff_per_match.append(   goal_difference )			

			if ( points_match == 3):
				wins +=  1
			elif ( points_match == 1):
				draws += 1
			elif ( points_match == 0):
				loses += 1
			else:
				raise ValueError, "Not valid result obtained from parse"
			# print 'Home ', dict_['Matchday'][i], points_match
		elif ( select_match == True and dict_['Away Team'][i] == team ):
			# print dict_['Matchday'][i]
			home_goals, away_goals = dict_['Goals Home'][i], dict_['Goals Away'][i]
			points_match = determine_away_points(home_goals,away_goals)
			points = points + points_match
			goal_difference = goal_difference + (away_goals-home_goals)
			goals_for += away_goals
			goals_against -= home_goals
			points_away += points_match
			total_points_per_match.append(points)

			if ( points_match == 3):
				wins += 1
			elif ( points_match == 1):
				draws += 1
			elif ( points_match == 0):
				loses += 1
			else:
				raise ValueError, "Not valid result obtained from parse"
			
			# print 'Away', dict_['Matchday'][i], points_match
		else:			pass
	return points,goal_difference,goals_for,abs(goals_against),\
		points_home,points_away,wins,draws,loses,\
		total_points_per_match, goals_for_per_match,goals_diff_per_match

def print_league_table(dict_,dict_teams):
	N_cats = 10
	max_team_character = 0
	for i,team in enumerate(dict_teams.keys()): max_team_character = max(len(team),max_team_character) 
	#print max_team_character
	format_str = "| {{:4}} | {{:{}}} | ".format(max_team_character) +("{:3} | "*N_cats)
	N_string_cols = len( format_str.format(*(['-'*4]+['-'*max_team_character]+['-'*3]*N_cats))  )
	print '='*N_string_cols
	print ("{:^"+str(N_string_cols)+"}").format( "{1} : {0} Table".format(
		dict_['League Name'],dict_['Years']) )
	print '='*N_string_cols
	print '-'*N_string_cols
	
	print  (format_str).format(*['Pos', 'Team','P','W','D','L',
		'GF','GA','GD','HP','AP','Pts'])
	print (format_str).format(*(['-'*4]+['-'*max_team_character]+['-'*3]*N_cats))
	
	N_teams = len(dict_teams.keys())
	
	#dict_teams[team] = {'points':point_totals[i],
			#'goal difference':goal_differences[i],
			#'league position':position, 'goals for':goals_for[i], 
			#'goals against':goals_against[i], 'home points':points_home[i],
			#'away points':points_away[i],
			#'wins':wins[i],'draws':draws[i],'loses':loses[i]}
	
	position_to_print = 1
	
	for j in range(N_teams):
		for i,team in enumerate(dict_teams.keys()):
			if ( dict_teams[team]['league position'] == position_to_print ):
				print (format_str).format(*[position_to_print,\
					team,len(dict_teams[team]['points evolution']),
					dict_teams[team]['wins'], dict_teams[team]['draws'],\
					dict_teams[team]['loses'], \
					dict_teams[team]['goals for'],\
					dict_teams[team]['goals against'],\
					dict_teams[team]['goal difference'],\
					dict_teams[team]['home points'],\
					dict_teams[team]['away points'],\
					dict_teams[team]['points']] )
				position_to_print += 1
	print '-'*N_string_cols

def get_all_EPL_leagues():
	files = [ file1.strip() for file1 in (open('EPL_list_of_leagues_parsed.txt','r')).readlines() ]
	return files

def get_ranking_based_on_points(point_totals,goal_differences,goals_for):	
	point_total_indeces  = index_rank_high_to_low(point_totals     )
	goal_diff_indeces    = index_rank_high_to_low(goal_differences )

	conflicts 	         = []
	points_of_conflict   = []
	
	unique_point_totals = []
	repeated_teams_by_points = []
	for i,point in enumerate(point_totals):
		if point not in unique_point_totals:
			unique_point_totals.append(point)
			repeated_teams_by_points.append([i])
		else:
			for j,point2 in enumerate(unique_point_totals):
				if point2 == point:
					repeated_teams_by_points[j].append(i)
	unique_GD_totals = []
	repeated_teams_by_GD = []
	for i,GD in enumerate(goal_differences):
		if GD not in unique_GD_totals:
			unique_GD_totals.append(GD)
			repeated_teams_by_GD.append([i])
		else:
			for j,GD2 in enumerate(unique_GD_totals):
				if GD2 == GD:
					repeated_teams_by_GD[j].append(i)

	mod_points           = array([1.0*point for point in point_totals]);
	maxpoints_modifier   = 10.0*max(abs(array(goal_differences)))
	maxpoints_modifier_2 = 100.0*max(abs(array(goals_for)))
	# print maxpoints_modifier
	for i,point in enumerate(unique_point_totals):
		if ( len(repeated_teams_by_points[i]) > 1):
			# print  repeated_teams_by_points[i]
			for j in repeated_teams_by_points[i]:
				# print mod_points[j], 1.0*goal_differences[j]/maxpoints_modifier
				tied_in_GD = False
				for k, GD in enumerate(unique_GD_totals):
					if ( len(repeated_teams_by_GD[k]) > 1 ):
						test_teams = repeated_teams_by_points[i]
						for l in repeated_teams_by_points[i]:
							if ( j != l and l in repeated_teams_by_GD[k] ):
								neighbor_is_too = True
							else:
								neighbor_is_too = False
						if ( j in repeated_teams_by_GD[k] and neighbor_is_too == True ):
							tied_in_GD = True
				if ( tied_in_GD == True ):
					mod_points[j] = mod_points[j] + 1.0*goal_differences[j]/maxpoints_modifier + \
						1.0*goals_for[j]/maxpoints_modifier_2
				else:
					mod_points[j] = mod_points[j] + 1.0*goal_differences[j]/maxpoints_modifier

	mod_points           = list(mod_points)
	point_total_indeces  = index_rank_high_to_low( mod_points  )

	return mod_points, point_total_indeces

def get_dict_teams(teams,point_total_indeces,point_totals,goal_differences,\
	goals_for,goals_against,points_home,points_away,wins,draws,loses,\
	points_evolution,goals_for_evolution,goals_diffs_evolution,lines_teams):
	dict_teams = {}
	for i,team in enumerate(teams):
		for j, index in enumerate(point_total_indeces):
			if ( index == i): position = j+1
		
		dict_teams[team] = {
			'points':point_totals[i],
			'goal difference':goal_differences[i],
			'league position':position, 
			'goals for':goals_for[i], 
			'goals against':goals_against[i], 
			'home points':points_home[i],
			'away points':points_away[i],
			'wins':wins[i],'draws':draws[i],'loses':loses[i],
			'points evolution':points_evolution[i],
			'goals for evolution':goals_for_evolution[i],
			'goals difference evolution':goals_diffs_evolution[i]
			}
		
		for j,line in enumerate(lines_teams):
			if ( line.find(team) != -1 ):
				team_logo_file = line.split(',')[1]
				dict_teams[team]['logo file'] = team_logo_file.strip()
				break

	return dict_teams

def get_league_table(print_bool,filename,Matchdays_selected=None):
	dict_ = parse_dict(filename)
	teams = obtain_unique_elements(dict_['Home Team'])
	# print len(teams), teams
	# teams_ = ['Manchester United','Chelsea','Manchester City','Arsenal','Tottenham Hotspur','Blackburn Rovers']
	point_totals     = []
	goal_differences = []
	goals_for        = []
	goals_against    = []
	points_away      = []
	points_home      = []
	wins = []; draws = []; loses = []
	points_evolution, goals_for_evolution, goals_diffs_evolution = [], [], []
	for team in teams:
		# print team, "points = ", tally_points(dict_,team)
		values = tally_points_gd(  dict_,team,Matchdays_selected=Matchdays_selected)
		point_totals.append(     values[0]  )
		goal_differences.append( values[1]  )
		goals_for.append(        values[2]  )
		goals_against.append(    values[3]  )
		points_home.append(      values[4]  )
		points_away.append(      values[5]  )
		#
		# types of results
		#
		wins.append(  values[6]  )
		draws.append( values[7]  )
		loses.append( values[8]  )	
		points_evolution.append( values[9] )
		goals_for_evolution.append(  values[10]  )
		goals_diffs_evolution.append( values[11] )
	# points,goal_difference,goals_for,goals_against,points_home,points_away

	mod_points, point_total_indeces = get_ranking_based_on_points(point_totals,
		goal_differences,goals_for)

	fopen = open('logos/team_logo_def.csv','r')
	lines_teams = fopen.readlines()
	fopen.close()

	dict_teams = get_dict_teams(teams,point_total_indeces,point_totals,goal_differences,
		goals_for,goals_against,points_home,points_away,wins,draws,loses,points_evolution,
			goals_for_evolution,goals_diffs_evolution,lines_teams)
	if ( print_bool == True ): print_league_table(dict_,dict_teams)
	return dict_teams
	

# dict_ = get_league_table()
# filename = 'EPL_2010_2011.csv'
# TEAMS1 =  ['Arsenal','Manchester United',\
# 		'Manchester City','Tottenham Hotspur', 'Chelsea']

# print TEAMS1
# for target_team in TEAMS1:
# 	# TEAMS = TEAMS1
# 	list_matches(target_team,TEAMS1,filename )
# # need a general method to untangle equal point totals and GD, goals for (more would be insane, rare right?)
# parse_master_EPL_9697_0910_list()
