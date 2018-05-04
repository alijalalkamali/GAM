from psychsim.pwl import *
from psychsim.reward import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *

class AfroWorldInitializer:
    def __init__(self, world,):
        self.world = world
        
        # breakpoint to see any changes in world
    
    def init_agent(self, name):
        r1 = Agent(name)
        # r1.setHorizon(1)
        self.world.addAgent(r1)
    
    def init_action(self, agent_name, action_list=[]):
        # bind actions to agents
        agent = self.world.agents[agent_name]
        
        # utility function
        # utility = 
        
        action1 = agent.addAction({'verb': 'vote'})
        state = 'economy'
        tree = makeTree(
            {'if':equalRow(stateKey(agent.name, 'close2party'), 1),
             True: incrementMatrix(stateKey(agent.name, state), 10),
             False: incrementMatrix(stateKey(agent.name, state), -10)})
        self.world.setDynamics(stateKey(agent.name, state), action1, tree)  
        
        action2 = agent.addAction({'verb': 'no_vote'})
        
        
        
        
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
        
    
    def init_state(self, agent_name, state_list):
        agent = self.world.agents[agent_name]
        for state_name, state_val in state_list.items():
            self.world.defineState(agent.name, state_name, state_val['type'])
            self.world.setState(agent.name, state_name, state_val['val'])
                # import pdb; pdb.set_trace()
                
    def set_reward(self):
        for agent in self.world.agents.values():
            # Here the second parameter of setReward is confusing me
            agent.setReward(maximizeFeature(stateKey(agent.name, 'economy')), 10)