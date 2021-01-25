import unittest
from grape_id import *

class GeneralTestCase(unittest.TestCase): # inherit from unittest.TestCase

    def test_is_partialMatchPhrase_true_working(self):
        self.assertTrue(partialMatchPhrase('sauvignon blanc blend',
          ['pinot grigio', 'sauvignon blanc', 'chardonnay']))

    def test_is_partialMatchPhrase_false_working(self):
        self.assertFalse(partialMatchPhrase('merlot blend', ['pinot grigio', 'sauvigon blanc', 'chardonnay']))

    def test_is_findColors_singleResult_working(self):
        colors = findColors('Vigorosa Rosato'.lower())
        self.assertEqual(colors, ['Rosé', 'Rosé', 'Rosé', 'Rosé', 'Rosé'])

    def test_is_findColors_multiResult_working(self):
        colors = findColors('Blanc de Noirs, white Champagne only from red grapes, produces wines with some weight, as here. It makes for a rich, full-blooded Champagne, packed with red fruits while also cut through with intense acidity.'.lower())
        self.assertEqual(colors, ['White', 'White', 'White', 'White', 'White', 'Red'])

    def test_is_findColors_noResult_working(self):
        colors = findColors('Earthy aromas mingle with mandarin peel on the nose. Reddish in color.'.lower())
        self.assertEqual(colors, [])

    def test_is_findPrefix_working(self):
        prefix = findPrefix('This wine hits your nose with a touch of bubbles.'.lower())
        self.assertEqual(prefix, 'Sparkling')

    def test_is_findPrefix_noResult_working(self):
        prefix = findPrefix('Earthy aromas mingle with mandarin peel on the nose. Reddish in color.'.lower())
        self.assertIsNone(prefix)

    def test_is_findSuffix_working(self):
        suffix = findSuffix('This red blend is the perfect example of full-bodied.'.lower())
        self.assertEqual(suffix, 'Blend')

    def test_is_findSuffix_noResult_working(self):
        suffix = findSuffix('Earthy aromas mingle with mandarin peel on the nose. Reddish in color.'.lower())
        self.assertIsNone(suffix)

    def is_chooseMostCommon_singleResult_working(self):
        searchList = ['Red', 'White', 'Red']
        (top, searchList) = chooseMostCommon(searchList)
        self.assertEqual(top, 'Red')

    def is_chooseMostCommon_tiedResult_working(self):
        searchList = ['Red', 'Red', 'White', 'White', 'Pink']
        (top, searchList) = chooseMostCommon(searchList)
        self.assertIsNone(top)

    def is_chooseMostCommon_tieBrokenResult_working(self):
        searchList = ['Red', 'Red', 'White', 'White', 'Pink']
        (top, searchList) = chooseMostCommon(searchList)
        self.assertEqual(top, 'Red')


    def is_chooseMostCommon_noResult_working(self):
        searchList = ['Red', 'Blue', 'White', 'Green', 'Pink']
        (top, searchList) = chooseMostCommon(searchList)
        self.assertIsNone(top)

if __name__ == '__main__':
    unittest.main()
