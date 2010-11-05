import unittest
import os
from svgsize import get_SVG_file_size

class TestSVGSize(unittest.TestCase):
    def _check(self, filename, x, y):
        filename = os.path.join(os.path.dirname(__file__), 
            'testdata', filename)
        fx, fy = get_SVG_file_size(filename)
        self.failUnlessEqual(fx, x)
        self.failUnlessEqual(fy, y)

    def test_file_size(self):
        self._check('01-one-red-triangle.svg', 400, 400)
        self._check('padlock.svg', 128, 128)

def test_suite():
    return unittest.makeSuite(TestSVGSize)
