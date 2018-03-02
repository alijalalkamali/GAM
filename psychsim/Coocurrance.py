from psychsim.pwl import *
from psychsim.reward import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *

import pandas as pd


class GAMWorldStateInitializer:
    def __init__(self, Coocurrances, World, agents):
        self.DEFAULT_ACTION_WEIGHT = 1
        self.DEFAULT_STATE_VALUE = 100

        self.cooc = Coocurrances
        self.world = World
        self.agents = agents

        self.states = [i for i in self.cooc.columns if i not in ['X', 'Total Count w/ Actions', 'Total Count Overall']]

        self.action_names = cooc.X.unique()
        self.action_probabilities = self.getActionProbabilities()

        self.actions = []

    def setStates(self, stateDefaults=None):
        # For each agent Create State Variables for each column name
        for a in self.agents:
            for i in self.states:
                self.world.defineState(a.name, i, int)
                if stateDefaults is not None:
                    self.world.setState(a.name, i, stateDefaults[i])
                else:
                    self.world.setState(a.name, i, 100)
                print a.name + " " + str(i) + " " + str(self.world.getState(a1.name, i))

    def getActionProbabilities(self):
        action_probabilities = {}
        for action_name in self.action_names:
            for state in self.states:
                val = self.cooc[state][self.cooc.X == action_name].iloc[0]
                if not isinstance(val, str):
                    continue
                else:
                    prob = val.split("-")
                    probIncrease = int(prob[0]) / 100.0
                    probDecrease = int(prob[1]) / 100.0
                    action_probabilities[action_name] = {'state': state,
                                                         'probIncrease': probIncrease,
                                                         'probDecrease': probDecrease}
        return action_probabilities

    def createActions(self, pos_vars_weights=None, neg_vars_weights=None):
        for agent in self.agents:
            for action_name, variables in self.action_probabilities.iteritems():
                state = variables['state']
                if state in pos_vars_weights:
                    weight = pos_vars_weights[state]
                elif state in neg_vars_weights:
                    weight = neg_vars_weights[state]
                else:
                    weight = self.DEFAULT_ACTION_WEIGHT

                tree_label = agent.name + "distribution for " + state

                action = agent.addAction({'verb': action_name})
                print action

                # why is it 'subject'? should it not be 'object'?
                tree = makeTree({tree_label: [
                    (incrementMatrix(stateKey(action['subject'], state), weight), variables['probIncrease']),
                    (incrementMatrix(stateKey(action['subject'], state), weight), variables['probDecrease'])
                    ]})

                self.world.setDynamics(stateKey(action['subject'], state), action, tree)

    # Currently applies termination condition to all agents
    def setTerminationCondition(self, goal_state, end_value):
        # Any of the "positive" state variables turns to 0
        for a in self.agents:
            tree = makeTree({'if': equalRow(stateKey(a.name, goal_state), end_value),
                             True: True, False: False})
            self.world.addTermination(tree)

    # Currently set same reward for all agents
    def setRewardCondition(self, rewardType, reward_state1, reward_state2=None):
        for a in self.agents:
            if rewardType == "max":
                a.setReward(maximizeFeature(reward_state1))
            elif rewardType == "min":
                a.setReward(minimizeFeature(reward_state1))
            elif rewardType == "minDifference" and reward_state2 is not None:
                a.setReward(minimizeDifference(reward_state1, reward_state2))
            else:
                print "Cannot set reward condition"


# Read In Coocurrance file
cooc = pd.read_csv("CooccuranceOutput2013.csv")

# Create World
world = World()

# Create Agents
a1 = Agent("A1")
a1.setHorizon(5)
a2 = Agent("A2")
a2.setHorizon(5)

# Add agents to world
world.addAgent(a1)
world.addAgent(a2)

# Set Goal for each agent to mazimize state "positive" variables and minimize "negative" variables
# vars should have positive and negative tags and weights in input document
# some vars are neutral?
pos_vars_weights = {'force': 1.0, 'cooperation': 1.0, 'welfare': 1.0, 'military': 1.0, 'economy': 1.0, 'trade': 1.0}
neg_vars_weights = {'price': 1.0, 'tension': 1.0}

gwsi = GAMWorldStateInitializer(cooc, world, [a1, a2])
gwsi.setStates()
gwsi.createActions(pos_vars_weights=pos_vars_weights, neg_vars_weights=neg_vars_weights)

# Run Simulation for X number of steps
print "Start Simulation"
world.setOrder(world.agents.keys())

# Set Termination Conditions
gwsi.setTerminationCondition("economy", 0)  # economy tanks
gwsi.setTerminationCondition("economy", 200)  # OR economy doubles

# Set Rewards
gwsi.setRewardCondition("max", "welfare")
gwsi.setRewardCondition("min", "tension")

# while not world.terminated():
#     result = world.step()
#     world.explain(result, 1)
#     world.explain(result, 2)
#     world.explain(result, 3)
#     world.explain(result, 4)
#     world.explain(result, 5)
#     step = step + 1


# How to encode the following "Reward Functions"?
# Fragile State Index
    # detect for economic decline
    # detect for increase in tension
    # detect for decrease in cooperation
    # detect for increase in force
# Conflict database (diplomacy)
    # detect for increase in military
    # detect for increase in force
# Economy (GDP)
    # detect for changes in economy, trade, welfare,
    # price?








