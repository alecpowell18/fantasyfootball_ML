import csv
from sets import Set
import numpy as np
import data_process as dp

DEBUG = True;

# Obtain season data
dp.train()
qb_scores = dp.predict_qbs_for_season()

if DEBUG:
	for qb in qb_scores:
		print qb, "Scores"
		print qb_scores.get(qb)


