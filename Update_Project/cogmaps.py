

import numpy as np
from  matplotlib import * 
import matplotlib.pyplot as plt
from tqdm import tqdm

#import argparse

from experiment import RMW
#from basic_functions import print_title

# Generic function to simulate one of the experiments
def simulate_experiment(experiment, nb_runs, plot_perf = True, plot_trials = True):
    logs_of_all_runs = experiment.run_n_times(nb_runs)

    if plot_perf:
        experiment.plot_rat_performance(logs_of_all_runs)
    if plot_trials:
        experiment.plot_one_run(logs_of_all_runs[-1])


# Simulate the Reference Memory in the Watermaze (RMW) experiment
def simulate_RMW(nb_runs, plot_perf = True, plot_trials = True):
    #print_title("Pace-cells navigation by Mylastwobraincells")
    simulate_experiment(RMW(), nb_runs, plot_perf = plot_perf, plot_trials = plot_trials)




if __name__ == "__main__":
    
    nb_runs_rmw = 10
    
    plot_trials = True 

    simulate_RMW(nb_runs_rmw, plot_trials = plot_trials)
    # if nb_runs_dmp > 0:
    #      simulate_DMP(nb_runs_dmp, plot_trials = plot_trials)