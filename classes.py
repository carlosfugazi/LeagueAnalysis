execfile('applications_on_parsed_data.py')

class League:
	def __init__(self,filename):
		dict_league = parse_dict( filename )
		self.dict_league = dict_league
		self.filename    = filename
		self.dict_teams  = get_league_table(False,self.filename)
		self.Nteams      = len( self.dict_teams.keys() )
		self.Matchdays   = 2*self.Nteams-2
		self.Teams       = self.dict_teams.keys()
		
	def __str__(self):
		self.print_league_table()
		return ''
	

	def print_league_table(self,Matchdays_selected=None):
		get_league_table(True,self.filename,Matchdays_selected=Matchdays_selected)

	def print_league_table_first_round(self,):
		Matchdays_selected = range(1,self.Matchdays/2+1)
		get_league_table(True,self.filename,Matchdays_selected=Matchdays_selected)

	def print_league_table_second_round(self,):
		Matchdays_selected = range(self.Matchdays/2+1,self.Matchdays+1)
		get_league_table(True,self.filename,Matchdays_selected=Matchdays_selected)

	def get_team_overall_results(self,team):
		data_ = tally_points_gd(self.dict_league,team)
		return data_

	def get_dict_teams(self,Matchdays_selected=None):
		return get_league_table(False,self.filename,Matchdays_selected=Matchdays_selected)

	def plot_team_points_evolution(self,team,linestyle='o-'):
		data_ = self.get_team_overall_results(team)
		plot( range(1,len(data_[9])+1,1),data_[9], linestyle,
			label = team+' {}'.format( self.dict_league['Years'] ), markersize=7.5)
		xlabel('Matchday'); ylabel('Points')
		xlim([1,len(data_[9])])

	def plot_team_position_evolution(self,team,linestyle='o-'):
		# data_ = self.get_team_overall_results(team)
		# plot( range(1,len(data_[9])+1,1),data_[9], linestyle,
		# 	label = team+' {}'.format( self.dict_league['Years'] ), markersize=7.5)
		positions = []
		for i in range(2,self.Matchdays+1):
			dict_teams = get_league_table(False,self.filename,Matchdays_selected=range(1,i+1))
			positions.append( dict_teams[team]['league position'] )
		print positions[-1], self.filename
			# Matcha
		plot( range(2,self.Matchdays+1),positions,linestyle,
			label=team+' {}'.format( self.dict_league['Years'] ), markersize=7.5)
		xlabel('Matchday'); ylabel('League position')
		axvline(x=self.Matchdays/2,linestyle='dashed',color='b')
		# xlim([1,len(data_[9])])
		yticks(range(1,20+1))
		grid(True)
		ylim(0.9,20.1)


		


