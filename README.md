# README for ARSFUT analysis

## From git hub repo, initialization stuff

+ git remote add origin https://github.com/carlosfugazi/LeagueAnalysis.git
+ git push -u origin master
+ git pull -u origin master

## Some source websites

+ Website for fonts 
	+ http://www.1001freefonts.com/italic-fonts-4.php
+ Results websites
	+ http://www.worldfootball.net/alle_spiele/ita-serie-a-2011-2012/
	+ http://www.worldfootball.net/alle_spiele/esp-primera-division-2011-2012/
	+ http://www.worldfootball.net/alle_spiele/fra-ligue-1/
	+ http://www.worldfootball.net/alle_spiele/bundesliga/
	+ http://www.premierleague.com/en-gb/matchday/results.html?paramComp_100=true&view=.dateSeason
	+ http://football-data.co.uk/englandm.php
	
## Code Structure

+ league_table_parsing.py
	- Parses the base csv data in ./csv_data/
		+ Produces the necessary league dictionary from these files
		+ Also produces the subsidiary dict based on the teams (every key is a team with their table information)
+ applications_on_parsed_data.py
		- Prints league tables, plots... etc...
+ classes.py
	- Creates a league class object going to be improved considerably.
		+ Already can print table, plot league position and points evolution as well

## League dict keys
 
+ Major keys in league dictionary object
	- dict_['League Name'] = LEAGUENAME
 	- dict_['Country'] = COUNTRY
 	- dict_['Years'] = YEARS
 	- dict_['Year1'] = int(YEARS.split('-')[0])
 	- dict_['Year2'] = int(YEARS.split('-')[1])
 	- dict_['N_games'] = len(dict_['Home Team'])
 	- Basic column structure of csv files: 
 		- 'Matchday,Home Team,Away Team,Goals Home,Goals Away,Points Home,Points Away']

## Teams dict 

+ Dict team (generated from league table data)
	- Code sample of definition: 
		`dict_teams[team] = {'points':point_totals[i],
 		'goal difference':goal_differences[i],
 		'league position':position, 'goals for':goals_for[i], 
 		'goals against':goals_against[i], 'home points':points_home[i],
 		'away points':points_away[i],
 		'wins':wins[i],'draws':draws[i],'loses':loses[i]}`

