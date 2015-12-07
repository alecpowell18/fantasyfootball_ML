import csv
from collections import defaultdict

abbrvs = {"New Orleans Saints":"NO", "Pittsburgh Steelers":"PIT", "New England Patriots":"NE",
	"New York Jets":"NYJ", "Miami Dolphins":"MIA", "Buffalo Bills":"BUF", "Baltimore Ravens":"BAL",
	"Cleveland Browns":"CLE", "Cincinnati Bengals":"CIN", "Houston Texans":"HOU", "Indianapolis Colts":"IND",
	"Jacksonville Jaguars":"JAX", "Tennessee Titans":"TEN", "Denver Broncos":"DEN", "Kansas City Chiefs":"KC",
	"San Diego Chargers":"SD", "Oakland Raiders":"OAK", "Dallas Cowboys":"DAL", "Washington Redskins":"Was",
	"New York Giants":"NYG", "Philadelphia Eagles":"PHI", "Minnesota Vikings":"MIN", "Green Bay Packers":"GB",
	"Detroit Lions":"DET", "Chicago Bears":"CHI", "Tampa Bay Buccaneers":"TB", "Atlanta Falcons":"ATL",
	"Carolina Panthers":"CAR", "San Francisco 49ers":"SF", "Seattle Seahawks":"SEA", "Arizona Cardinals":"ARZ",
	"St. Louis Rams":"STL", "St":"STL"}


def getDefLib():
	defense_stats = []
	steam_names = []
	defense_parameters = []
	Def_Lib = defaultdict(lambda: defaultdict(dict))

	defense = open('Defense.csv.csv', 'rU')
	defense_read = csv.reader(defense, dialect=csv.excel_tab)
	for param in defense_read.next()[0].split(','):
		defense_parameters.append(param)

	Week = 1
	for line in defense:
		if "Week" not in line:
			single_params = line.split(',')
			team_name = abbrvs[single_params[0].split('. ')[1]]

			Def_Lib[Week][team_name]["Sacks"] = single_params[2]
			Def_Lib[Week][team_name]["Recovered_Fumbles"] = single_params[3]
			Def_Lib[Week][team_name]["Ints"] = single_params[4]
			Def_Lib[Week][team_name]["DefTD"] = single_params[5]
			Def_Lib[Week][team_name]["PA"] = single_params[6]
			Def_Lib[Week][team_name]["PaYd"] = single_params[7]
			Def_Lib[Week][team_name]["RuYd"] = single_params[8]
			Def_Lib[Week][team_name]["Safeties"] = single_params[9]
			Def_Lib[Week][team_name]["DefTD"] = single_params[10]
			Def_Lib[Week][team_name]["FanPts"] = single_params[11]
		else:
			Week += 1
	return Def_Lib

def getTeamList(Def_Lib):
	Teams = []
	for team in Def_Lib[1]:
		print team
		Teams.append(team)
	return Teams

