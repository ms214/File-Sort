import unittest
import pickle

from background import Background
from file import File

class TestSort(unittest.TestCase):

    def setUp(self):
        r_file = File()
        self.bg = Background(r_file.ruleData[0])

    def testCkChagne(self):
        self.assertFalse(self.bg.ckChange())

    def testBg_move(self):
        self.assertTrue(self.bg.bg_move())



if __name__ == '__main__':
    unittest.main()