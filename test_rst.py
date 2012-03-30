"""rst.py test suite."""

import unittest
import random
import itertools as it

import tempfile_util as tfu

import numpy as np

import rst

import static_files


test_file = static_files.static_file_func(__file__, 'test_data', 
                                          {'cpr' : 'cpr.rst',
                                           'expected_cpr_crds' : 'expected_cpr_crds.dat',
                                           'expected_cpr_comment': 'expected_cpr_comment.dat'})


class ReadCPRTestCase(unittest.TestCase):
    """Test reading a known mdrd file."""

    def test_read_comment(self):

        with open(test_file('expected_cpr_comment')) as f:
            expected_comment = f.next()[:-1]

        with rst.open(test_file('cpr')) as f:
            self.assertEqual(f.comment, expected_comment)


    def test_read_crd(self):
        with open(test_file('expected_cpr_crds')) as f:
            expected_crds = [float(x) for x in f.read().split()]

        with rst.open(test_file('cpr')) as f:
            crds = f.next()

        for (expected, crd) in it.izip_longest(expected_crds, crds):
            self.assertAlmostEqual(expected, crd, 3)


comment_chars=[' '] + [chr(x) for x in range(ord('a'), ord('z'))]

def random_comment(length=20, chars=comment_chars):
    """Generate a random nonsensical comment."""
    num_chars = len(chars)
    return ''.join(chars[random.randint(0, num_chars-1)] for count in xrange(length))

def random_crds(num_atoms, maxabs=20):
    """Generate a numpy array with random coordinates."""
    _rand = random.random

    crds = [2 * maxabs * (_rand() - 0.5) 
            for count in xrange(3 * num_atoms)]

    return np.array(crds)

class WriteReadTestCase(unittest.TestCase):
    """Test reading crds written by rst.py"""

    def test_read_comment(self):
        comment = random_comment()
        num_atoms = random.randint(1,100)
        crds = random_crds(num_atoms)

        with tfu.TempfileSession() as tfs:
            file_name = tfs.temp_file_name('.rst')

            with rst.open(file_name, 'w', comment=comment) as f:
                f.write(crds)

            with rst.open(file_name, 'r') as f:
                self.assertEqual(f.comment, comment)


    def test_read_crds(self):
        comment = random_comment()
        num_atoms = random.randint(1,100)

        num_crds = 1 # random.randint(1, 10)
        crdss = [random_crds(num_atoms) for count in xrange(num_crds)]

        with tfu.TempfileSession() as tfs:
            file_name = tfs.temp_file_name('.rst')

            with rst.open(file_name, 'w', comment=comment) as f:

                for crds in crdss:
                    f.write(crds)

            with rst.open(file_name, 'r') as f:
                for expected_crds, read_crds in it.izip_longest(crdss, f):
                    self.assertNotEqual(expected_crds, None)
                    self.assertNotEqual(read_crds, None)
                    for (expected, crd) in it.izip_longest(expected_crds, read_crds):
                        self.assertAlmostEqual(expected, crd, 3)



if __name__ == "__main__":
    unittest.main()

