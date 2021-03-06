# -*- coding: utf-8 -*-
"""Homework_4_MDP_Kesenheimer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ePhAaMCjSD3ZWEg207hjHulNpTixmYzn

# Import

Requied modules are imported and pymdptoolbox is installed
"""

!pip install pymdptoolbox
import mdptoolbox.mdp as mdp
import mdptoolbox.util as util
import mdptoolbox.example as example

import random
import numpy as np
from itertools import permutations
from itertools import product
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix

"""#Preperation of MDP

##Warehouse Attributes
Warehouse Attributes are set.

Size of warehouse
Number of products
Probabilities of products
Movements
"""

warehouse = ["A","B","C","D"]

products = ["p1","p2"]
probability = {"p1": 0.8,"p2": 0.2}
probabilities_only = [0.8, 0.2]
if (len(products) != len(probability)):
  print("ERROR: Prob. or Products are unqueal ")
movements = ["stock", "unstock"]

"""## States
All possible states are determined by calling function get_states. For visualization purpose the number of states and all states are printed.
"""

def get_states(warehouse, product, movements):
  unique_combinations = []
  if (len(warehouse) != 4):
    print("ERROR: Warehouse_Size not correct")
  if (len(product) != 2):
    print("ERROR: Warehouse_Size not correct")
  if (len(movements) != 2):
    print("ERROR: Warehouse_Size not correct")
  part = product.copy()
  part.insert(0,"E")
  for a in range(3):
    for b in range(3):
        for c in range(3):
          for d in range(3):
            for e in range(2):
              for f in range(2):
                unique_combinations.append([[part[a], part[b], part[c], part[d]],product[e], movements[f]])
  return unique_combinations

states = get_states(warehouse, products, movements)
print(states)
print(len(states))

"""## Actions
All possible actions are determined by calling function get_actions
"""

def get_actions(warehouse):
  unique_combinations = []
  if (len(warehouse) != 4):
    print("ERROR: Warehouse_Size not correct")
  for a in range(len(warehouse)):
    unique_combinations.append(warehouse[a])
  return unique_combinations

actions = get_actions(warehouse)
print(actions)
print(len(actions))

"""##Transistion Probability Matrix"""

def valid_transition(start, ziel, type):
  counter1 = 0
  counter2 = 0
  for x in range(len(start[0])):
    if start[0][x] == ziel[0][x]:
      counter1 += 1
    if start[0][x] != ziel[0][x]:
      counter2 += 1
  #check, if transition for stock and unstock is valid by ccounting the number of bin changes and whether the bin change fits to the product and movement 
  if (start[0][type] == "E" and ziel[0][type] == start[1] and start[2] == "stock" and counter1 == 3 and counter2 == 1):
    return True
  elif (ziel[0][type] == "E" and start[0][type] == start[1]  and start[2] == "unstock" and counter1 == 3 and counter2 == 1):
    return True
  else:
    False

def get_transition_matrix(stat, prob, act):
  trans_mat = []
  for start in range(len(stat)):
    row =[]
    for ziel in range(len(stat)):
      if valid_transition(stat[start], stat[ziel], act):
        row.append(prob[stat[ziel][1]])
      else: 
        row.append(0)
    trans_mat.append(row)
  return trans_mat

# get for each action a transition probability matrix
trans_matrix_0 = get_transition_matrix(states, probability,0)
trans_matrix_1 = get_transition_matrix(states, probability,1)
trans_matrix_2 = get_transition_matrix(states, probability,2)
trans_matrix_3 = get_transition_matrix(states, probability,3)

"""## Fulfill stochastic requirements"""

#set the main diagonal of the States x States Matrix to 1
if (len(trans_matrix_0) == len(trans_matrix_1) == len(trans_matrix_2) == len(trans_matrix_3)):
  for i in range(len(trans_matrix_0)):
    if sum(trans_matrix_0[i]) == 0:
      trans_matrix_0[i][i] = 1.0
    if sum(trans_matrix_1[i]) == 0:
      trans_matrix_1[i][i] = 1.0
    if sum(trans_matrix_2[i]) == 0:
      trans_matrix_2[i][i] = 1.0
    if sum(trans_matrix_3[i]) == 0:
      trans_matrix_3[i][i] = 1.0
