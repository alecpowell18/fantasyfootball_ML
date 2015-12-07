import csv
from sets import Set
import numpy as np
import data_process as dp
import matplotlib.pyplot as plt

DEBUG = True;

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

	plt.plot(x_coords, y_coords, 'r*', x_coords, x_coords, "bo")

	plt.show()

# Obtain season data
dp.train()
qb_scores = dp.predict_qbs_for_season()

plot_graph()



if DEBUG:
	for qb in qb_scores:
		print qb, "Scores"
		print qb_scores.get(qb)


