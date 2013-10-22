# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
    self.tmp_values = util.Counter()
    states = self.mdp.getStates()
    
    for i in range(self.iterations):
        for state in states:
            self.tmp_values[state] = self.getQValue(state, self.getPolicy(state))
        self.values = self.tmp_values
    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    if self.mdp.isTerminal(state):
        return 0
    
    possible_states = self.mdp.getTransitionStatesAndProbs(state, action)
    q_value = 0
    for possible_state in possible_states:
        next_state, prob = possible_state
        reward = self.mdp.getReward(state, action, next_state)
        value = self.getValue(next_state)
        q_value += prob*(reward + self.discount*value)
        
    return q_value

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    print state
    possible_actions = self.mdp.getPossibleActions(state)
    print possible_actions
    best_q_value = -float('inf')
    best_action = None
    for action in possible_actions:
        q_value = self.getQValue(state, action)
        print q_value
        if q_value > best_q_value:
            best_action = action
    print best_action
    return best_action
  
  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
