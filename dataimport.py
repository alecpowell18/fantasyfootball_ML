print "hello"

import csv
from sets import Set
import numpy as np

top_ten = ['Andrew Luck','Aaron Rodgers','Drew Brees','Peyton Manning',
	'Russell Wilson', 'Matt Ryan', 'Eli Manning', 'Philip Rivers', 'Tom Brady']
top_one = ['Aaron Rodgers']
thetas = {}

fantasy_weights = {'Yds':.04,'Td':4,'Int':-1,'Ryds':.1,'Rtd':6}

# HELPER: given a stat and week, get prev n weeks
def statHelper(player, stat, perfnum, n):
	toret = []
	startperf = max(perfnum-n, 0)
	while startperf < perfnum:
		toret.append(qb_stats[player][stat][startperf])
		startperf += 1
	return toret

def training():
	for qb in top_ten:
		# print qb, "----------"
		theta = {}
		for i in the_big_five:
			x = []
			y = []
			for perfnum in range(13):	# really starts at week 4, but...
				x.append(statHelper(qb,i,perfnum+3,3))
				y.append(qb_stats[qb][i][perfnum+3])
			x_matrix = np.matrix(x)
			y_matrix = np.matrix(y)
			if np.count_nonzero(x_matrix) == 0:
				theta[i] = np.matrix([[0],[0],[0]])
			else: theta[i] = (x_matrix.getT()*x_matrix).getI()*x_matrix.getT()*y_matrix.getT()
			# print theta[i]
		thetas[qb] = theta 

def predictions(week):
	print "Hi, we're predicting now."
	for qb in top_ten:
		totalfantasyvalue = 0
		theta = thetas[qb]
		for i in the_big_five:
			x = np.matrix(statHelper(qb,i,week,3)).getT()
			# print x
			totalfantasyvalue += float(theta[i].getT()*x*fantasy_weights[i])
		print "Predicted fantasy score for", qb, "is:", totalfantasyvalue, "****"


qb_stats = {}
qb_names = Set()
qb_parameters = []
the_big_five = ['Yds','Td','Int','Ryds','Rtd']
the_big_one = ['Td']

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
		for i in range(len(the_big_five)):
			qb_stats[current_name][the_big_five[i]] = []
	current_param = 0
	for param in single_params:
		if qb_parameters[current_param] in the_big_five:
			qb_stats[current_name][qb_parameters[current_param]].append(float(param.strip()))
		current_param += 1

# print qb_stats['Peyton Manning']['Rtd']
# print statHelper('Aaron Rodgers','Td',7,3)

training()
predictions(7)
