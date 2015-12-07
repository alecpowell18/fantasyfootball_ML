import csv
from sets import Set
import numpy as np
import data_process as dp
import matplotlib.pyplot as plt

DEBUG = False;
TRAINING_RATIO = 0.3

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
			print qb_stats[qb][i][j]
		actual_fantasy_performance.append(fantasypts)
	return actual_fantasy_performance

def get_actual_perf(perfIdx):
	fantasypts = 0
	for i in range(len(the_big_five)):
		# print "******", dp.qb_perfs[perfIdx][1]
		fantasypts += dp.qb_perfs[perfIdx][1][i]*fantasy_weights[the_big_five[i]]
	return fantasypts

def predict_perf(perfIdx):
	totalfantasyvalue = 0
	for i in range(len(the_big_five)):
		x = np.matrix(dp.qb_perfs[perfIdx][0][i]).getT()
		totalfantasyvalue += float(dp.theta[the_big_five[i]].getT()*x*fantasy_weights[the_big_five[i]])
	return totalfantasyvalue


def plot_graph():
	min_error = min_training_examples = 0
	max_error = 100;
	max_training_examples = 100;

	# Setup labels and axes
	plt.ylabel('Mean Absolute Error')
	plt.xlabel('# Training Examples')
	plt.axis([min_training_examples,max_training_examples, min_error, max_error])

	# Define points for plotting
	x_coords = np.arange(5.,100.,2)
	y_coords = x_coords*1.5

	plt.plot(x_coords, y_coords, 'r^', label="Training Error")
	plt.plot(x_coords, x_coords, "bo", label="Test Error")

	plt.legend()

	plt.show()

# Obtain season data
dp.make_perfs_bag()
TOTAL_PERF_RECORDS = len(dp.qb_perfs)
TOTAL_TRAINING_RECORDS = int(TRAINING_RATIO * TOTAL_PERF_RECORDS)
#TRAINING
selectedTrainingPerfs = dp.train_new(TOTAL_TRAINING_RECORDS)
TOTAL_TEST_RECORDS = TOTAL_PERF_RECORDS - TOTAL_TRAINING_RECORDS
qb_scores = dp.predict_qbs_for_season()
qb_stats = dp.get_qb_stats()

# Get Andrew Luck's actual performance data
andrew_luck = get_actual_performance('Andrew Luck',4)
print "ACTUAL PERFORMANCES****"
print len(andrew_luck)
print "*******", andrew_luck, "******"


# Right now, we're just testing Andrew Luck's predictions for weeks 4-16.
plist = []
for i in range(3,16):
	# plist.append(predictions(i))
	plist.append(dp.predict_qb_for_week('Andrew Luck', i))
print "PREDICTIONS****"
print len(plist)
print "******", plist, "******"


#Calculate training error
training_error_sum = 0
test_error_sum = 0
for idx in range(TOTAL_PERF_RECORDS):
	actual_perf_score = get_actual_perf(idx)
	predicted_perf_score = predict_perf(idx)
	if idx in selectedTrainingPerfs:
		training_error_sum += abs(actual_perf_score - predicted_perf_score)
	else:
		test_error_sum += abs(actual_perf_score - predicted_perf_score)


mean_abs_error_train = training_error_sum / float(TOTAL_TRAINING_RECORDS)
mean_abs_error_test = test_error_sum / float(TOTAL_TEST_RECORDS)

print "And mean absolute training error is....", mean_abs_error_train
print "And mean abs testing error..", mean_abs_error_test

plot_graph()


# runningerror = 0
# count = 0
# for game in range(len(plist)):
# 	print plist[game]
# 	predict = plist[game][0]
# 	actual = andrew[game]
# 	print "P:", predict
# 	print "A:", actual
# 	diff = abs(actual - predict)
# 	diffsq = diff*diff
# 	print "diff sq is", diffsq
# 	runningerror += diffsq
# 	count += 1
# print count, "COUNT"
# mse = float(runningerror / count)
# print mse