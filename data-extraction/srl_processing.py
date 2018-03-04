'''
Basic implementation of SRL processing tasks discussed on Feb 16.
'''

import tree_builder as tb
import coref_resolution as cr
import os.path

def file_loader(filename, col=0):
    '''
    Read certain coloumn from text file.
    '''
    with open(filename) as fp:
        ret = fp.readlines()
        ret = [line.split()[col] for line in ret]
        return ret
    return None

base_forms = []
stative_verb_list = []
actor_list = []

base_forms = file_loader('params/states.txt')
stative_verb_list = file_loader('params/stativewords.txt')
actor_list = file_loader('params/countr_map.txt')

def process_file(filename):
    srl_filename = '%s.txt.srl'%filename
    coref_filename = '%s.xml'%filename
    
    if not os.path.isfile(srl_filename) or not os.path.isfile(coref_filename):
        print('%s file missing'%'filename')
        return
    
    t = tb.TreeBuilder()
    c = cr.CorefResoluter()
    
    # process single file
    
    t.filename = srl_filename
    c.load_file(coref_filename)
    
    sentence_count = 1
    for p in t.get_sentence_from_file():
        # process single sentence
        
        root_nodes = t.build_tree(p)
        for root_node in root_nodes:
            state_nodes = root_node.find_list('lemma', base_forms)
            # import pdb; pdb.set_trace()
            if not state_nodes:
                print('no state found in sentence:%d root:%s'%(
                    sentence_count, root_node.label['form']))
            else:
                # import pdb; pdb.set_trace()
                states = [n.label['form'] for n in state_nodes]
                print('states:%s'%str(states))
                
                # lemma here instead of form
                stative_verb_nodes = root_node.find_list('lemma', stative_verb_list) 
                # import pdb; pdb.set_trace()
                if not stative_verb_nodes:
                    print('no stative verb found in %d'%sentence_count)
                else:
                    stative_verbs = [n.label['form'] for n in stative_verb_nodes]
                    print('stative verbs:%s'%str(stative_verbs))
                    
                    possesive_pronoun_node = stative_verb_nodes[0].find('deprel', 'poss')
                    actor_nodes = root_node.find_list('form', actor_list)
                    actors = [n.label['form'] for n in actor_nodes]
                    if not possesive_pronoun_node:
                        print('no possesive pronoun found in %d'%sentence_count)
                        # find actor directly.
                        
                        
                    else:
                        # find actor through corenlp.
                        pass
                    
                    # return actor, state, stative verb
                    return (actors, states, stative_verbs)
        sentence_count += 1

def main():
    print(process_file('data/test'))
    # for i in range(1, 2):
    #     process_file('data/newsText%d'%i)

if __name__ == '__main__':
    main()