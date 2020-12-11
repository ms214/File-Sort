import unittest

from file import File

class TestSort(unittest.TestCase):

    def setUp(self):
        self.s1 = File()

    def testWriteGeneralRule(self):
        self.s1.writeGeneralRule('C:/Users/minso/Downloads', False)
        self.assertEqual(self.s1.ruleData, ['C:/Users/minso/Downloads', False])

    def testGetGeneralRule(self):
        self.assertEqual(self.s1.getGeneralRule(), self.s1.ruleData)


if __name__ == '__main__':
    unittest.main()