else:
  print("Fehler")
print("eliminated zeros in trans_matrix")

def check_norm(matrix):
  for row in matrix:
    if(sum(row) != 1):
      print("Achtung! Summe nicht 1")
      break
  print("Success, Sum of all Rows is correct")

#check sum of each row, whether matrices fulfill stochastic requirement
norm_trans_matrix_0 = normalize(trans_matrix_0, axis=1, norm='l1')
norm_trans_matrix_1 = normalize(trans_matrix_1, axis=1, norm='l1')
norm_trans_matrix_2 = normalize(trans_matrix_2, axis=1, norm='l1')
norm_trans_matrix_3 = normalize(trans_matrix_3, axis=1, norm='l1')

check_norm(norm_trans_matrix_0)
check_norm(norm_trans_matrix_1)
check_norm(norm_trans_matrix_2)
check_norm(norm_trans_matrix_3)

"""## Reward Matrix"""

# return reward per bin
def reward(bin):
  if bin == 0:
    return 3
  elif bin == 1 or bin == 2:
    return 2
  elif bin == 3:
    return 1
  else:
    print("Fehler im Reward")

# check for valid reward by validating the movement type and the affected bin by that product and movement 
def valid_reward(start, ziel):
  if (start[2] =="stock" ):
    if start[0][ziel] == "E":
      return reward(ziel)
    else:
      return 0

  if (start[2] == "unstock"):
    if start[0][ziel] == start[1]:
      return reward(ziel)
    else: 
      return 0

def get_reward_matrix(states, actions):
  matrix = []
  for start in range(len(states)):
    row = []
    for ziel in range(len(actions)):
      row.append(valid_reward(states[start], ziel))
    matrix.append(row)
  return matrix

""" For visualization purpose the number of rewards and all rewards are printed.
 Matrix must fulfill SxA property 
"""

rewards = get_reward_matrix(states, actions)
print(len(rewards))
print(rewards)

"""## Assemble 
Matrices are converted to numpy arrays for processing in MDP Toolbox. Shapes of numpy arrays is printed to validate the correct shape.

T = AxSxS

R = SxA
"""

np.array(norm_trans_matrix_0)
np.array(norm_trans_matrix_1)
np.array(norm_trans_matrix_2)
np.array(norm_trans_matrix_3)
np.array(rewards)

T = np.array([norm_trans_matrix_0, norm_trans_matrix_1, norm_trans_matrix_2,norm_trans_matrix_3])
R = np.array(rewards)

print(T.shape)
print(R.shape)

def get_rec_action(policy, state):
    if len(policy)!=len(states):
        return "Policy does not match number of states!"
    #give state and get action(position based on chosen policy)
    for it_state in range(len(states)):
        #find position of state to search policy at this posiiton 
        if states[it_state]==state:
            return actions[policy[it_state]]
    return "Input state is invalid, check shape and items!"

"""#MDP

##Determination of policies

Definition of the mdp with discount factor, maximal iterations, the tranisition probability matrix and the reward matrix
"""

all_policies = {}
discountFactor = 0.6
iterations = 10000

#FiniteHorizon
fh_class = mdp.FiniteHorizon(T, R, discountFactor, N = iterations)
fh_class.run()
policy = []
policy_iterations = fh_class.policy
for state in policy_iterations:
  policy.append(state[iterations-1])
all_policies["FiniteHorizon"] = tuple(policy)
print("FiniteHorizon duration:", fh_class.time)
print("FiniteHorizon iterations: N.A")

print("_________________")

#PolicyIteraiton
pi_class = mdp.PolicyIteration(T, R, discountFactor, max_iter=iterations)
pi_class.run()
all_policies["PolicyIteration"] = pi_class.policy
print("PolicyIteraiton duration:", pi_class.time)
print("PolicyIteraiton iterations:", pi_class.iter)

print("_________________")

