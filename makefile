backup:
	git add ./\*.py ./\*.txt ./\*.csv ./\*.ods
	
define_remote:
	git remote add origin https://github.com/carlosfugazi/LeagueAnalysis.git
	
push:
	git push origin master

pull:
	git pull origin master