def getCumDefLib(Def_Lib, Teams):
	Cum_Def_Lib = defaultdict(lambda: defaultdict(dict))
	for Week in Def_Lib:
		for Team in Teams:
			if Team in Def_Lib[Week]:
				Cum_Def_Lib[Week][Team]["Bye"] = False
				Cum_Def_Lib[Week][Team]["TotalGames"] = 0
				Cum_Def_Lib[Week][Team]["Sacks"] = 0
				Cum_Def_Lib[Week][Team]["Recovered_Fumbles"] = 0
				Cum_Def_Lib[Week][Team]["Ints"] = 0
				Cum_Def_Lib[Week][Team]["DefTD"] = 0
				Cum_Def_Lib[Week][Team]["PA"] = 0
				Cum_Def_Lib[Week][Team]["PaYd"] = 0
				Cum_Def_Lib[Week][Team]["RuYd"] = 0
				Cum_Def_Lib[Week][Team]["Safeties"] = 0
				Cum_Def_Lib[Week][Team]["DefTD"] = 0
				Cum_Def_Lib[Week][Team]["FanPts"] = 0
			else:
				Cum_Def_Lib[Week][Team]["Bye"] = True
			if Team == "Seattle Seahawks":
				print "Week is " + str(Week)
				print str(Cum_Def_Lib[Week][Team]["Bye"])

	for Team in Teams:
		Cum_Def_Lib[0][Team]["Bye"] = False
		Cum_Def_Lib[0][Team]["TotalGames"] = 0
		Cum_Def_Lib[0][Team]["Sacks"] = 0
		Cum_Def_Lib[0][Team]["Recovered_Fumbles"] = 0
		Cum_Def_Lib[0][Team]["Ints"] = 0
		Cum_Def_Lib[0][Team]["DefTD"] = 0
		Cum_Def_Lib[0][Team]["PA"] = 0
		Cum_Def_Lib[0][Team]["PaYd"] = 0
		Cum_Def_Lib[0][Team]["RuYd"] = 0
		Cum_Def_Lib[0][Team]["Safeties"] = 0
		Cum_Def_Lib[0][Team]["DefTD"] = 0
		Cum_Def_Lib[0][Team]["FanPts"] = 0

	for Week in Def_Lib:
		for Team in Teams:
			if(Cum_Def_Lib[Week][Team]["Bye"] == False):
				Cum_Def_Lib[Week][Team]["TotalGames"] = Cum_Def_Lib[Week-1][Team]["TotalGames"] + 1
				TotalGames = Cum_Def_Lib[Week][Team]["TotalGames"]
				Cum_Def_Lib[Week][Team]["Sacks"] = int(Def_Lib[Week][Team]["Sacks"]) + Cum_Def_Lib[Week-1][Team]["Sacks"]
				Cum_Def_Lib[Week][Team]["avg_Sacks"] = Cum_Def_Lib[Week][Team]["Sacks"]/float(TotalGames)
				Cum_Def_Lib[Week][Team]["Recovered_Fumbles"] + int(Def_Lib[Week][Team]["Recovered_Fumbles"]) + Cum_Def_Lib[Week-1][Team]["Recovered_Fumbles"]
				Cum_Def_Lib[Week][Team]["avg_Recovered_Fumbles"] = Cum_Def_Lib[Week][Team]["Recovered_Fumbles"]/float(TotalGames)
				Cum_Def_Lib[Week][Team]["Ints"] = int(Def_Lib[Week][Team]["Ints"]) + Cum_Def_Lib[Week-1][Team]["Ints"]
				Cum_Def_Lib[Week][Team]["avg_Ints"] = Cum_Def_Lib[Week][Team]["Ints"]/float(TotalGames)
				Cum_Def_Lib[Week][Team]["DefTD"] = int(Def_Lib[Week][Team]["DefTD"]) + Cum_Def_Lib[Week-1][Team]["DefTD"]
				Cum_Def_Lib[Week][Team]["avg_DefTD"] = Cum_Def_Lib[Week][Team]["DefTD"]/float(TotalGames)
				Cum_Def_Lib[Week][Team]["PA"] = int(Def_Lib[Week][Team]["PA"]) + Cum_Def_Lib[Week-1][Team]["PA"]
				Cum_Def_Lib[Week][Team]["avg_PA"] = Cum_Def_Lib[Week][Team]["PA"]/float(TotalGames)
				Cum_Def_Lib[Week][Team]["PaYd"] = int(Def_Lib[Week][Team]["PaYd"]) + Cum_Def_Lib[Week-1][Team]["PA"]
				Cum_Def_Lib[Week][Team]["avg_PaYd"] = Cum_Def_Lib[Week][Team]["PaYd"]/float(TotalGames)
				Cum_Def_Lib[Week][Team]["RuYd"] = int(Def_Lib[Week][Team]["RuYd"]) + Cum_Def_Lib[Week-1][Team]["RuYd"]
				Cum_Def_Lib[Week][Team]["avg_RuYd"] = Cum_Def_Lib[Week][Team]["RuYd"]/float(TotalGames)
				Cum_Def_Lib[Week][Team]["Safeties"] = int(Def_Lib[Week][Team]["Safeties"]) + Cum_Def_Lib[Week-1][Team]["Safeties"]
				Cum_Def_Lib[Week][Team]["avg_Safeties"] = Cum_Def_Lib[Week][Team]["Safeties"]/float(TotalGames)
				Cum_Def_Lib[Week][Team]["DefTD"] += int(Def_Lib[Week][Team]["DefTD"]) + Cum_Def_Lib[Week-1][Team]["DefTD"]
				Cum_Def_Lib[Week][Team]["avg_DefTD"] = Cum_Def_Lib[Week][Team]["DefTD"]/float(TotalGames)
				Cum_Def_Lib[Week][Team]["FanPts"] += int(Def_Lib[Week][Team]["FanPts"]) + Cum_Def_Lib[Week-1][Team]["FanPts"]
				Cum_Def_Lib[Week][Team]["avg_FanPts"] = Cum_Def_Lib[Week][Team]["FanPts"]/float(TotalGames)
			else:
				for component in Cum_Def_Lib[Week-1][Team]:
					if component != "Bye":
						Cum_Def_Lib[Week][Team][component] = Cum_Def_Lib[Week-1][Team][component]
	return Cum_Def_Lib