#PolicyIterationModified
pim_class = mdp.PolicyIterationModified(T, R, discountFactor, max_iter=iterations)
pim_class.run()
all_policies["PolicyIterationModified"] = pim_class.policy
print("PolicyIterationModified duration:", pim_class.time)
print("PolicyIterationModified iterations:", pim_class.iter)

print("_________________")

#RelativeValueIteration
rvi_class = mdp.RelativeValueIteration(T, R, discountFactor, max_iter=iterations)
rvi_class.run()
all_policies["RelativeValueIteration"] = rvi_class.policy
print("RelativeValueIteration duration:", rvi_class.time)
print("RelativeValueIteration iterations:", rvi_class.iter)

print("_________________")

#ValueIteration
vi_class = mdp.ValueIteration(T, R, discountFactor, max_iter=iterations)
vi_class.run()
all_policies["ValueIteration"] = vi_class.policy
print("ValueIteration duration:", vi_class.time)
print("ValueIteration iterations:", vi_class.iter)

print("_________________")

#ValueIterationGS
vigs_class = mdp.ValueIterationGS(T, R, discountFactor, max_iter=iterations)
vigs_class.run()
all_policies["ValueIterationGS"] = vigs_class.policy
print("ValueIterationGS duration:", vigs_class.time)
print("ValueIterationGS iterations:", vigs_class.iter)

#print policies for visualization purposes 
for key in all_policies:
  print(key)
  print(all_policies[key])

"""#Simulation 
For evaluation purposes an simulation of tasks the agent performs is conducted. The resulting reward after all iterations of tasks is returned
"""

def simulate(policy, iterations=100, randomstart=False, druck=False):
    reward=[]

    # either start with random state or empty warehouse with random storing task
    if randomstart:
        #state = (random.choices(states, k=1)[0]).copy()
        state= [['p2', 'p1', 'E', 'E'], 'p2', 'stock']
    else:
        warhouse_state = [warehouse]
        warhouse_state.append("store")
        warhouse_state.append(random.choices(products, tuple(probabilities_only), k=1)[0])
        state = warhouse_state.copy()

    for i in range(iterations):
        if druck:
            print()
            print("iteration", i+1)
        # validate states, if impossible movement is suggested 
        # unstock item that is not in warehouse
        if state[-1] == "unstock" and state[-2] not in state[0]:
            state[-1] = "stock"
            if druck:
                print("changed to store", state)
        # stock item in full warehouse
        if state [-1] == "stock" and "E" not in state[0]:
            state[-1]="unstock"
            if druck:
                print("changed to unstore", state)
            # unstock and stock not possible
            if (state[-2] not in state[0]):
                state[-2] = random.choices(products, tuple(probabilities_only), k=1)[0]
                if druck:
                    print("changed item", state)
        
        
        #get recommended action based on policy and current state  
        action = get_rec_action(policy, state)
        if druck:
            print("start", state)
            print("action", action)         
        
        #find index of action and state
        for it_action in range(len(actions)):
            if action == actions[it_action]:
                break       
        for it_state in range(len(states)):
            if state == states[it_state]:
                break
        
        # add reward based on state and action
        reward.append(rewards[it_state][it_action])
        if druck:
            print("reward", rewards[it_state][it_action])
        
        # find possible next states(indices) from transition matrix
        possible_next = list(np.where((T[it_action][it_state]) != 0)[0])
        probabilites_next = []
        for i in possible_next:
            probabilites_next.append(T[it_action][it_state][i])
        if druck:
            print("possible next", possible_next)
            print("probabilities next", probabilites_next)

        # pick next state based on assigned probability 
        it_state = random.choices(possible_next, probabilites_next, k=1)[0]
        state = states[it_state].copy()
        if druck:
            print("result",it_state, state)
        
        
    #return sum of reward
    return sum(reward)

"""# Simulation Results"""

rounds = 100
print("Maximum Reward:", rounds * 3)
print("")
# loop over policy dictionary to print policy, total reward and reward per iteration
for key, value in all_policies.items():
  rew = simulate(value,iterations=rounds, randomstart=True, druck=False)
  print(key,":")
  print("  total reward:", rew)
  print("  average reward per iteration:", rew / rounds)
  print("")

simulate(value,iterations=5, randomstart=True, druck=True)