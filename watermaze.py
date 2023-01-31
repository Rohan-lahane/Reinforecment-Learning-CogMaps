# -*- coding: utf-8 -*-
"""watermaze.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z0twhKSUWmi3PXxLQf15pxr2rP8lkmcp

Here we have simulated RMW task (Reference memory in watermaze) as shown in the foster et al paper. It is a circular tank with a radius R. And a platform (final goal). Reaching the final goal gives the agent a Reward. the platform can be moved to a differentplace each timeto simulate a delayed mathing to pacetask (DMP)
"""

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