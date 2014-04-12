execfile('applications_on_parsed_data.py')

class League:
	def __init__(self,filename):
		dict_league = parse_dict( filename )
		self.dict_league = dict_league
		self.filename    = filename
		self.dict_teams  = get_league_table(False,self.filename)

	def print_league_table(self,):
		get_league_table(True,self.filename)

	def get_team_overall_results(self,team):
		data_ = tally_points_gd(self.dict_league,team)
		return data_

	def plot_team_points_evolution(self,team,linestyle='o-'):
		data_ = self.get_team_overall_results(team)
		plot( range(1,len(data_[9])+1,1),data_[9], linestyle,
			label = team+' {}'.format( self.dict_league['Years'] ), markersize=7.5)
		xlabel('Matchday'); ylabel('Points')
		xlim([1,len(data_[9])])


		


