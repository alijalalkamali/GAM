'''
Basic implementation of SRL processing tasks discussed on Feb 16.
'''

import logging
import tree_builder
import os.path
from corenlp_xml.document import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SrlProcessor:
    def __init__(self):
        self.stative_path = 'data/params/stativewords.txt'
        self.stative_verb_list = self.file_loader(self.stative_path)
        self.actor_path = 'data/params/country_nationality.txt'
        self.actor_list = self.get_country_list(self.actor_path)
        
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
        :rtype: tuple(actor,
                      actor is the direct child of state,
                      action verb,
                      state,
                      stative verb,
                      possesive pronoun,
                      possesive pronoun resolution)
                      Here should have possesive pronoun is the direct child 
        '''
        actor, actor_is_dc = '_', '_'
        action_verb, state, stative_verb, possesive_pronoun = '_', '_', '_', '_'
        possesive_pronoun_reso = '_'
        
        prefix_name = os.path.join(*(filename.split('/')[:-2]))
        part_name = os.path.join(*(filename.split('/')[-2:]))
        srl_filename = os.path.join(
            prefix_name, 'ClearNLPOutput', '%s.txt.srl'%part_name)
        corenlp_filename = os.path.join(
            prefix_name, 'CoreNLPOutput', '%s.xml'%part_name)

        if not os.path.isfile(srl_filename):
            logger.info('%s file missing'%srl_filename)
            return
        if not os.path.isfile(corenlp_filename):
            logger.info('%s file missing'%corenlp_filename)
            return
        
        sen = self.tb.get_ith_sentence_from_file(srl_filename, sen_id)

        root_nodes = self.tb.build_tree(sen)
        
        # In case there are multiple roots.
        for root_node in root_nodes:
            # Finding state node by provided word id
            state_node = root_node.find('id', w_id)
            if not state_node:
                logger.debug('no state found in sentence:%d root:%s'%(
                    sen_id, root_node.label['form']))
                # Continue to find the id in next root node.
            else:
                state = state_node[0].label['form']
                logger.debug('state:%s'%str(state))
                
                # lemma here instead of form
                stative_verb_nodes = root_node.find_list(
                    'lemma', self.stative_verb_list) 
                    
                if not stative_verb_nodes:
                    logger.debug('no stative verb found in %d'%sen_id)
                else:
                    stative_verbs = [n.label['form'] for n in stative_verb_nodes]
                    stative_verb = ','.join(stative_verbs)
                    logger.debug('stative verbs:%s'%str(stative_verbs))
                    
                    # Change find to direct children
                    possesive_pronoun_nodes = state_node[0].find('deprel', 'poss')
                    # Not checking if actor is from state's subtree.
                    actor_nodes = root_node.find_list('form', self.actor_list.keys())
                    if not actor_nodes:
                        return None
                    actors = [n.label['form'] for n in actor_nodes]
                    actors_is_dc = []
                    for n1 in actor_nodes:
                        for n2 in stative_verb_nodes:
                            if n2.is_direct_parent(n1):
                                actors_is_dc.append('1')
                                break
                        else:
                            actors_is_dc.append('0')
                                
                    if not possesive_pronoun_nodes:
                        logger.debug('no possesive pronoun found in %d'%sen_id)
                        # find actor directly.
                        
                        
                    else:
                        possesive_pronoun = possesive_pronoun_nodes[0].label['form']
                        logger.debug('possesive pronoun found in %d: %d, first is %s'%(
                            sen_id,
                            len(possesive_pronoun_nodes),
                            possesive_pronoun))
                        
                        # find actor through corenlp.
                        actors = []
                        f = open(corenlp_filename, 'rb')
                        xml_string = f.read()
                        f.close()
                        doc = Document(xml_string)

                        possesive_pronoun_id = possesive_pronoun_nodes[0].label['id']
                        for coref in doc.coreferences:
                            isFound = False
                            _actor = None
                            for mention in coref.mentions:
                                _sen_id = mention.sentence.id
                                _w_id = mention.head.id
                                if sen_id == _sen_id and _w_id == possesive_pronoun_id:
                                    isFound = True
                                if not _actor and  mention.text in self.actor_list:
                                    _actor = self.actor_list[mention.text]

                            if isFound and _actor:
                                possesive_pronoun_reso = _actor
                                actors.append(_actor)
                    
                    # by default action verb is the root
                    action_verb = root_node.label['form']
                    
                    return (';'.join(actors), ';'.join(actors_is_dc),
                            action_verb, state, ';'.join(stative_verbs),
                            # possesive_pronoun, possesive_pronoun_reso
                            )


    def process_list(self, list_filename):
        '''
        :type filename: string
        :rtype list(tuple)
        '''
        
        if not os.path.isfile(list_filename):
            logger.error('%s file missing'%'filename')
            return
        
        with open(list_filename) as f:
            
            for line in f:
                filename, sen_id, w_id, word = tuple(line.strip().split(','))
                logger.info('processing '+filename)
                ret = self.process_sentence(filename, int(sen_id), int(w_id))
                if ret:
                    yield (filename,) + ret
        

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
        print(ans)
    
if __name__ == '__main__':
    main()