import csv
from collections import defaultdict

abbrvs = {'New Orleans Saints':'NO', 'Pittsburgh Steelers':'PIT', 'New England Patriots':'NE',
	'New York Jets':'NYJ', 'Miami Dolphins':'MIA', 'Buffalo Bills':'BUF', 'Baltimore Ravens':'BAL',
	'Cleveland Browns':'CLE', 'Cincinnati Bengals':'CIN', 'Houston Texans':'HOU', 'Indianapolis Colts':'IND',
	'Jacksonville Jaguars':'JAX', 'Tennessee Titans':'TEN', 'Denver Broncos':'DEN', 'Kansas City Chiefs':'KC',
	'San Diego Chargers':'SD', 'Oakland Raiders':'OAK', 'Dallas Cowboys':'DAL', 'Washington Redskins':'WAS',
	'New York Giants':'NYG', 'Philadelphia Eagles':'PHI', 'Minnesota Vikings':'MIN', 'Green Bay Packers':'GB',
	'Detroit Lions':'DET', 'Chicago Bears':'CHI', 'Tampa Bay Buccaneers':'TB', 'Atlanta Falcons':'ATL',
	'Carolina Panthers':'CAR', 'San Francisco 49ers':'SF', 'Seattle Seahawks':'SEA', 'Arizona Cardinals':'ARZ',
	'St. Louis Rams':'STL', 'St':'STL'}

Years = [2013, 2014]
week_list = ["Week", "week"]

def getDefLib():
	defense_stats = []
	steam_names = []
	defense_parameters = []
	Def_Lib = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

	defense = open('Full_Defense_Data.csv', 'rU')
	defense_read = csv.reader(defense, dialect=csv.excel_tab)
	for param in defense_read.next()[0].split(','):
		defense_parameters.append(param)

	Year = 2014

	Week = 1
	for line in defense:
		if("2013") in line:
			Year = 2013
			Week = 0
		else:
			if "week" not in line.lower():
				single_params = line.split(',')
				team_name = abbrvs[single_params[0].split('. ')[1]]
				Def_Lib[Year][Week][team_name]["Sacks"] = single_params[2]
				Def_Lib[Year][Week][team_name]["Recovered_Fumbles"] = single_params[3]
				Def_Lib[Year][Week][team_name]["Ints"] = single_params[4]
				Def_Lib[Year][Week][team_name]["DefTD"] = single_params[5]
				Def_Lib[Year][Week][team_name]["PA"] = single_params[6]
				Def_Lib[Year][Week][team_name]["PaYd"] = single_params[7]
				Def_Lib[Year][Week][team_name]["RuYd"] = single_params[8]
				Def_Lib[Year][Week][team_name]["Safeties"] = single_params[9]
				Def_Lib[Year][Week][team_name]["DefTD"] = single_params[10]
				Def_Lib[Year][Week][team_name]["FanPts"] = single_params[11]
			else:
				Week += 1
	return Def_Lib

def getTeamList(Def_Lib):
	Teams = []
	for team in Def_Lib[2013][1]:
		# print team
		Teams.append(team)
	return Teams

