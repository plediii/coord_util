"""gro.py test suite."""

import unittest
import itertools as it

import numpy as np

import gro

import static_files


test_file = static_files.static_file_func(__file__, 'test_data', 
                                          {'water' : 'water.gro',
                                           'expected_water_crds' : 'expected_water_crds.dat',
                                           'expected_water_comment': 'expected_water_comment.dat',
                                           'sh3' : 'sh3.gro',
                                           'expected_sh3_crds' : 'expected_sh3_crds.dat',
                                           'expected_sh3_comment': 'expected_sh3_comment.dat'})


class ReadCase(object):
    """Test reading a known mdrd file."""

    decimals=3

    def test_read_comment(self):

        with open(self.expected_comment_file) as f:
            expected_comment = f.next()

        with gro.open(self.test_file_name, decimals=self.decimals) as f:
            f.next()            # read a geometry to get its comment
            self.assertEqual(f.comment, expected_comment)


    def test_read_crd(self):
        with open(self.expected_crds_file) as f:
            expected_crds = 10. * np.array([float(x) for x in f.read().split()])

        with gro.open(self.test_file_name, decimals=self.decimals) as f:
            crds = f.next()

        for (expected, crd) in it.izip_longest(expected_crds, crds):
            self.assertAlmostEqual(expected, crd, self.decimals)

class ReadWaterTestCase(ReadCase, unittest.TestCase):
    test_file_name=test_file('water')
    expected_comment_file=test_file('expected_water_comment')
    expected_crds_file=test_file('expected_water_crds')


class ReadSH3TestCase(ReadCase, unittest.TestCase):
    test_file_name=test_file('sh3')
    expected_comment_file=test_file('expected_sh3_comment')
    expected_crds_file=test_file('expected_sh3_crds')



if __name__ == "__main__":
    unittest.main()

