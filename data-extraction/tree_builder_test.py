'''
Unit tests for tree_builder.py.

'''

import unittest
import tree_builder

class TreeBuilderTest(unittest.TestCase):
	
	def test_get_paragraph_from_file(self):
		t = tree_builder.TreeBuilder()
		t.filename = 'newsText1.txt.srl'
		self.assertEqual(t.get_paragraph_from_file(), 5)
		
	def test_build_tree(self):
		t = tree_builder.TreeBuilder()
		t.filename = 'newsText1.txt.srl'
		l = list(t.get_paragraph_from_file())
		

if __name__ == '__main__':
	unittest.main()