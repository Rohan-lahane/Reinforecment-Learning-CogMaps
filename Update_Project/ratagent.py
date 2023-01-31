
import numpy as np
from numpy.linalg import norm         
from numpy.random import choice      
from tqdm import tqdm               

from parameters import * 
from basic_functions import random_position

from placells import PlaceCells
from critic import Critic
from actor import Actor

class Rat:

  # '''this class simulates the behaviour of a rat learning through unsupervised method  '''


  place_cells = None
  critic = None
  actor = None

  current_pos = None
  prev_pos =None
  starting_pos = [
      np.array([XO,YO+(R_WATERMAZE*0.9)]), #up
      np.array([XO,YO-(R_WATERMAZE*0.9)]), #down
      np.array([XO+(R_WATERMAZE*0.9),YO]),  #right
      np.array([XO-(R_WATERMAZE*0.9),YO])  #left 
  ]

  prev_pos_diff = None
  pos_diff_by_direction = {
      "top_left":       np.array([-0.35355, 0.35355 ]),
      "top":            np.array([0.0     , 1.0     ]),
      "top_right":      np.array([0.35355 , 0.35355 ]),
      "right":          np.array([1.0     , 0.0     ]),
      "bottom_right":   np.array([0.35355 , -0.35355]),
      "bottom":         np.array([0.0     , -1.0    ]),
      "bottom_left":    np.array([-0.35355, -0.35355]),
      "left":           np.array([-1.0    , 0.0     ])
  }

  def __init__(self):
    self.place_cells = PlaceCells()
    self.critic = Critic()
    self.actor = Actor()

    self.reset_position()

  def reset_position(self):
    self.current_pos = self.starting_pos[choice(len(self.starting_pos))].copy()
    self.prev_pos = None

    self.prev_pos_diff = np.array([0,0])
    self.place_cells.reset_activations()


  def reset(self):
    self.critic.reset_weights()
    self.actor.reset_weights()

      # ''' try to use this directly '''
 


  def next_pos(self,watermaze):
    self.prev_pos = self.current_pos

    #using probability to pick the direction of next step randomly

    probability = self.actor.action_probability(self.place_cells)
    new_dir=choice(self.actor.actions, p= probability)

    new_pos_diff = self.pos_diff_by_direction[new_dir] * SPEED* STEP_TIME
    pos_diff = (ACTION_MOMENTUM_RATIO* new_pos_diff) + ((1- ACTION_MOMENTUM_RATIO)* self.prev_pos_diff)

    if norm(self.current_pos+pos_diff) >= R_WATERMAZE :
        pos_diff = pos_diff*(-1) 

    self.current_pos += pos_diff
    self.prev_pos_diff =pos_diff

    self.place_cells.update_activations(self.current_pos)
    
    reward = 1 if norm(self.current_pos-watermaze.platform.center) <= watermaze.platform.radius else 0

    return new_dir, reward

  def update_weights(self, direction, reward):
      error = self.critic.update_weights(self.place_cells, reward)
      self.actor.update_weights(self.place_cells, direction, error)

      return error

  def one_step(self,watermaze):
    direction,  reward= self.next_pos(watermaze)
    error = self.update_weights(direction,reward)

    return direction, reward, error

  def n_steps(self,watermaze,nof_steps,show_progress_bar= True):
    log = {
        "direction":[],
         "reward": [],
         "error" :[],
         "position":[]
    }
    iterator = tqdm(range(nof_steps), desc = "steps") if show_progress_bar else range(nof_steps)

    for _ in iterator:
        direction, reward, error = self.simulate_one_step(watermaze)

        log["direction"].append(direction)
        log["reward"].append(reward)
        log["error"].append(error)
        log["position"].append(self.current_pos.copy())

    return log 

  def one_trial(self,watermaze):
      log = { 
          "direction":[],
          "reward": [],
          "error" :[],
          "position":[]
      }

      self.reset_position()
      
      for _ in range(int(np.round(TRIAL_TIME/STEP_TIME))) :

          direction,reward,error= self.one_step(watermaze)

          log["direction"].append(direction)
          log["reward"].append(reward)
          log["error"].append(error)
          log["position"].append(self.current_pos.copy())


          if reward == 1:
             break

      log["critic_vals"] = self.critic.val_estimates(self.place_cells)
      log["action_probability"] = self.actor.action_probability_in_maze(self.place_cells)

      return log

  def n_trials(self,watermaze,nof_trials, show_progress_bar= True):
      logs =[]
      iterator = tqdm(range(nof_trials), desc = "Trials") if show_progress_bar else range(nof_trials)


      for _ in iterator: 
        log = self.one_trial(watermaze)
        logs.append(log)


      return logs