"""geometry.py test suite."""

import unittest
import random
import math
import numpy as np
import copy

import coord_math as cm


num_test=100                    # Number of random tests to do

def randomize_mol(mol):
    """Randomly move a molecule around."""
    translation_vector = np.array([random.random() * 10.0 + 5.0 for i in xrange(3)])
    (rot_alpha, rot_beta, rot_gamma) = [random.random() * 2 * math.pi for i in xrange(3)]
    return cm.translate(cm.rotate_euler(mol, rot_alpha, rot_beta, rot_gamma), translation_vector)

methane = np.array([0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0,
                    0.0, 0.0, 1.0,
                    1.0, 0.0, 0.0])

def perturb(mol, delta=10.0, min=1.0):
    """Change the coordinates of the atoms in a random way."""
    perturbed_coords = mol.copy()
    for idx in xrange(len(perturbed_coords)):
        perturbed_coords[idx] = perturbed_coords[idx] + min + delta * random.random()
    return perturbed_coords

def invert_z(mol):
    """Negate the z coordinate for each atom."""
    inverted_coords = mol.copy().reshape((-1, 3))
    for idx in xrange(len(inverted_coords)):
        inverted_coords[idx][2] = -inverted_coords[idx][2]
    return inverted_coords.reshape((-1,))

def methane_sample():
    """Return a methane molecule."""
    global methane
    return randomize_mol(methane)

tolerance = 1e-7

class CheckCOM(unittest.TestCase):
    
    def test_com_methane(self):
        """The center of mass for methane should be as expected."""
        global tolerance, methane
        expected_com = np.array([0.25] * 3)
        com = cm.center_of_geometry(methane)
        diff = expected_com - com
        assert np.linalg.norm(diff) < tolerance, "com is wrong: \ncom = \n%s, \nexpected = \n%s." % (com, expected_com)
        
