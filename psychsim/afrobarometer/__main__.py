import argparse
import configure
import copy
import logging
import os.path
import savReaderWriter
import world_initializer

from psychsim.world import *


# dir_path = os.path.dirname(os.path.realpath(__file__))
# ACTION_PATH = os.path.join(dir_path, 'action_list.txt')
# AGENT_PATH = os.path.join(dir_path, 'agent_list.txt')
# STATE_PATH = os.path.join(dir_path, 'state_list.txt')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract data from newsTexts.')
    parser.add_argument('--inputdir', '-i', required=True, help='input train file')
    parser.add_argument('--outputdir', '-o', default='outputs/', help='directory for outputs')
    parser.add_argument('--number', '-n', default=100, type=int, help='number of records')
    args = parser.parse_args()
    

    total = 0
    true_pos, true_neg, false_pos, false_neg = 0, 0, 0, 0
    
    with savReaderWriter.SavReader(args.inputdir) as reader:
        header = reader.header
        for line in reader[:args.number]:
            world = World()
            awi = world_initializer.AfroWorldInitializer(world)
            agent_name = line[0]
            state_list = copy.deepcopy(configure.preset_states)
            for state_no, state_property in configure.lookup_states.items():
                #(TODO) validation for lookup number
                state_list[state_property['name']] = {'type':state_property['type'],
                                                      'val':state_property['type'](line[state_no])}
                logger.debug('%s\'s %s, %d', agent_name, state_property['name'], line[state_no])
            awi.init_agent(agent_name)
            awi.init_state(agent_name, state_list)
            # import pdb; pdb.set_trace()
            # print(world.agents[agent_name].states)
            awi.init_action(agent_name)
            facts_vote = int(line[80])
    
            awi.set_reward()

    
            world.setOrder(world.agents.keys())
            result = world.step()
            # world.explain(result, 1)
            
            # Manually find the action. Assuming here is only one decision.
            for _result in result:
                if _result.has_key('actions'):
                    for name, action in _result['actions'].items():
                        predict_vote = 0 if action['verb']=='no_vote' else 1
                        # import pdb; pdb.set_trace()  
                        logger.info('%s %s', name, action)
                        break
                    break
            if facts_vote == 1 and predict_vote == 1:
                true_pos += 1
            elif facts_vote == 1 and predict_vote == 0:
                false_neg += 1
            elif facts_vote == 0 and predict_vote == 1:
                false_pos += 1
            else:
                true_neg += 1
    if true_pos+false_neg == 0:
        recall = 1
    else:
        recall = float(true_pos)/(true_pos+false_neg)
    if true_pos+false_pos == 0:
        precision = 1
    else:
        precision = float(true_pos)/(true_pos+false_pos)
    logger.info('true_pos: %d false_pos: %d false_neg: %d true_neg: %d',
                true_pos, false_pos, false_neg, true_neg)
    logger.info('precision:%f  recall:%f', precision, recall)
                    
            # import pdb; pdb.set_trace()
    # Validating hypothesis
    # for name in facts_vote:
    #     total += 1
    #     if 
        
    