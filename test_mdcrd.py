"""mdcrd.py test suite."""

import unittest
import random
import itertools as it

import tempfile_util as tfu

import numpy as np

import mdcrd

import static_files


test_file = static_files.static_file_func(__file__, 'test_data', 
                                          {'ala' : 'ala.crd',
                                           'expected_ala_crds' : 'expected_ala_crds.dat',
                                           'expected_ala_comment': 'expected_ala_comment.dat'})


class ReadAlaTestCase(unittest.TestCase):
    """Test reading a known mdrd file."""

    def test_read_comment(self):

        with open(test_file('expected_ala_comment')) as f:
            expected_comment = f.next()

        with mdcrd.open(test_file('ala'), num_atoms=22) as f:
            self.assertEqual(f.comment, expected_comment)


    def test_read_crd(self):
        with open(test_file('expected_ala_crds')) as f:
            expected_crds = [float(x) for x in f.read().split()]

        with mdcrd.open(test_file('ala'), num_atoms=22) as f:
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
    """Test reading crds written by mdcrd.py"""

    def test_read_comment(self):
        comment = random_comment()
        num_atoms = random.randint(1,100)
        crds = random_crds(num_atoms)

        with tfu.TempfileSession() as tfs:
            file_name = tfs.temp_file_name('.crd')

            with mdcrd.open(file_name, 'w', num_atoms=num_atoms,
                            comment=comment) as f:
                f.write(crds)

            with mdcrd.open(file_name, 'r', num_atoms=num_atoms) as f:
                self.assertEqual(f.comment, comment)


    def test_read_crds(self):
        comment = random_comment()
        num_atoms = random.randint(1,100)

        num_crds = random.randint(1, 10)
        crdss = [random_crds(num_atoms) for count in xrange(num_crds)]

        with tfu.TempfileSession() as tfs:
            file_name = tfs.temp_file_name('.crd')

            with mdcrd.open(file_name, 'w', num_atoms=num_atoms,
                            comment=comment) as f:

                for crds in crdss:
                    f.write(crds)

            with mdcrd.open(file_name, 'r', num_atoms=num_atoms) as f:
                for expected_crds, read_crds in it.izip_longest(crdss, f):
                    self.assertNotEqual(expected_crds, None)
                    self.assertNotEqual(read_crds, None)
                    for (expected, crd) in it.izip_longest(expected_crds, read_crds):
                        self.assertAlmostEqual(expected, crd, 3)



if __name__ == "__main__":
    unittest.main()

