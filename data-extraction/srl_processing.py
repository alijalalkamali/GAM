'''
Basic implementation of SRL processing tasks discussed on Feb 16.
'''

import tree_builder
import coref_resolution
import os.path

class SrlProcessor:
    def __init__(self):
        self.stative_path = 'data/params/stativewords.txt'
        self.stative_verb_list = self.file_loader(self.stative_path)
        self.actor_path = 'data/params/countr_map.txt'
        self.actor_list = self.file_loader(self.actor_path)
        
        # self.states_path = 'params/states.txt'
        # self.base_forms = self.file_loader(self.states_path)
                
        self.tb = tree_builder.TreeBuilder()
        
    
    def file_loader(self, filename, col=0):
        '''
        Read certain coloumn from text file.
        '''
        with open(filename) as fp:
            ret = fp.readlines()
            ret = [line.split()[col] for line in ret]
            return ret
        return None

    def process_sentence(self, file_obj, sen_id, w_id):
        '''
        :param 
        :type file_obj: object, sen_id: int, w_id: int
        :rtype: tuple(actors, action verb, state, stative verb)
        '''
        sen = self.tb.get_ith_sentence_from_file(file_obj, sen_id)

        root_nodes = self.tb.build_tree(sen)
        # In case there are multiple roots.
        for root_node in root_nodes:
            # Finding state node by provided word id
            state_node = root_node.find_list('id', w_id)
            if not state_node:
                print('no state found in sentence:%d root:%s'%(
                    sen_id, root_node.label['form']))
                # Continue to find the id in next root node.
            else:
                state = state_node.label['form']
                print('state:%s'%str(state))
                
                # lemma here instead of form
                stative_verb_nodes = root_node.find_list('lemma', self.stative_verb_list) 
                # import pdb; pdb.set_trace()
                if not stative_verb_nodes:
                    print('no stative verb found in %d'%sen_id)
                else:
                    stative_verbs = [n.label['form'] for n in stative_verb_nodes]
                    print('stative verbs:%s'%str(stative_verbs))
                    
                    possesive_pronoun_node = state_node.find('deprel', 'poss')
                    actor_nodes = root_node.find_list('form', self.actor_list)
                    actors = [n.label['form'] for n in actor_nodes]
                    if not possesive_pronoun_node:
                        print('no possesive pronoun found in %d'%sen_id)
                        # find actor directly.
                        
                        
                    else:
                        # find actor through corenlp.
                        pass
                    
                    # find action verb
                    action_verb = ''
                    
                    return (actors, action_verb, state, stative_verbs)


    def process_file(self, filename, state_list):
        '''
        :type filename: string, state_list: list(tuple)
        :rtype list(tuple)
        '''
        
        srl_filename = '%s.txt.srl'%filename
        coref_filename = '%s.xml'%filename
        
        if not os.path.isfile(srl_filename) or not os.path.isfile(coref_filename):
            print('%s file missing'%'filename')
            return
        
        # process single file
        
        self.tb.filename = srl_filename
        
        with open(filename) as file_obj:
            for state in state_list:
                yield self.process_sentence(file_obj, state[0], state[1])

def main():
    '''
    Default data directory:
    data-extraction/
    ├── data
    │   ├── 20140519
    │   │   ├── ClearNLPOutput
    │   │   │   ├──Part1
    │   │   │   ...
    │   │   │   └──PartN
    │   │   └── CoreNLPOutput
    │   │       ├──Part1
    │   │       ...
    │   │       └──PartN
    │   └── params
    │       ├── countr_map.txt
    │       └── stativewords.txt
    ├── srl_processing.py
    ├── tree_builder.py
    ├── tree_builder_test.py
    ├── tree_util.py
    └── tree_util_test.py
    '''
    sp = SrlProcessor()
    
    # Find state
    state_list = ()
    
    # Iterating through newsTexts
    for i in range(1, 2):
        sp.process_file('data/20140519/Part1/newsText%d'%i, state_list)
    
if __name__ == '__main__':
    main()