def getCumDefLib(Def_Lib, Teams):
	Cum_Def_Lib = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
	for Year in Years:
		for Week in Def_Lib[Year]:
			for Team in Teams:
				if Team in Def_Lib[Year][Week]:
					Cum_Def_Lib[Year][Week][Team]["Bye"] = False
					Cum_Def_Lib[Year][Week][Team]["TotalGames"] = 0
					Cum_Def_Lib[Year][Week][Team]["Sacks"] = 0
					Cum_Def_Lib[Year][Week][Team]["Recovered_Fumbles"] = 0
					Cum_Def_Lib[Year][Week][Team]["Ints"] = 0
					Cum_Def_Lib[Year][Week][Team]["DefTD"] = 0
					Cum_Def_Lib[Year][Week][Team]["PA"] = 0
					Cum_Def_Lib[Year][Week][Team]["PaYd"] = 0
					Cum_Def_Lib[Year][Week][Team]["RuYd"] = 0
					Cum_Def_Lib[Year][Week][Team]["Safeties"] = 0
					Cum_Def_Lib[Year][Week][Team]["DefTD"] = 0
					Cum_Def_Lib[Year][Week][Team]["FanPts"] = 0
				else:
					Cum_Def_Lib[Year][Week][Team]["Bye"] = True
	for Team in Teams:
		for Year in Years:
			Cum_Def_Lib[Year][0][Team]["Bye"] = False
			Cum_Def_Lib[Year][0][Team]["TotalGames"] = 0
			Cum_Def_Lib[Year][0][Team]["Sacks"] = 0
			Cum_Def_Lib[Year][0][Team]["Recovered_Fumbles"] = 0
			Cum_Def_Lib[Year][0][Team]["Ints"] = 0
			Cum_Def_Lib[Year][0][Team]["DefTD"] = 0
			Cum_Def_Lib[Year][0][Team]["PA"] = 0
			Cum_Def_Lib[Year][0][Team]["PaYd"] = 0
			Cum_Def_Lib[Year][0][Team]["RuYd"] = 0
			Cum_Def_Lib[Year][0][Team]["Safeties"] = 0
			Cum_Def_Lib[Year][0][Team]["DefTD"] = 0
			Cum_Def_Lib[Year][0][Team]["FanPts"] = 0

	for Year in Years:
		for Week in Def_Lib[Year]:
			for Team in Teams:
				if(Cum_Def_Lib[Year][Week][Team]["Bye"] == False):
					Cum_Def_Lib[Year][Week][Team]["TotalGames"] = Cum_Def_Lib[Year][Week-1][Team]["TotalGames"] + 1
					TotalGames = Cum_Def_Lib[Year][Week][Team]["TotalGames"]
					Cum_Def_Lib[Year][Week][Team]["Sacks"] = int(Def_Lib[Year][Week][Team]["Sacks"]) + Cum_Def_Lib[Year][Week - 1][Team]["Sacks"]
					Cum_Def_Lib[Year][Week][Team]["avg_Sacks"] = Cum_Def_Lib[Year][Week][Team]["Sacks"]/float(TotalGames)
					Cum_Def_Lib[Year][Week][Team]["Recovered_Fumbles"] + int(Def_Lib[Year][Week][Team]["Recovered_Fumbles"]) + Cum_Def_Lib[Year][Week - 1][Team]["Recovered_Fumbles"]
					Cum_Def_Lib[Year][Week][Team]["avg_Recovered_Fumbles"] = Cum_Def_Lib[Year][Week][Team]["Recovered_Fumbles"]/float(TotalGames)
					Cum_Def_Lib[Year][Week][Team]["Ints"] = int(Def_Lib[Year][Week][Team]["Ints"]) + Cum_Def_Lib[Year][Week - 1][Team]["Ints"]
					Cum_Def_Lib[Year][Week][Team]["avg_Ints"] = Cum_Def_Lib[Year][Week][Team]["Ints"]/float(TotalGames)
					Cum_Def_Lib[Year][Week][Team]["DefTD"] = int(Def_Lib[Year][Week][Team]["DefTD"]) + Cum_Def_Lib[Year][Week - 1][Team]["DefTD"]
					Cum_Def_Lib[Year][Week][Team]["avg_DefTD"] = Cum_Def_Lib[Year][Week][Team]["DefTD"]/float(TotalGames)
					Cum_Def_Lib[Year][Week][Team]["PA"] = int(Def_Lib[Year][Week][Team]["PA"]) + Cum_Def_Lib[Year][Week - 1][Team]["PA"]
					Cum_Def_Lib[Year][Week][Team]["avg_PA"] = Cum_Def_Lib[Year][Week][Team]["PA"]/float(TotalGames)
					Cum_Def_Lib[Year][Week][Team]["PaYd"] = int(Def_Lib[Year][Week][Team]["PaYd"]) + Cum_Def_Lib[Year][Week - 1][Team]["PA"]
					Cum_Def_Lib[Year][Week][Team]["avg_PaYd"] = Cum_Def_Lib[Year][Week][Team]["PaYd"]/float(TotalGames)
					Cum_Def_Lib[Year][Week][Team]["RuYd"] = int(Def_Lib[Year][Week][Team]["RuYd"]) + Cum_Def_Lib[Year][Week - 1][Team]["RuYd"]
					Cum_Def_Lib[Year][Week][Team]["avg_RuYd"] = Cum_Def_Lib[Year][Week][Team]["RuYd"]/float(TotalGames)
					Cum_Def_Lib[Year][Week][Team]["Safeties"] = int(Def_Lib[Year][Week][Team]["Safeties"]) + Cum_Def_Lib[Year][Week - 1][Team]["Safeties"]
					Cum_Def_Lib[Year][Week][Team]["avg_Safeties"] = Cum_Def_Lib[Year][Week][Team]["Safeties"]/float(TotalGames)
					Cum_Def_Lib[Year][Week][Team]["DefTD"] += int(Def_Lib[Year][Week][Team]["DefTD"]) + Cum_Def_Lib[Year][Week - 1][Team]["DefTD"]
					Cum_Def_Lib[Year][Week][Team]["avg_DefTD"] = Cum_Def_Lib[Year][Week][Team]["DefTD"]/float(TotalGames)
					Cum_Def_Lib[Year][Week][Team]["FanPts"] += int(Def_Lib[Year][Week][Team]["FanPts"]) + Cum_Def_Lib[Year][Week - 1][Team]["FanPts"]
					Cum_Def_Lib[Year][Week][Team]["avg_FanPts"] = Cum_Def_Lib[Year][Week][Team]["FanPts"]/float(TotalGames)
				else:
					for component in Cum_Def_Lib[Year][Week - 1][Team]:
						if component != "Bye":
							Cum_Def_Lib[Year][Week][Team][component] = Cum_Def_Lib[Year][Week - 1][Team][component]
	return Cum_Def_Lib

