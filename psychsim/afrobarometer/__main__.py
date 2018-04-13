import os.path
from psychsim.pwl import *
from psychsim.reward import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *

import configure

dir_path = os.path.dirname(os.path.realpath(__file__))
ACTION_PATH = os.path.join(dir_path, 'action_list.txt')
AGENT_PATH = os.path.join(dir_path, 'agent_list.txt')
STATE_PATH = os.path.join(dir_path, 'state_list.txt')


class AfroWorldInitializer:
    def __init__(self, world):
        self.world = world
        
        self.init_agent()
        self.init_state()
        self.init_action()
        self.set_reward()
        
        # breakpoint to see any changes in world
    
    def init_agent(self):
        r1 = Agent('resident1')
        r1.setHorizon(1)
        self.world.addAgent(r1)
        # r2 = Agent('resident2')
        # r2.setHorizon(1)
        # self.world.addAgent(r2)
    
    def init_action(self):
        # bind actions to agents
        agent = self.world.agents['resident1']
        for action_name, value in configure.actions_trust.items():
            for state in value:
                action = agent.addAction({'verb': action_name})
                prob_increase = value[state]
                prob_decrease = 1. - prob_increase
                tree = makeTree({'distribution':[
                    (incrementMatrix(stateKey(agent.name, state), 10),
                     prob_increase),
                    (incrementMatrix(stateKey(agent.name, state), -10),
                     prob_decrease)
                    ]})
                self.world.setDynamics(stateKey(agent.name, state), action, tree)
        
        # set dynamics
    
    def init_state(self):
        for agent in self.world.agents.values():
            for state_name in configure.states:
                # set default to 100 
                # (TODO: change the default number)
                self.world.defineState(agent.name, state_name, int)
                self.world.setState(agent.name, state_name, 50)
                
    def set_reward(self):
        for agent in self.world.agents.values():
            agent.setReward(maximizeFeature(stateKey(agent.name, 'economy')), 0.1)

if __name__ == '__main__':
    world = World()
    awi = AfroWorldInitializer(world)
    world.setOrder(world.agents.keys())
    result = world.step()
    world.explain(result, 4)
