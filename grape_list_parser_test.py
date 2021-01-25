import unittest
from grape_list_parser import *

class GeneralTestCase(unittest.TestCase): # inherit from unittest.TestCase

    def test_is_splitNames_by_comma_working(self):
        names = 'Adakarasi, Adakarassy, Avsa adasi, Avsa island, Balikesir, Erdek, Noir des iles'
        nameLst = splitNames(names)
        self.assertEqual(nameLst, ['Adakarasi', 'Adakarassy', 'Avsa adasi', 'Avsa island', 'Balikesir', 'Erdek', 'Noir des iles'])

    def test_is_splitNames_by_forwardslash_working(self):
        names = 'Douce noir/Charbono/Bonarda/Turca'
        nameLst = splitNames(names)
        self.assertEqual(nameLst, ['Douce noir', 'Charbono', 'Bonarda', 'Turca'])

    def test_is_removeComments_parenthesis_working(self):
        name = 'Arbanne (in Les Riceys and Moulins-en-Tonnerrois)'
        nameMod = removeComments(name)
        self.assertEqual(nameMod, 'Arbanne')

    def test_is_removeComments_brackets_working(self):
        name = 'Elmer Swenson[3]'
        nameMod = removeComments(name)
        self.assertEqual(nameMod, 'Elmer Swenson')

if __name__ == '__main__':
    unittest.main()
