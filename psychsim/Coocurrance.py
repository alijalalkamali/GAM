from psychsim.pwl import *
from psychsim.reward import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *
import cmd

import pandas as pd

import argparse

class GAMWorldStateInitializer:
    def __init__(self, Coocurrances, World, agents):
        self.DEFAULT_ACTION_WEIGHT = 1.
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
                print a.name + " " + str(i) + " " + str(self.world.getState(a.name, i))

    def getActionProbabilities(self):
        action_probabilities = {}
        for action_name in self.action_names:
            action_probabilities[action_name] = {}
            for state in self.states:
                val = self.cooc[state][self.cooc.X == action_name].iloc[0]
                if not isinstance(val, str):
                    continue
                else:
                    prob = val.split("-")
                    probIncrease = abs(int(prob[0]) / 100.0)
                    probDecrease = abs(int(prob[1]) / 100.0)
                    action_probabilities[action_name][state] = {'probIncrease': probIncrease,
                                                                'probDecrease': probDecrease}
        return action_probabilities

    def createActions(self, pos_vars_weights=None, neg_vars_weights=None):
        for agent in self.agents:
            for action_name, states in self.action_probabilities.iteritems():
                for state, probabilities in states.iteritems():
                    if state in pos_vars_weights:
                        weight = pos_vars_weights[state]
                    elif state in neg_vars_weights:
                        weight = neg_vars_weights[state]
                    else:
                        weight = self.DEFAULT_ACTION_WEIGHT

                    action = agent.addAction({'verb': action_name})

                    tree = makeTree({'distribution': [
                        (incrementMatrix(stateKey(action['subject'], state), weight), probabilities['probIncrease']),
                        (incrementMatrix(stateKey(action['subject'], state), weight), probabilities['probDecrease'])
                        ]})

                    self.world.setDynamics(stateKey(action['subject'], state), action, tree)

    # Currently applies termination condition to all agents
    def setTerminationCondition(self, goal_state, end_value):
        # Any of the "positive" state variables turns to 0
        for a in self.agents:
            tree = makeTree({'if': equalRow(stateKey(a.name, goal_state), end_value),
                             True: True, False: False})
            self.world.addTermination(tree)

    # Prompts User to Set Termination Conditions
    def getTerminationConditions(self):
        setting_conditions = raw_input("Y to set termination conditions.  To skip, press any other key. ")
        if setting_conditions == "Y":
            while setting_conditions == "Y":
                print self.states
                goal_state = ""
                while goal_state not in self.states:
                    goal_state = raw_input("Select State: ")
                    if goal_state in self.states:
                        break
                    print "Not a valid state"

                end_value = None
                while end_value is None:
                    end_value = raw_input("Set Termination State Value: ")
                    if not end_value[0].isalpha():
                        end_value = int(end_value)
                        break
                    print "Not a valid target value"

                print "Setting Termination Condition: if {state} reaches value of {target}".format(state=goal_state, target=end_value)
                self.setTerminationCondition(goal_state, end_value)
                setting_conditions = raw_input("Y to set more termination conditions.  To continue, press any other key. ")

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

    # Prompts User to Set Reward Conditions
    def getRewardCondition(self):
        setting_conditions = raw_input("Y to set reward conditions.  To skip, press any other key. ")
        if setting_conditions == "Y":
            while setting_conditions == "Y":
                print self.states
                goal_state = ""
                while goal_state not in self.states:
                    goal_state = raw_input("Select Goal State: ")
                    if goal_state in self.states:
                        break
                    print "Not a valid state"

                min_max = None
                while min_max is None:
                    min_max = raw_input("Minimize(1), Maximize(2), or Minimize Difference(3)?: ")
                    if not min_max[0].isalpha():
                        min_max = int(min_max)
                        if min_max == 1:
                            min_max = "min"
                            break
                        elif min_max == 2:
                            min_max = "max"
                            break
                        elif min_max == 3:
                            min_max = "minDifference"
                            break
                        else:
                            pass
                    print "Not a valid target value"

                goal_state2 = None
                if min_max == "minDifference":
                    print self.states
                    goal_state2 = ""
                    while goal_state2 not in self.states:
                        goal_state2 = raw_input("Select State to Minimize difference with {state}: ".format(state=goal_state))
                        if goal_state2 in self.states:
                            break
                        print "Not a valid state"

                print "Setting Reward Condition"
                self.setRewardCondition(min_max, goal_state, reward_state2=goal_state2)
                setting_conditions = raw_input("Y to set more reward conditions.  To continue, press any other key. ")

    # Set weights for states
    def setWeights(self):
        set_weights = raw_input("Y to set weights. To skip, press any other key. ")
        pos_vars_weights = {}
        neg_vars_weights = {}
        if set_weights != "Y":
            for state in self.states:
                pos_vars_weights[state] = 1
        else:
            i = 0
            while i < len(self.states):
                state_weight = raw_input("Set weight for {state}: ".format(state=self.states[i]))
                if not state_weight.isalpha():
                    state_weight = int(state_weight)
                    if state_weight < 0:
                        neg_vars_weights[self.states[i]] = state_weight
                    else:
                        pos_vars_weights[self.states[i]] = state_weight
                    i = i + 1
                else:
                    print "Weight for state variable must be an integer"
        return pos_vars_weights, neg_vars_weights


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cf', help="Coocurrance File", required=True)
    parser.add_argument('-a', help="Number of Agents", default=2)
    parser.add_argument('--ho', help="Horizon", default=3)
    parser.add_argument('-v', help="Verbose", default=False)
    args = parser.parse_args()

    # Read In Coocurrance file
    cooc = pd.read_csv(args.cf)

    # Create World
    print "Creating World"
    world = World()

    # Create Agents
    print "Creating Agents"
    agents = []
    for i in range(1, int(args.a) + 1):
        agent_name = "A" + str(i)
        print "Creating Agent: {agent}".format(agent=agent_name)
        agent = Agent(agent_name)
        agent.setHorizon(args.ho)
        agents.append(agent)
        print "Adding Agent to World"
        world.addAgent(agent)

    gwsi = GAMWorldStateInitializer(cooc, world, agents)

    print "Set Weights to Prioritize States"
    # Set Goal for each agent to mazimize state "positive" variables and minimize "negative" variables
    # vars should have positive and negative tags and weights in input document
    # some vars are neutral?
    # pos_vars_weights = {'force': 1.0, 'cooperation': 1.0, 'welfare': 1.0, 'military': 1.0, 'economy': 1.0, 'trade': 1.0}
    # neg_vars_weights = {'price': 1.0, 'tension': 1.0}

    pos_var_weights, neg_var_weights = gwsi.setWeights()
    if args.v:
        print gwsi.states
        print gwsi.action_probabilities
    gwsi.setStates()
    gwsi.createActions(pos_vars_weights=pos_var_weights, neg_vars_weights=neg_var_weights)

    # Set Termination Conditions
    print "Set Termination Conditions"
    gwsi.getTerminationConditions()
    # gwsi.setTerminationCondition("economy", 90)  # economy decreases by 10 %
    # gwsi.setTerminationCondition("economy", 110)  # OR economy increases by 10%
    # gwsi.setTerminationCondition("tension", 90)  # tension decreases by 10 %
    # gwsi.setTerminationCondition("tension", 110)  # OR tension increases by 10%

    # Set Rewards
    print "Set Reward Conditions"
    gwsi.getRewardCondition()
    # gwsi.setRewardCondition("max", "economy")
    # gwsi.setRewardCondition("minDifference", "tension", "trade")

    # Run Simulation for X number of steps
    print "Start Simulation"
    world.setOrder(world.agents.keys())

    step = 0
    while not world.terminated():
        result = world.step()
        world.explain(result, 1)
        # world.explain(result, 2)
        # world.explain(result, 3)
        # world.explain(result, 4)
        # world.explain(result, 5)
        step = step + 1
        if step == 50:
            break









