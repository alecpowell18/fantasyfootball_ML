import csv
import random
from sets import Set
import numpy as np
import data_process as dp
import matplotlib.pyplot as plt

DEBUG = False
TRAINING_RATIO = 0.7

fantasy_weights = {'Yds':.04,'Td':4,'Int':-1,'Ryds':.1,'Rtd':6}
the_big_five = ['Yds','Td','Int','Ryds','Rtd']
the_big_one = ['Td']
season_long_qbs = ['Derek Carr', 'Andy Dalton', 'Joe Flacco', 'Andrew Luck','Aaron Rodgers','Drew Brees','Peyton Manning',
	'Russell Wilson', 'Matt Ryan', 'Eli Manning', 'Philip Rivers', 'Tom Brady', 'Colin Kaepernick', 'Ben Roethlisberger',
	'Matthew Stafford', 'Ryan Tannehill']

def get_actual_performance(qb,week_start):
	actual_fantasy_performance = []
	for j in range(week_start-1,len(qb_stats[qb]['Td'])):
		fantasypts = 0
		for i in the_big_five:
			fantasypts += qb_stats[qb][i][j]*fantasy_weights[i]
		actual_fantasy_performance.append(fantasypts)
	return actual_fantasy_performance

def get_actual_perf(perfIdx):
	fantasypts = 0
	for i in range(len(the_big_five)):
		fantasypts += dp.qb_perfs[perfIdx][1][i]*fantasy_weights[the_big_five[i]]
	return fantasypts

def predict_perf(perfIdx):
	totalfantasyvalue = 0
	for i in range(len(the_big_five)):
		x = np.matrix(dp.qb_perfs[perfIdx][0][i]).getT()
		totalfantasyvalue += float(dp.theta[the_big_five[i]].getT()*x*fantasy_weights[the_big_five[i]])
	average_defense_rnk = sum(dp.qb_perfs_defenses[perfIdx][0]) / len(dp.qb_perfs_defenses[perfIdx][0])
	today_defense_rnk = dp.qb_perfs_defenses[perfIdx][1]
	diff_rnk = today_defense_rnk - average_defense_rnk
	defense_adjustment = diff_rnk / float(average_defense_rnk)
	return totalfantasyvalue + defense_adjustment

def predict_stat_perf(perfIdx):
	totalfantasyvalue = 0
	for i in range(len(the_big_five)):
		x = np.matrix(dp.qb_perfs[perfIdx][0][i]).getT()
		totalfantasyvalue += float(dp.theta[the_big_five[i]].getT()*x*fantasy_weights[the_big_five[i]])
	return totalfantasyvalue

def predict_perf_gameday(perfIdx):
	statValue = predict_stat_perf(perfIdx)
	defRnk = dp.qb_perfs_defenses[perfIdx][1]

	x = []
	x.append(statValue)
	x.append(defRnk)

	x_matrix = np.matrix(x)

	return x_matrix * dp.gameday_thetas[0]

def plot_graph():
	min_error = 0
	max_error = 20

	min_num_examples = 10
	max_num_examples = 250

	# Setup labels and axes
	plt.ylabel('Mean Absolute Error')
	plt.xlabel('# Examples')
	plt.axis([min_num_examples,max_num_examples, min_error, max_error])

	# Define points for plotting
	num_examples = []
	all_train_errors = []
	all_test_errors = []

	for i in range(min_num_examples,max_num_examples,5):
		(train_error,test_error) = train_and_test(i)
		all_train_errors.append(train_error)
		all_test_errors.append(test_error)
		num_examples.append(i)

	plt.plot(num_examples, all_train_errors, 'r^', label="Training Error")
	plt.plot(num_examples, all_test_errors, "bo", label="Test Error")
	plt.legend()

	plt.show()

 
# Obtain season data
dp.make_perfs_bag()
TOTAL_PERF_RECORDS = len(dp.qb_perfs)

def train_and_test(num_examples):
	TOTAL_TRAINING_RECORDS = int(TRAINING_RATIO * num_examples)
	TOTAL_TEST_RECORDS = int((1-TRAINING_RATIO) * num_examples)

	#TRAINING
	selectedTrainingPerfs = dp.train_gameday_LR(TOTAL_TRAINING_RECORDS)

	#Calculate training error
	training_error_sum = 0
	for idx in selectedTrainingPerfs:
		actual_perf_score = get_actual_perf(idx)
		predicted_perf_score = predict_perf_gameday(idx).item(0)
		training_error_sum += abs(actual_perf_score - predicted_perf_score)
	
	#Calculate the test error
	test_examples = 0
	test_error_sum = 0
	while test_examples < TOTAL_TEST_RECORDS:
		rand_index = random.randint(0,TOTAL_PERF_RECORDS-1)
		if rand_index not in selectedTrainingPerfs:
			test_examples+=1
			actual_perf_score = get_actual_perf(rand_index)
			predicted_perf_score = predict_perf_gameday(idx).item(0)
			test_error_sum += abs(actual_perf_score - predicted_perf_score)

	mean_abs_error_train = training_error_sum / float(TOTAL_TRAINING_RECORDS)
	mean_abs_error_test = test_error_sum / float(TOTAL_TEST_RECORDS)

	if DEBUG: print "And mean absolute training error is....", mean_abs_error_train
	if DEBUG: print "And mean abs testing error..", mean_abs_error_test
	return (mean_abs_error_train, mean_abs_error_test)
	

def main():
	plot_graph()

if __name__ == "__main__":
    main()