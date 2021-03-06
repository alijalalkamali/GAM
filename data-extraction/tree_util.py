'''
Tree data representation and tree operations for SRL data processing.

Operations includes:

1. search node

author: JL <linjiach@usc.edu>
'''

class Node(object):
    def __init__(self, label, children=[]):
        '''
        The semantic role labeling format requires 8 fields.
        ID: current token ID (starting at 1).
        FORM: word form.
        LEMMA: lemma.
        POS: part-of-speech tag.
        FEATS: features (different features are delimited by '|', keys and values are delimited by '=', and '_' indicates no feature).
        HEAD: head token ID.
        DEPREL: dependency label.
        SHEADS: semantic heads ('_' indicates no semantic head).
        '''
        self.label = label # A dictionary containing 8 fields (optional)
        self.children = children
        self.parent = None
        self.sem_relation = None
        
    def __str__(self):
        return '%s:%s'%(str(self.label['id']), self.label['form'])
        
    def __eq__(self, n):
        return self.label['id'] == n.label['id']
        
    def add_child(self, child, sem_relation = None):
        '''
        Adding a child to the current node.
        '''
        self.children.append(child)
        child.parent = self
        child.sem_relation = sem_relation
        
    def find(self, field, value):
        '''
        Find the nodes that have certain field's value equal to given 
        value.
        '''
        ret = []
        if self.label.get(field) == value:
            ret.append(self)
        for child in self.children:
            ret+=child.find(field, value)
        return ret
        
    def find_list(self, field, value_list):
        '''
        Find the nodes that have certain field's value equal to one of
        the given values.
        '''
        ret = []
        if self.label.get(field) in value_list:
            ret.append(self)
        for child in self.children:
            ret+=child.find_list(field, value_list)
        return ret
        
    def rev_find_list(self, field, value_list):
        '''
        Find the nodes from bottom to top
        (TODO: fix inconsistent return type with find_list.)
        '''
        if not self.parent:
            return None
        if self.parent.label.get(field) in value_list:
            return self.parent
        else:
            return self.parent.rev_find_list(field, value_list)
            
    def is_direct_parent(self, node):
        for child in self.children:
            if child == self:
                return True
        return False
        
    def is_parent(self, node):
        if not node.parent:
            return False
        if node.parent == self:
            return True
        return self.is_parent(node.parent)


# def search_lemmas(node, lemmas):
#     '''
#     Args:
#         node: The root node for searching. Node
#         lemmas: All the target lemmas. List of string
        
#     Returns:
#         All sub nodes that has one of the given lemmas.
#     '''
#     pass