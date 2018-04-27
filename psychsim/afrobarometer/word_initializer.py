from psychsim.pwl import *
from psychsim.reward import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *

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
        r2 = Agent('resident2')
        r2.setHorizon(1)
        self.world.addAgent(r2)
    
    def init_action(self):
        # bind actions to agents
        agent = self.world.agents['resident1']
        
        # utility function
        # utility = 
        
        action = agent.addAction({'verb': 'vote'})
        state = 'economy'
        tree = makeTree(
            {'if':equalRow(stateKey(agent.name, 'close2party'), '1'),
             True: incrementMatrix(stateKey(agent.name, state), 10),
             False: incrementMatrix(stateKey(agent.name, state), -10)})
        
        
        # for action_name, value in configure.actions_trust.items():
        #     for state in value:
        #         action = agent.addAction({'verb': action_name})
        #         prob_increase = value[state]
        #         prob_decrease = 1. - prob_increase
        #         # Probablistic tree
        #         # 
        #         # tree = makeTree({'distribution':[
        #         #     (incrementMatrix(stateKey(agent.name, state), 10),
        #         #      prob_increase),
        #         #     (incrementMatrix(stateKey(agent.name, state), -10),
        #         #      prob_decrease)
        #         #     ]})
                
        #         tree = makeTree(
        #             {'if':greaterThanRow(stateKey(agent.name, 'trust'),50)
        #             (stateKey(agent.name, state),
        #             100*(prob_increase-0.5)))
        #         self.world.setDynamics(stateKey(agent.name, state), action, tree)
        
        # set dynamics
        self.world.setDynamics(stateKey(agent.name, state), action, tree)
    
    def init_state(self):
        for agent in self.world.agents.values():
            for state_name, state_val in configure.states.items():
                # set default to 100 
                # (TODO: change the default number)
                self.world.defineState(agent.name, state_name, int)
                self.world.setState(agent.name, state_name, state_val)
                # import pdb; pdb.set_trace()
                
    def set_reward(self):
        for agent in self.world.agents.values():
            agent.setReward(maximizeFeature(stateKey(agent.name, 'economy')), 0.1)