

import numpy as np
from tqdm import tqdm

from watermaze import Watermaze
from placells import * 
from actor import *
from critic import *  
from ratagent import Rat
from results import TrialFigure, RatPerformanceFigure




class Experiment:
   

    rat = None

    # It must be defined by concrete child classes!
    rat_perf_filename = None


    def __init__(self):
        self.rat = Rat()


    def run_n_times(self, nof_times):
        logs_of_all_runs = []

        for _ in tqdm(range(nof_times)):
            logs_of_all_runs.append(self.run_once(show_progress_bar = False))
        
        return logs_of_all_runs


    def plot_rat_performance(self, logs_of_all_runs):
        # RatPerformanceFigure(logs_of_all_runs).save_and_close(self.rat_perf_filename + ".png")
        RatPerformanceFigure(logs_of_all_runs).show()




class RMW(Experiment):
    '''
    Reference Memory in the Watermaze (RMW) experiment.
    '''
    
    first_watermaze = None
    #second_watermaze = None


    def __init__(self):
        super().__init__()
        self.rat_perf_filename = "rmw-rat-performance"

        self.first_watermaze = Watermaze()
        #self.second_watermaze = Watermaze()


    def set_new_random_plateforms(self):
        self.first_watermaze.platform_pos()
       # self.second_watermaze.platform_pos()


    def run_once(self, show_progress_bar = True):
        # Reset some parameters
        self.rat.reset()
        self.set_new_random_plateforms()

        # Run trials corresponding to the day 1 to 9 (4 trials/day)
        logs = self.rat.n_trials(self.first_watermaze, 9 * 4,
                                          show_progress_bar = show_progress_bar)

        

        return logs
        #debug this baadme 

    def run_n_times(self, nb_times):
        logs_of_all_runs = []

        for _ in tqdm(range(nb_times)):
            logs_of_all_runs.append(self.run_once(show_progress_bar = False))
        
        return logs_of_all_runs


    def plot_one_run(self, logs):
        for index, log in tqdm(enumerate(logs), desc = "Trial plots (RMW)"):
            # Determine which watermaze corresponds to the current log
            watermaze = self.first_watermaze 
         
            TrialFigure(watermaze, self.rat, log).show()