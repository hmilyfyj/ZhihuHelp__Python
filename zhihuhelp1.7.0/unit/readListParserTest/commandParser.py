# -*- coding: utf-8 -*-
__author__ = 'zentao'

import sys
# 添加库路径
currentPath = sys.path[0]
currentPath = currentPath.replace('unit\\readListParserTest', '')
print currentPath
sys.path.append(currentPath)

from codes.baseClass import *
from codes.readListParser import *

import unittest

"""
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
"""
f = open('./ReadList.txt')
parser = ReadListParser()
for line in f:
    result = parser.parseCommandLine(line)
    BaseClass.printDict(result)
