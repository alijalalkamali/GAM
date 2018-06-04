'''
Unit tests for tree_util.py.

'''

import unittest
import tree_util

class TreeUtilTest(unittest.TestCase):
	def setUp(self):
		self.root = tree_util.Node({'id':0, 'form':'improve'}, [])
		self.root.add_child(tree_util.Node({'id':1, 'form':'economy'}))
		self.root.add_child(tree_util.Node({'id':2, 'form':'to'}))
	
	def test_find(self):
		testcases = [('id', 2), ('form', 'economy'), ('pos', 1), ('form', 'one')]
		self.assertEqual(self.root.find('id', 2)[0].label['id'], 2)
		self.assertEqual(self.root.find('form', 'economy')[0].label['form'], 'economy')
		self.assertEqual(len(self.root.find('pos', 1)), 0)
		self.assertEqual(len(self.root.find('form', 'one')), 0)

if __name__ == '__main__':
	unittest.main()