class CheckRMSD(object):

    def test_positive_rmsd(self):
        """The rmsd between a molecule and itself should be semi-positive."""
        global num_test
        for idx in xrange(num_test):
            rmsd = self.rmsd(methane_sample(), methane_sample())
            assert rmsd >= 0.0, " rmsd is negative: %s" % rmsd

    def test_zero_rmsd(self):
        """The rmsd between a molecule and itself should be zero."""
        global tolerance, num_test
        for idx in xrange(num_test):
            some_methane = methane_sample()
            rmsd = self.rmsd(some_methane, some_methane)
            assert rmsd  <= tolerance, "rmsd is too large.  rmsd = %s" % rmsd

    def test_general_rmsd(self):
        """RMSD should have the general property that the rmsd between a molecule and random translations/rotations of itself is nearly zero."""
        global tolerance, num_test
        for idx in xrange(num_test):
            rmsd = self.rmsd(methane_sample(), methane_sample())
            assert rmsd  <= tolerance, "rmsd is too large.  rmsd = %s; idx = %s" % (rmsd, idx)
    
    def test_swapped_atom(self):
        """The rmsd should be bigger if I swap the positions of two atoms."""
        global tolerance, num_test
        for idx in xrange(num_test):
            unswapped_methane = methane_sample()
            methane_coords = copy.deepcopy(unswapped_methane)
            (methane_coords[1], methane_coords[2]) = (methane_coords[2], methane_coords[1])
            rmsd = self.rmsd(unswapped_methane, methane_coords)
            # this is a generous underestimate of how much the rmsd should change.
            assert  rmsd > tolerance, "rmsd did not become larger as expected. rmsd = %s" % rmsd
            
    def test_perturb_atoms(self):
        """The rmsd should be bigger if I randomly perturb its coordinates."""
        global num_test
        for idx in xrange(num_test):
            unperturbed_methane = methane_sample()
            perturbed_methane = perturb(unperturbed_methane, 10.0)
            rmsd = self.rmsd(unperturbed_methane, perturbed_methane)
            # this is a generous underestimate of how much the rmsd should change.
            assert  rmsd > 1.0, "rmsd did not become large as expected. rmsd = %s" % rmsd

    def test_rmsd_invariant(self):
        """The rmsd measure should be invariant under random translations and rotations."""
        global tolerance, num_test
        for idx in xrange(num_test):
            unperturbed_methane = methane_sample()
            perturbed_methane = perturb(unperturbed_methane, 10.0)
            before = self.rmsd(unperturbed_methane, perturbed_methane)
            after = self.rmsd(unperturbed_methane, randomize_mol(perturbed_methane))
            assert  abs(before - after) < tolerance, "randomizing mol changed the rmsd: before = %s, after = %s; idx = %s" % (before, after, idx)
        
    def test_distinguish_inversion(self):
        """Inverting a coordinate should not be a possible orthogonal transformation."""
        global tolerance, num_test
        for idx in xrange(num_test):
            some_methane = methane_sample()
            inverted_methane = invert_z(some_methane)
            rmsd = self.rmsd(some_methane, inverted_methane)
            assert  rmsd > tolerance, "rmsd too low for inverted coordinate. rmsd = %s" % rmsd

    def test_known_rmsd(self):
        """RMSD for a specific case should evaluate as I expect."""
        global tolerance, num_test
        for idx in xrange(num_test):
            first_mol = randomize_mol(np.array([0.0, 0.0, -1.0, 0.0, 0.0, 1.0]))

            second_mol = randomize_mol(np.array([0.0, 0.0, -2.0, 0.0, 0.0, 3.0]))

            rmsd = self.rmsd(first_mol, second_mol)
            expected = 1.5
            assert abs(rmsd - expected) < tolerance, "rmsd was not as expected: %s != %s" % (rmsd, 1.0)

    def test_translated(self):
        """Translating a molecule should not affect its rmsd."""
        global tolerance, num_test
        for idx in xrange(num_test):
            translation_vector = [random.random() * 10.0 + 5.0 for i in xrange(3)]
            some_methane = methane_sample()
            before = self.rmsd(some_methane, some_methane)
            after = self.rmsd(some_methane, cm.translate(some_methane, translation_vector))
            assert abs(before - after) < tolerance, "translating the molecule affected its rmsd. before = %s, rmsd = %s, idx = %s" % (before, after, idx)

    def test_known_translated(self):
        """RMSD for a specific case should evaluate as I expect."""
        global tolerance, num_test
        for idx in xrange(num_test):
            first_mol = randomize_mol(np.array([0.0, 0.0, -1.0, 0.0, 0.0, 1.0]))

            second_mol = randomize_mol(np.array([0.0, 0.0, -2.0, 0.0, 0.0, 3.0]))

            translation_vector = np.array([random.random() * 10.0 + 5.0 for i in xrange(3)])

            rmsd = self.rmsd(first_mol, cm.translate(second_mol, translation_vector))
            expected = 1.5
            assert abs(rmsd - expected) < tolerance, "rmsd was not as expected: %s != %s" % (rmsd, 1.0)


    def test_rotated(self):
        """Rotating a molecule around the first euler angle should not affect its rmsd."""
        global tolerance, num_test
        for idx in xrange(num_test):
            some_methane = methane_sample()
            before = self.rmsd(some_methane, some_methane)
            after = self.rmsd(some_methane, cm.rotate_euler(some_methane, random.random() * math.pi, random.random() * math.pi, random.random() * math.pi))
            assert abs(before - after) <= tolerance, "rotating the molecule affected its rmsd. before = %s, rmsd = %s, idx = %s" % (before, after, idx)

    def test_known_rotated(self):
        """RMSD for a specific case should evaluate as I expect."""
        global tolerance, num_test
        for idx in xrange(num_test):
            first_mol = randomize_mol(np.array([0.0, 0.0, -1.0, 0.0, 0.0, 1.0]))

            second_mol = randomize_mol(np.array([0.0, 0.0, -2.0, 0.0, 0.0, 3.0]))

            # translation_vector = np.array([random.random() * 10.0 + 5.0 for i in xrange(3)])

            rmsd = self.rmsd(first_mol, cm.rotate_euler(second_mol, random.random() * math.pi, random.random() * math.pi, random.random() * math.pi))
            expected = 1.5
            assert abs(rmsd - expected) < tolerance, "rmsd was not as expected: %s != %s" % (rmsd, 1.0)

    


class CheckRMSD_rmsd(CheckRMSD, unittest.TestCase):
    """Check just the rmsd rotation function."""

    rmsd = staticmethod(cm.rmsd)

class CheckRMSD_rmsd_rotation(CheckRMSD, unittest.TestCase):
    """Exercise each of the separate components of RMSD. """

    
    def rmsd(self, x, y):
        x = cm.translate(x, -cm.center_of_geometry(x))
        y = cm.translate(y, -cm.center_of_geometry(y))
        rot = cm.rmsd_rotation(x, y)
        y = cm.transform(y, rot)
        return cm.flat_rmsd(x, y)


