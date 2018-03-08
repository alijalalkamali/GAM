'''
Basic implementation of SRL processing tasks discussed on Feb 16.
'''

import tree_builder
import os.path
# from corenlp_xml.document import Document

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

    # def find_coref(self, corenlp_filename, possesive_pronoun_node):
    #     f = open(corenlp_filename, 'rb')
    #     xml_string = f.read()
    #     f.close()
    #     doc = Document(xml_string)

    #     possesive_pronoun_id = possesive_pronoun_node.label['id']

    #     for coref in doc.coreferences:
    #         for mention in coref.mentions:
    #             _sen_id = mention.sentence.id
    #             _w_id = mention.head.id
    #             if sen_id == _sen_id and _w_id == possesive_pronoun_id:
    #                 for _mention in coref.mentions:
    #                     if _mention.text in self.actor_list:
    #                         return [self.actor_list[_mention.text]]


    #     return []
    
    def process_sentence(self, filename, sen_id, w_id):
        '''
        :param 
        :type filename: string, sen_id: int, w_id: int
        :rtype: tuple(actors, action verb, state, stative verb)
        '''
        
        srl_filename = '%s.txt.srl'%filename
        coref_filename = '%s.xml'%filename
        # self.tb.filename = srl_filename
        if not os.path.isfile(srl_filename):
            print('%s file missing'%srl_filename)
            return
        # if not os.path.isfile(coref_filename):
        #     print('%s file missing'%coref_filename)
        #     return
        
        sen = self.tb.get_ith_sentence_from_file(srl_filename, sen_id)

        root_nodes = self.tb.build_tree(sen)
        
        # In case there are multiple roots.
        for root_node in root_nodes:
            # import pdb; pdb.set_trace()
            # Finding state node by provided word id
            state_node = root_node.find('id', w_id)
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
                    possesive_pronoun_node = state_node[0].find('deprel', 'poss')
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
                # (TODO: Make unified directory resolution.)
                filename = 'data/ClearnlpOutput/%s'%filename
                print('processing '+filename)
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
    
    
    # (TODO: Iterate through the results.)
    for ans in sp.process_list('list.txt'):
        pass
    
if __name__ == '__main__':
    main()