def getTeamRanking(team, week):
	Def_Lib = getDefLib()
	Teams = getTeamList(Def_Lib)
	# print Teams
	Cum_Def_Lib = getCumDefLib(Def_Lib, Teams)

def getSchedule(Teams):
	schedule_raw = open('Schedule.csv', 'rU')
	schedule_lines = csv.reader(schedule_raw, dialect=csv.excel_tab)
	schedule = defaultdict(lambda: defaultdict(dict))
	bye = defaultdict(lambda: defaultdict(dict))
	week = 0
	cur_year = 2014
	for line in schedule_lines:
		info = line[0].split(',')
		if info[0] == "Year 2013":
			cur_year = 2013
			week = 1
		elif info[0] != "Week":
			schedule[cur_year][week][abbrvs[info[4]]] = abbrvs[info[6]]
			schedule[cur_year][week][abbrvs[info[6]]] = abbrvs[info[4]]
		else:
			if(week != 0):
				for team in Teams:
					if team not in schedule[cur_year][week]:
						schedule[cur_year][week][team] = "BYE"
						bye[cur_year][team] = week
			week += 1
	return (schedule, bye)

def getTrueWeek(bye, perfnum, team, year):
	bye_game = int(bye[year][team])
	if bye_game > perfnum:
		return perfnum
	else:
		return perfnum + 1

def getDefenseScore(week, team, Cum_Def_Lib, year):
	total = .5 * Cum_Def_Lib[year][week][team]["avg_PA"]
	total += .05 * Cum_Def_Lib[year][week][team]["avg_PaYd"]
	total -= 2 * Cum_Def_Lib[year][week][team]["avg_Ints"]
	return total

def getTeamRank(week, team, Cum_Def_Lib, year):
	cur_rank = 1
	team_score = getDefenseScore(week, team, Cum_Def_Lib, year)
	fan_rank = []
	for team_iter in Cum_Def_Lib[year][week]:
		if team_iter != team:
			if getDefenseScore(week, team_iter, Cum_Def_Lib, year) < team_score:
				cur_rank +=1
	return cur_rank


def getDefenseRank(rawPerfNum, team, year):
	perfNum = rawPerfNum + 1
	Def_Lib = getDefLib()
	Teams = getTeamList(Def_Lib)
	Cum_Def_Lib = getCumDefLib(Def_Lib, Teams)
	schedule, bye = getSchedule(Teams)
	true_week = getTrueWeek(bye, perfNum, team, year)
	# rank = getTeamRank(true_week, team, Cum_Def_Lib, year)
	score = getDefenseScore(true_week, team, Cum_Def_Lib, year)
	#print true_week
	return score

def main():
	perfNum = 15
	team = "SEA"
	# print getDefenseRank(perfNum, team, 2013)

if __name__ == "__main__":
    main()