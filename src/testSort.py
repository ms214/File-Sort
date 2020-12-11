import unittest

from sort import Sort

class TestSort(unittest.TestCase):

    def setUp(self):
        self.s1 = Sort()

    def testOpenFile(self):
        self.assertTrue(self.s1.openFile())

    def testMove(self):
        self.s1.ckfile()
        self.assertTrue(self.s1.move())



if __name__ == '__main__':
    unittest.main()