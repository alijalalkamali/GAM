import os.path
from psychsim.pwl import *
from psychsim.reward import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *

dir_path = os.path.dirname(os.path.realpath(__file__))
ACTION_PATH = os.path.join(dir_path, 'action_list.txt')
AGENT_PATH = os.path.join(dir_path, 'agent_list.txt')
STATE_PATH = os.path.join(dir_path, 'state_list.txt')


class AfroWorldInitializer:
    def __init__(self, world):
        self.world = world
        
        self.init_agent()
        self.init_action()
        self.init_state()
        # import pdb; pdb.set_trace()
        # breakpoint to see any changes in world
    
    def init_agent(self):
        agent_names = [line.rstrip('\n') for line in open(AGENT_PATH)]
        for agent_name in agent_names:
            agent = Agent(agent_name)
            agent.setHorizon(1)
            self.world.addAgent(agent)
    
    def init_action(self):
        action_names = [line.rstrip('\n') for line in open(ACTION_PATH)]
        # bind actions to agents
        for agent in self.world.agent.values():
            for action_name in action_names:
                agent.addAction({'verb': action_name})
        
        # set dynamics
    
    def init_state(self):
        state_names = [line.rstrip('\n') for line in open(STATE_PATH)]
        for agent in self.world.agent.values():
            for state_name in state_names:
                # set default to 100 
                # (TODO: change the default number)
                agent.setState(state_name, 100)

if __name__ == '__main__':
    world = World()
    awi = AfroWorldInitializer(world)