class TestEulerRotation(unittest.TestCase):
    
    def test_rotation_orthogonal(self):
        eye = np.eye(3)
        for count in xrange(100):
            (rot_alpha, rot_beta, rot_gamma) = [random.random() * 2 * math.pi for i in xrange(3)]
            matrix = cm.euler_rotation_matrix(rot_alpha, rot_beta, rot_gamma)
            product = np.dot(matrix, matrix.transpose())
            delta = np.abs(product - eye)
            self.assertTrue(delta.max() < 1e-5)

    def test_flip_alpha(self):
        flip = np.eye(3)
        flip[0, 0] = -1
        flip[1,1] = -1
        rot_alpha, rot_beta, rot_gamma = math.pi, 0., 0.
        matrix = cm.euler_rotation_matrix(rot_alpha, rot_beta, rot_gamma)
        delta = np.abs(matrix - flip)
        self.assertTrue(delta.max() < 1e-5, "%s !=\n %s" % (matrix, flip))

    def test_flip_beta(self):
        flip = np.eye(3)
        flip[1,1] = -1
        flip[2,2] = -1
        rot_alpha, rot_beta, rot_gamma = 0., math.pi, 0.
        matrix = cm.euler_rotation_matrix(rot_alpha, rot_beta, rot_gamma)
        delta = np.abs(matrix - flip)
        self.assertTrue(delta.max() < 1e-5, "%s !=\n %s" % (matrix, flip))


    def test_flip_gamma(self):
        flip = np.eye(3)
        flip[0,0] = -1
        flip[1,1] = -1
        rot_alpha, rot_beta, rot_gamma = 0., 0., math.pi
        matrix = cm.euler_rotation_matrix(rot_alpha, rot_beta, rot_gamma)
        delta = np.abs(matrix - flip)
        self.assertTrue(delta.max() < 1e-5, "%s !=\n %s" % (matrix, flip))

    def test_quarter_rotate_alpha(self):
        flip = np.array([[0., -1., 0.],
                         [1., 0., 0.],
                         [0., 0., 1.]])
        rot_alpha, rot_beta, rot_gamma = math.pi/2., 0., 0.
        matrix = cm.euler_rotation_matrix(rot_alpha, rot_beta, rot_gamma)
        delta = np.abs(matrix - flip)
        self.assertTrue(delta.max() < 1e-5, "%s !=\n %s" % (matrix, flip))

    def test_quarter_rotate_gamma(self):
        flip = np.array([[0., -1., 0.],
                         [1., 0., 0.],
                         [0., 0., 1.]])
        rot_alpha, rot_beta, rot_gamma = 0., 0., math.pi/2.
        matrix = cm.euler_rotation_matrix(rot_alpha, rot_beta, rot_gamma)
        delta = np.abs(matrix - flip)
        self.assertTrue(delta.max() < 1e-5, "%s !=\n %s" % (matrix, flip))


    def test_quarter_rotate_beta_alpha(self):
        flip = np.array([[0., 0., 1.],
                         [1., 0., 0.],
                         [0., 1., 0.]])
        rot_alpha, rot_beta, rot_gamma = math.pi/2., math.pi/2, 0.
        matrix = cm.euler_rotation_matrix(rot_alpha, rot_beta, rot_gamma)
        delta = np.abs(matrix - flip)
        self.assertTrue(delta.max() < 1e-5, "%s !=\n %s" % (matrix, flip))


    def test_quarter_rotate_beta_gamma(self):
        flip = np.array([[0., -1., 0.],
                         [0., 0., -1.],
                         [1., 0., 0.]])
        rot_alpha, rot_beta, rot_gamma = 0., math.pi/2., math.pi/2
        matrix = cm.euler_rotation_matrix(rot_alpha, rot_beta, rot_gamma)
        delta = np.abs(matrix - flip)
        self.assertTrue(delta.max() < 1e-5, "%s !=\n %s" % (matrix, flip))

        

class TestAtomDist(unittest.TestCase):
    

    def test_atom_dist(self):
        for count in range(100):
            d1 = random.random() * 10.
            d2 = random.random() * 10.
            d3 = random.random() * 10.

            mol = np.array([0.0, 0.0, 0.0,
                            0.0, d1, 0.0,
                            0.0, 0.0, d2,
                            d3, 0.0, 0.0])
            mol = randomize_mol(mol)

            tol = 1e-5

            def test_distance(mol, idx, jdx, d):
                dist = cm.atom_dist(mol, idx, jdx)
                self.assertTrue(abs(dist - d) < tol, "distance %d to %d was incorrect: %s != %s" % (idx, jdx, dist, d))

            for jdx, d in enumerate([d1, d2, d3], 2):
                test_distance(mol, 1, jdx, d)

            test_distance(mol, 0, 0, 0.)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(CheckRMSD('test_general_rmsd'))
    suite.addTest(CheckRMSD('test_distinguish_inversion'))
    return suite
    
if __name__ == "__main__":
#     suite = suite()
#     suite.debug()
    unittest.main()
