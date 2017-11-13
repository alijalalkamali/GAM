import sys
sys.path.append('psychsim')
from psychsim.reward import *
from psychsim.pwl import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *

#########################Actor#######################
world = World()
US = Agent('United States')
US.setHorizon(1)
world.addAgent(US)

UK = Agent('Ukraine')
UK.setHorizon(1)
world.addAgent(UK)

######################states##########################

world.defineState(US.name,'force',float)
world.defineState(US.name,'cooperation',float)
world.defineState(US.name,'welfare',float)
world.defineState(US.name,'military',float)
world.defineState(US.name,'tie',float)
world.defineState(US.name,'economy',float)
world.defineState(US.name,'price',float)
world.defineState(US.name,'tension',float)
world.defineState(US.name,'trade',float)

### set initial state of world.

world.setState(US.name,'force',0.5)
world.setState(US.name,'cooperation',0.5)
world.setState(US.name,'welfare',0.5)
world.setState(US.name,'military',0.5)
world.setState(US.name,'tie',0.5)
world.setState(US.name,'economy',0.5)
world.setState(US.name,'price',0.5)
world.setState(US.name,'tension',0.5)
world.setState(US.name,'trade',0.5)

##############action#################################
urgeAction = US.addAction({'verb': 'urge'})
tree = makeTree({'distribution': [(incrementMatrix(stateKey(urgeAction['subject'], 'tension'), 1.),0.68), # Prob of Action increasing the state
    (incrementMatrix(stateKey(urgeAction['subject'], 'tension'), 1.), 1.-0.68)]}) # Prob of action decreasing the state
world.setDynamics(stateKey(urgeAction['subject'], 'tension'), urgeAction, tree)



urgeAction = US.addAction({'verb': 'urge'})
tree = makeTree({'distribution': [(incrementMatrix(stateKey(urgeAction['subject'], 'tension'), 1.),0.68), # Prob of Action increasing the state
    (incrementMatrix(stateKey(urgeAction['subject'], 'tension'), 1.), 1.-0.68)]}) # Prob of action decreasing the state
world.setDynamics(stateKey(urgeAction['subject'], 'tension'), urgeAction, tree)



urgeAction = US.addAction({'verb': 'urge'})
tree = makeTree({'distribution': [(incrementMatrix(stateKey(urgeAction['subject'], 'tension'), 1.),0.68), # Prob of Action increasing the state
    (incrementMatrix(stateKey(urgeAction['subject'], 'tension'), 1.), 1.-0.68)]}) # Prob of action decreasing the state
world.setDynamics(stateKey(urgeAction['subject'], 'tension'), urgeAction, tree)


urgeAction = US.addAction({'verb': 'urge'})
tree = makeTree({'distribution': [(incrementMatrix(stateKey(urgeAction['subject'], 'tension'), 1.),0.68), # Prob of Action increasing the state
    (incrementMatrix(stateKey(urgeAction['subject'], 'tension'), 1.), 1.-0.68)]}) # Prob of action decreasing the state
world.setDynamics(stateKey(urgeAction['subject'], 'tension'), urgeAction, tree)





######################################################


world.defineState(US.name,'y',int)
world.defineState(US.name, 'goal_x', int)
world.defineState(US.name, 'goal_y', int);



print(world.agents.keys())
