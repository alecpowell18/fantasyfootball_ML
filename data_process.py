import csv
from sets import Set
import numpy as np
import random
import defense_parser as defense

season_long_qbs = ['Derek Carr', 'Andy Dalton', 'Joe Flacco', 'Andrew Luck','Aaron Rodgers','Drew Brees','Peyton Manning',
	'Russell Wilson', 'Matt Ryan', 'Eli Manning', 'Philip Rivers', 'Tom Brady', 'Colin Kaepernick', 'Ben Roethlisberger',
	'Matthew Stafford', 'Ryan Tannehill']
qb_team_abbreviations = {'Derek Carr':'OAK', 'Andy Dalton':'CIN', 'Joe Flacco':'BAL', 'Andrew Luck':'IND','Aaron Rodgers':'GB',
	'Drew Brees':'NO','Peyton Manning':'DEN', 'Russell Wilson':'SEA', 'Matt Ryan':'ATL', 'Eli Manning':'NYG', 'Philip Rivers':'SD',
	'Tom Brady':'NE', 'Colin Kaepernick':'SF', 'Ben Roethlisberger':'PIT','Matthew Stafford':'DET', 'Ryan Tannehill':'MIA'}

fantasy_weights = {'Yds':.04,'Td':4,'Int':-1,'Ryds':.1,'Rtd':6}

DEBUG = False

gameday_thetas = []
theta = {}

qb_stats = {}
qb_names = Set()
qb_parameters = []
the_big_five = ['Yds','Td','Int','Ryds','Rtd']
data_fields = ['Yds','Td','Int','Ryds','Rtd','DefRnk']
the_big_one = ['Td']

qb_perfs = []
#list of tuples
qb_perfs_defenses = []

# Lookback Configuration
look_back = 3

# Configures for Lookback
zeros_list = []
for j in range(look_back):
	zeros_list.append(0)
default_matrix = (np.matrix(zeros_list)).getT()
start_week = 1+look_back
end_week = 16

# HELPER: given a stat and week, get prev n weeks
def statHelper(player, stat, perfnum, n):
	toret = []
	startperf = max(perfnum-n, 0)
	while startperf < perfnum:
		if stat == 'DefRnk':
			toret.append(defense.getDefenseRank(startperf,qb_team_abbreviations[player]))
		else: toret.append(qb_stats[player][stat][startperf])
		startperf += 1
	return toret

def train_V1():
	if DEBUG: print "Training for Specific QB Approach"
	for qb in season_long_qbs:
		theta = {}
		if DEBUG: print qb
		for i in the_big_five:
			x = []
			y = []
			for perfnum in range(13):	# really starts at week 4, but...
				x.append(statHelper(qb,i,perfnum+3,3))
				y.append(qb_stats[qb][i][perfnum+3])
			x_matrix = np.matrix(x)
			y_matrix = np.matrix(y)
			try:
				theta[i] = (x_matrix.getT()*x_matrix).getI()*x_matrix.getT()*y_matrix.getT()
			except np.linalg.LinAlgError:
				if DEBUG: print "Warning: Detected non-invertible matrix for", i ," so using zeros."
				theta[i] = np.matrix([[0],[0],[0]])
		if DEBUG:
			print "Thetas for",qb
			print theta
		thetas[qb] = theta

def train_generalized(trainingsz):
	if DEBUG: print "Training for Generalized Theta Approach"
	indices = random.sample(xrange(len(qb_perfs)), trainingsz)
	for i in range(len(the_big_five)):
		x = []
		y = []
		for idx in indices:
			x.append(qb_perfs[idx][0][i])	#fill X matrix with this perf's X's
			y.append(qb_perfs[idx][1][i])	#fill Y ''
		x_matrix = np.matrix(x)
		y_matrix = np.matrix(y)
		try:
			theta[the_big_five[i]] = (x_matrix.getT()*x_matrix).getI()*x_matrix.getT()*y_matrix.getT()
		except np.linalg.LinAlgError:
			if DEBUG: print "Warning: Detected non-invertible matrix for", i ," so using zeros."
			# The following needs to be changed to match the look back we are using!
			theta[the_big_five[i]] = default_matrix
	return indices

