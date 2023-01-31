

import numpy as np

from parameters import*
from basic_functions import random_position

class Platform:
  center = None
  radius = R_PLATFORM
  
  def __init__(self):
    self.set_random_center()

  def set_random_center(self):
    self.center = random_position((XO,YO), R_WATERMAZE)  


class Watermaze:

  platform = None

  center = np.array([XO,YO])
  radius = R_WATERMAZE

  def __intit__(self): 
    self.platform_pos()

  def platform_pos(self):
    self.platform = Platform()