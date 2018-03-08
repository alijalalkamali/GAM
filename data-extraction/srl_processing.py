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
        self.actor_path = 'data/params/country_nationality.txt'
        self.actor_list = self.get_country_list(self.actor_path).keys()
        
        # self.states_path = 'params/states.txt'
        # self.base_forms = self.file_loader(self.states_path)
                
        self.tb = tree_builder.TreeBuilder()
        
    def get_country_list(self, country_list_file):
        country_list = {}
        with open(country_list_file) as f:
            for line in f:
                line = line.strip().split('\t')
                if len(line) > 0:
                    _country = line[0]
                    for country in line:
                        country_list[country] = _country
        return country_list
    
    def file_loader(self, filename, col=0):
        '''
        Read certain coloumn from text file.
        '''
        with open(filename) as fp:
            ret = fp.readlines()
            ret = [line.split()[col] for line in ret]
            return ret
        return None

    def process_sentence(self, filename, sen_id, w_id):
        '''
        :param 
        :type filename: string, sen_id: int, w_id: int
        :rtype: tuple(actors, action verb, state, stative verb)
        '''
        
        srl_filename = '%s.txt.srl'%filename
        coref_filename = '%s.xml'%filename
        # self.tb.filename = srl_filename
        
        sen = self.tb.get_ith_sentence_from_file(srl_filename, sen_id)

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
                state = state_node[0].label['form']
                print('state:%s'%str(state))
                
                # lemma here instead of form
                stative_verb_nodes = root_node.find_list(
                    'lemma', self.stative_verb_list) 
                # import pdb; pdb.set_trace()
                if not stative_verb_nodes:
                    print('no stative verb found in %d'%sen_id)
                else:
                    stative_verbs = [n.label['form'] for n in stative_verb_nodes]
                    print('stative verbs:%s'%str(stative_verbs))
                    
                    # Change find to direct children
                    possesive_pronoun_node = state_node.find('deprel', 'poss')
                    # Not checking if actor is from state's subtree.
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


    def process_list(self, list_filename):
        '''
        :type filename: string
        :rtype list(tuple)
        '''
        if not os.path.isfile(list_filename):
            print('%s file missing'%'filename')
            return
        
        with open(list_filename) as f:
            for line in f:
                filename, sen_id, w_id, word = tuple(line.strip().split(','))
                yield self.process_sentence(filename, int(sen_id), int(w_id))
        

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
        # (TODO: Iterate through the results.)
        sp.process_list('list.txt')
    
if __name__ == '__main__':
    main()