def getTeamRanking(team, week):
	Def_Lib = getDefLib()
	Teams = getTeamList(Def_Lib)
	print Teams
	Cum_Def_Lib = getCumDefLib(Def_Lib, Teams)

def getSchedule(Teams):
	schedule_raw = open('Schedule.csv', 'rU')
	schedule_lines = csv.reader(schedule_raw, dialect=csv.excel_tab)
	schedule = defaultdict(dict)
	bye = {}
	week = 0
	for line in schedule_lines:
		info = line[0].split(',')
		if info[0] != "Week":
			schedule[week][abbrvs[info[4]]] = abbrvs[info[6]]
			schedule[week][abbrvs[info[6]]] = abbrvs[info[4]]
		else:
			if(week != 0):
				for team in Teams:
					if team not in schedule[week]:
						schedule[week][team] = "BYE"
						bye[team] = week
			week += 1
	return (schedule, bye)

def getTrueWeek(bye, perfnum, team):
	bye_game = int(bye[team])
	if bye_game > perfnum:
		return perfnum
	else:
		return perfnum + 1

def getDefenseScore(week, team, Cum_Def_Lib):
	total = .5 * Cum_Def_Lib[week][team]["avg_PA"]
	total += .05 * Cum_Def_Lib[week][team]["avg_PaYd"]
	total -= 2 * Cum_Def_Lib[week][team]["avg_Ints"]
	return total

def getTeamRank(week, team, Cum_Def_Lib):
	cur_rank = 1
	team_score = getDefenseScore(week, team, Cum_Def_Lib)
	fan_rank = []
	for team_iter in Cum_Def_Lib[week]:
		if team_iter != team:
			print "team is " + str(team_iter)
			print Cum_Def_Lib[week][team_iter]["avg_PA"]
			if getDefenseScore(week, team_iter, Cum_Def_Lib) < team_score:
				cur_rank +=1
	return cur_rank


def getDefenseRank(perfNum, team):
	Def_Lib = getDefLib()
	Teams = getTeamList(Def_Lib)
	Cum_Def_Lib = getCumDefLib(Def_Lib, Teams)
	schedule, bye = getSchedule(Teams)
	true_week = getTrueWeek(bye, perfNum, team)
	rank = getTeamRank(true_week, team, Cum_Def_Lib)
	#print true_week
	print rank

def main():
	perfNum = 16
	team = "PHI"
	getDefenseRank(perfNum, team)



# def the_rest():
	

# 	team_var = "Green Bay Packers"
# 	stat_var = "FanPts"
# 	stats_var_2 = "avg_" + stat_var
# 	for week_loop in Def_Lib:
# 		print "\nWeek is " + str(week_loop)
# 		if Cum_Def_Lib[week_loop][team_var]["Bye"] == True:
# 			print "Bye week! Stats are the same as the previous week.\n"
# 		else:
# 			print "Weekly " + str(stat_var) + " are " + str(Def_Lib[week_loop][team_var][stat_var])
# 			print "Cumulative " + str(stat_var) + " at this point are " + str(Cum_Def_Lib[week_loop][team_var][stat_var])
# 			print "Average " + str(stat_var) + " is " + str(Cum_Def_Lib[week_loop][team_var][stats_var_2])

if __name__ == "__main__":
    main()