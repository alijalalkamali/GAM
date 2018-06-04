'''
Reform the tree structure in ClearNLP.

'''

import tree_util


class Config:
    '''
    Configuration of the inputs.
    
    Enables batch inputs from files here.
    '''
    pass

    
class TreeBuilder:
    def __init__(self):
        self.config = ''
        self.filename = '' # Current file
        self.sentence_index = 0 # Current sentence
    
    def set_config(self, config):
        pass    
    
    def get_lines(self):
        pass

    def get_sentence(self):
        '''
        Generate SRL labels of a sentence.
        The paragraph is located by self.filename and self.paragraph_index.
        '''
        if self.config == 'file':
            pass
                    
    def get_sentence_from_file(self, filename):
        '''
        Generate each sentence as a list of lines.
        '''
        with open(filename) as f:
            count = 0
            buf = []
            for _, line in enumerate(f):
                if '\t' not in line:
                    count += 1
                    yield buf
                    buf = []
                else:
                    buf.append(line)
            if buf:
                yield buf
                
    def get_ith_sentence_from_file(self, filename, i):
        '''
        Generate ith sentence as a list of lines.
        '''
        cnt = 1 # sentence count starts from 1
        for sen in self.get_sentence_from_file(filename):
            if cnt == i:
                return sen
            cnt += 1
        # Exception handling, index out of bound.
        return []
    
    def build_tree(self, sentence, sem = False):
        '''
        Build tree from the current get_lines().
        
        Returns:
            Root node of the new tree. tree_util.Node
        '''
        # Create nodes and index.
        _dict = {}
        for line in sentence:
            fields = line.split('\t')
            if len(fields) <2:
                continue
            _label = {
                'id':int(fields[0]),
                'form':fields[1],
                'lemma':fields[2],
                'pos':fields[3],
                'feats':fields[4],
                'head':int(fields[5]),
                'deprel':fields[6],
                'sheads':fields[7],
            }
            _dict[int(fields[0])] = tree_util.Node(label=_label, children=[])
        
        # Connect nodes.
        root_nodes = []
        for _, n in _dict.items():
            if sem:
                if n.label['sheads'] == '_\n':
                    root_nodes.append(n)
                else:
                    for part in n.label['sheads'].split(';'):
                        parent, sem_relation = part.split(':')
                        _dict[int(parent)].add_child(n, sem_relation)
            else:
                if n.label['head'] != 0:
                    _dict[n.label['head']].add_child(n)
                else:
                    root_nodes.append(n)
        
        return root_nodes
        
    
    # def build_from_config(self):
    #     '''
    #     A interface for building all files and paragraphs from config.
    #     '''
        
    #     if self.config.source == 'file':
    #         for i in range(len(self.config.filenames)):
    #             pass