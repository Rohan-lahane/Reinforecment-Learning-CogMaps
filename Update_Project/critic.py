

import numpy as np
from numpy.linalg import norm        
from numpy.random import choice      
from tqdm import tqdm                

from parameters import * 
from basic_functions import random_position

from placells import *
# from critic import *

class Critic:

      # ''' this class estimates the value fuction from place cells '''

  weights = None

  def __init__(self):
      self.reset_weights()

  def reset_weights(self):
      self.weights = np.zeros((CELL_COUNT))

  def val_estimates(self,place_cells):
      return [np.dot(activation,self.weights)for activation in place_cells.activation_in_maze]

  def update_weights(self,place_cells,reward):
      prev_val_estimate = np.dot(place_cells.prev_activation, self.weights)
      current_val_estimate = np.dot(place_cells.current_activation,self.weights)

      if reward == 1:
        current_val_estimate = 0

      error = reward+ (TDECAY*current_val_estimate)- prev_val_estimate
      ''' insert equation from paper in report  '''
      self.weights = self.weights + C_LEARNING_RATE* (error* place_cells.prev_activation)

      return error