def predict_stats_perf(perfIdx):
	totalfantasyvalue = 0
	for i in range(len(the_big_five)):
		x = np.matrix(qb_perfs[perfIdx][0][i]).getT()
		totalfantasyvalue += float(theta[the_big_five[i]].getT()*x*fantasy_weights[the_big_five[i]])
	return totalfantasyvalue

def get_actual_perf(perfIdx):
	fantasypts = 0
	for i in range(len(the_big_five)):
		fantasypts += qb_perfs[perfIdx][1][i]*fantasy_weights[the_big_five[i]]
	return fantasypts

def train_gameday_LR(trainingsz):
	if DEBUG: print "Training - includes defensive values"
	indices = train_generalized(trainingsz)
	# print theta

	x  =[]
	y = []
	for i in indices:
		features = []

		# Generate a training example consisting of statistical prediction and defensive rank 
		features.append(predict_stats_perf(i))
		features.append(qb_perfs_defenses[i][1])

		x.append(features)
		y.append(get_actual_perf(i))	

	x_matrix = np.matrix(x)
	y_matrix = np.matrix(y)
	gameday_thetas.append((x_matrix.getT()*x_matrix).getI()*x_matrix.getT()*y_matrix.getT())

	# print gameday_thetas
	return indices

#PERF STRUCT: 
def make_perfs_bag():
	if DEBUG: print "Making the bag of all performances data"
	#change to list of ALL QBs
	for qb in season_long_qbs:
		# will have to change to adjust for ALL QBs
		for perfnum in range(17-start_week):
			x = []
			y = []
			for i in the_big_five:
				x.append(statHelper(qb,i,perfnum+look_back,look_back))
				y.append(qb_stats[qb][i][perfnum+look_back])
			qb_perfs.append((x,y))
			tup_1 = statHelper(qb,'DefRnk',perfnum+look_back,look_back)
			tup_2 = defense.getDefenseRank(perfnum, qb_team_abbreviations[qb])
			qb_perfs_defenses.append((tup_1,tup_2))
	if DEBUG: print "Bag filled."
	# print qb_perfs_defenses

def predict_qbs_for_week(week):
	qb_week_scores = {}
	for qb in season_long_qbs:
		qb_val = predict_qb_for_week(qb, week)
		qb_week_scores[qb] = qb_val
	return qb_week_scores

def predict_qb_for_week(qb, week):
	totalfantasyvalue = 0
	for i in range(len(the_big_five)):
		x = np.matrix(statHelper(qb,the_big_five[i],week,look_back)).getT()
		if DEBUG: print theta
		if DEBUG: print theta[the_big_five[i]]
		totalfantasyvalue += float(theta[the_big_five[i]].getT()*x*fantasy_weights[the_big_five[i]])
	return totalfantasyvalue

def predict_qbs_for_season():
	qb_scores = {}
	for qb in season_long_qbs:
		week_scores = [];
		for w in range(start_week, end_week+1):
			score = predict_qb_for_week(qb, w)
			week_scores.append(score)
		qb_scores[qb] = week_scores
	return qb_scores

def get_qb_stats():
	return qb_stats

qbs = open('data_2014.csv', 'rU')
qbs_read = csv.reader(qbs, dialect=csv.excel_tab)

for parameter in qbs_read.next()[0].split(','):
	qb_parameters.append(parameter)

for line in qbs_read:
	single_params = line[0].split(',')
	current_name = single_params[0].strip()
	current_name = current_name[current_name.find('.')+2:]
	week = single_params[2].strip()
	qb_names.add(current_name)
	if current_name not in qb_stats.keys():
		qb_stats[current_name] = {}
		for i in range(len(data_fields)):
			qb_stats[current_name][data_fields[i]] = []
	current_param = 0
	for param in single_params:
		if qb_parameters[current_param] in the_big_five:
			qb_stats[current_name][qb_parameters[current_param]].append(float(param.strip()))
		current_param += 1

