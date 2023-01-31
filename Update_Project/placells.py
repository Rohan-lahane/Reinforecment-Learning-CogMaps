import numpy as np
from numpy.linalg import norm        
from numpy.random import choice      
from tqdm import tqdm               

from parameters import * 
from basic_functions import random_position

class PlaceCells: 

  centers = None

  current_activation = None
  prev_activation = None

  position_in_maze = None
  activation_in_maze = None

  def __init__(self):
    self.set_random_centers()
    self.reset_activations()

    self.init_position_in_maze()
    self.init_activation_in_maze()

  def reset_activations(self):
    self.current_activation = np.zeros((CELL_COUNT))
    self.prev_activation = np.zeros((CELL_COUNT))

  def set_random_centers(self):
      def get_random_center():
          return random_position((XO,YO),R_WATERMAZE)

      self.centers = np.array(
          [get_random_center() for _ in range(CELL_COUNT) ]
      )


  def init_position_in_maze(self):
      step = 0.05

      x_coords = np.arange(XO - R_WATERMAZE, XO + R_WATERMAZE + step, step )
      y_coords = np.arange(YO - R_WATERMAZE, YO + R_WATERMAZE + step, step )

      positions = np.array(np.meshgrid(x_coords,y_coords)).T.reshape(-1,2)
        # ''' meshgrid returns coordinate matrix  '''
      origin = np.array([XO,YO])
      distances_from_origin = norm(origin-positions, axis = 1)

      self.position_in_maze = positions[ distances_from_origin <= R_WATERMAZE]


  def init_activation_in_maze(self):
      self.activation_in_maze = np.array([self.activation_at(pos) for pos in self.position_in_maze])

  def activation_at(self,position):
      return np.exp(- np.square(norm(self.centers-position,axis = 1 ))
                      /(2*PLACE_CELL_STD*PLACE_CELL_STD))
      # ''' insert formula from the paper in the rport  '''

  def update_activations(self,new_position):
      np.copyto(self.prev_activation, self.current_activation)
      self.current_activation =self.activation_at(new_position)