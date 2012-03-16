"""topology.py test suite."""

import unittest

import numpy as np

import topology as t

class AtomOffsetInvariantTestCase(unittest.TestCase):

    def test_molecule(self):
        top = t.Molecule('water', ['H', 'O', 'H'])


        for idx in range(top.num_atoms):
            self.assertEqual(top.offsets_by_atom[idx].shape, (3,))


        offsets = top.atom_offsets
        reshaped = top.offsets_by_atom.reshape(len(offsets))

        self.assertEqual(list(reshaped), list(offsets))


    def test_polymer(self):
        ala = t.Molecule('ALA', ['N', 'CA', 'CB', 'C', 'O'])

        gly = t.Molecule('GLY', ['N', 'CA', 'C', 'O'])

        class Polymer(t.Polymer):
            monomers = ['ALA', 'GLY']

        top = t.Polymer('polymer', [ala, gly])


        for idx in range(top.num_atoms):
            self.assertEqual(top.offsets_by_atom[idx].shape, (3,))


        offsets = top.atom_offsets
        reshaped = top.offsets_by_atom.reshape(len(offsets))

        self.assertEqual(list(reshaped), list(offsets))



class MoleculeAtomTestCase(unittest.TestCase):

    ndof = 3

    def test_num_atoms(self):
        top = t.Molecule('water', ['H', 'O', 'H'], ndof=self.ndof)

        self.assertEqual(top.num_atoms, 3)

    def test_default_offsets(self):
        top = t.Molecule('water', ['H', 'O', 'H'], ndof=self.ndof)

        self.assertEqual(list(top.atom_offsets), range(3 * self.ndof))

    def test_get_atoms(self):
        top = t.Molecule('water', ['H', 'O', 'H'], ndof=self.ndof)

        h_atoms = top.get_atoms('H')
        o_atoms = top.get_atoms('O')

        self.assertEqual(len(h_atoms), 2)
        self.assertEqual(len(o_atoms), 1)

    def test_get_atom_coords(self):
        top = t.Molecule('water', ['H', 'O', 'H'], ndof=self.ndof)

        h_atoms = top.get_atoms('H')
        o_atoms = top.get_atoms('O')


        x = np.array(range(self.ndof * top.num_atoms))

        h_x = h_atoms.get_coords(x)
        o_x = o_atoms.get_coords(x)

        expected_h_x = np.array(range(0 * self.ndof, 1 * self.ndof) + range(2 * self.ndof, 3 * self.ndof))
        expected_o_x = np.array(range(1 * self.ndof, 2 * self.ndof))

        self.assertEqual(list(expected_h_x), list(h_x))
        self.assertEqual(list(expected_o_x), list(o_x))


    def test_set_atom_coords(self):

        top = t.Molecule('water', ['H', 'O', 'H'], ndof=self.ndof)

        h_atoms = top.get_atoms('H')
        o_atoms = top.get_atoms('O')


        x = np.array(range(self.ndof * top.num_atoms))

        # Set the coordinates to something crazy
        expected_h_x = np.array(range(9 * self.ndof, 11 * self.ndof))
        expected_o_x = np.array(range(9 * self.ndof, 10 * self.ndof))

        h_atoms.set_coords(x, expected_h_x)
        o_atoms.set_coords(x, expected_o_x)

        h_x = h_atoms.get_coords(x)
        o_x = o_atoms.get_coords(x)

        self.assertEqual(list(expected_h_x), list(h_x))
        self.assertEqual(list(expected_o_x), list(o_x))


class MoleculeAtom1DTestCase(MoleculeAtomTestCase):

    ndof = 1



class PolymerAtomTestCase(unittest.TestCase):

    def make_top(self):
        ala = t.Molecule('ALA', ['N', 'CA', 'CB', 'C', 'O'])
        gly = t.Molecule('GLY', ['N', 'CA', 'C', 'O'])
        return t.Polymer('poly', [ala, gly])        


    def test_num_atoms(self):
        top = self.make_top()

        self.assertEqual(top.num_atoms, 9)
    
    def test_get_atom_num_atoms(self):
        top = self.make_top()

        ca_atoms = top.get_atoms('C')
        cb_atoms = top.get_atoms('CB')

        self.assertEqual(len(ca_atoms), 2)
        self.assertEqual(len(cb_atoms), 1)

    def test_get_atom_num_monomers(self):
        top = self.make_top()

        ca_atoms = top.get_atoms('C')
        cb_atoms = top.get_atoms('CB')

        self.assertEqual(ca_atoms.num_monomers, 2)
        self.assertEqual(cb_atoms.num_monomers, 2)


    def test_get_atom_coords(self):
        top = self.make_top()

        c_atoms = top.get_atoms('C')
        cb_atoms = top.get_atoms('CB')

        x = np.array(range(3 * top.num_atoms))

        c_x = c_atoms.get_coords(x)
        cb_x = cb_atoms.get_coords(x)

        expected_c_x = np.array(range(3 * 3, 3 * 4) + range(3 * 5 + 3 * 2, 3 * 5 + 3*3))
        expected_cb_x = np.array(range(3 * 2, 3 * 3))

        self.assertEqual(list(c_x), list(expected_c_x))
        self.assertEqual(list(cb_x), list(expected_cb_x))


    def test_get_regex_atom_coords(self):
        top = self.make_top()

        c_atoms = top.regex_get_atoms('^C$')
        no_atoms = top.regex_get_atoms('^(N|O)$')

        x = np.array(range(3 * top.num_atoms))

        c_x = c_atoms.get_coords(x)
        no_x = no_atoms.get_coords(x)

        expected_c_x = np.array(range(3 * 3, 3 * 4) + range(3 * 5 + 3 * 2, 3 * 5 + 3*3))
        expected_no_x = np.array(range(3 * 0, 3 * 1) + range(3 * 4, 3 * 5)
                                 + range(3 * 5 + 3 * 0, 3 * 5 + 3 * 1) 
                                 + range(3 * 5 + 3 * 3, 3 * 5 + 3 * 4))

        self.assertEqual(list(c_x), list(expected_c_x))
        self.assertEqual(list(no_x), list(expected_no_x))


    def test_get_atomset_coords(self):
        top = self.make_top()

        c_atoms = top.get_atomset(['C'])
        no_atoms = top.get_atomset(['N', 'O'])

        x = np.array(range(3 * top.num_atoms))

        c_x = c_atoms.get_coords(x)
        no_x = no_atoms.get_coords(x)

        expected_c_x = np.array(range(3 * 3, 3 * 4) + range(3 * 5 + 3 * 2, 3 * 5 + 3*3))
        expected_no_x = np.array(range(3 * 0, 3 * 1) + range(3 * 4, 3 * 5)
                                 + range(3 * 5 + 3 * 0, 3 * 5 + 3 * 1) 
                                 + range(3 * 5 + 3 * 3, 3 * 5 + 3 * 4))

        self.assertEqual(list(c_x), list(expected_c_x))
        self.assertEqual(list(no_x), list(expected_no_x))



    def test_get_regex_not_atom_coords(self):
        top = self.make_top()

        not_c_atoms = top.regex_get_other_atoms('^C$')
        not_no_atoms = top.regex_get_other_atoms('^(N|O)$')

        x = np.array(range(3 * top.num_atoms))

        not_c_x = not_c_atoms.get_coords(x)
        not_no_x = not_no_atoms.get_coords(x)

        expected_not_c_x = np.array(range(3 * 0, 3 * 3) + range(3 * 4, 3 * 7) + range(3 * 8, 3 * 9))
        expected_not_no_x = np.array(range(3 * 1, 3 * 4) + range(3 * 6, 3 * 8))

        self.assertEqual(list(not_c_x), list(expected_not_c_x))
        self.assertEqual(list(not_no_x), list(expected_not_no_x))



    def test_set_atom_coords(self):
        top = self.make_top()

        c_atoms = top.get_atoms('C')
        cb_atoms = top.get_atoms('CB')

        x = np.array(range(3 * top.num_atoms))

        expected_c_x = np.array(range(6, 12))
        expected_cb_x = np.array(range(10,13))

        c_atoms.set_coords(x, expected_c_x)
        cb_atoms.set_coords(x, expected_cb_x)

        c_x = c_atoms.get_coords(x)
        cb_x = cb_atoms.get_coords(x)

        self.assertEqual(list(expected_c_x), list(c_x))
        self.assertEqual(list(expected_cb_x), list(cb_x))


class PolymerMonomerTestCase(unittest.TestCase):

    def make_top(self):
        ala = t.Molecule('ALA', ['N', 'CA', 'CB', 'C', 'O'])
        gly = t.Molecule('GLY', ['N', 'CA', 'C', 'O'])
        return t.Polymer('poly', [ala, gly])        


    def test_monomer_number(self):
        top = self.make_top()

        self.assertEqual(top.num_monomers, 2)

    def test_default_atom_offsets(self):
        top = self.make_top()

        self.assertEqual(list(top.atom_offsets), range(3 * (5 + 4)))

    def test_default_target_offsets(self):
        top = self.make_top()

        self.assertEqual(list(top.target_offsets), range(3 * (5 + 4)))


    def test_get_monomer_by_index(self):
        top = self.make_top()

        ala = top.get_monomer_by_index(0)
        gly = top.get_monomer_by_index(1)

        self.assertEqual(ala.name, 'ALA')
        self.assertEqual(gly.name, 'GLY')


    def test_monomer_atom_offsets(self):
        top = self.make_top()

        ala = top.get_monomer_by_index(0)
        gly = top.get_monomer_by_index(1)

        self.assertEqual(list(ala.atom_offsets), range(3 * 5))
        self.assertEqual(list(gly.atom_offsets), range(3 * 5, 3 * 5 + 3 * 4))


    def test_get_monomer(self):
        top = self.make_top()

        ala = top.get_monomer('ALA')

        self.assertEqual(ala.num_atoms, 5)
        self.assertEqual(ala.atoms, ['N', 'CA', 'CB', 'C', 'O'])

        gly = top.get_monomer('GLY')

        self.assertEqual(gly.num_atoms, 4)
        self.assertEqual(gly.atoms, ['N', 'CA', 'C', 'O'])


        self.assertEqual(top.num_monomers, 2)
        

    def test_get_monomer_coords(self):

        top = self.make_top()

        x = np.array(range(3 * top.num_atoms))
        
        ala = top.get_monomer('ALA')
        expected_ala_x = np.array(range(3*5))
        ala_x = ala.get_coords(x)
        self.assertEqual(list(ala_x), list(expected_ala_x))

        gly = top.get_monomer('GLY')
        expected_gly_x = np.array(range(3 * 5, 3 * 5 + 3 * 4))
        gly_x = gly.get_coords(x)
        self.assertEqual(list(gly_x), list(expected_gly_x))

    def test_set_monomer_coords(self):
        top = self.make_top()

        x = np.array(range(3 * top.num_atoms))
        
        ala = top.get_monomer('ALA')
        expected_ala_x = np.array(range(20, 35))
        ala.set_coords(x, expected_ala_x)
        ala_x = ala.get_coords(x)
        self.assertEqual(list(ala_x), list(expected_ala_x))

        gly = top.get_monomer('GLY')
        expected_gly_x = np.array(range(30, 30 + 3 * 4))
        gly.set_coords(x, expected_gly_x)
        gly_x = gly.get_coords(x)
        self.assertEqual(list(gly_x), list(expected_gly_x))

        
    def test_multi_get_monomer_coords(self):

        ala = t.Molecule('ALA', ['N', 'CA', 'CB', 'C', 'O'])
        gly = t.Molecule('GLY', ['N', 'CA', 'C', 'O'])
        top = t.Polymer('poly', [ala, gly, ala])

        x = np.array(range(3 * top.num_atoms))
        
        ala = top.get_monomer('ALA')

        expected_ala_x = np.array(range(3*5) + range(3*9,3*(9+5)))
        ala_x = ala.get_coords(x)
        self.assertEqual(list(ala_x), list(expected_ala_x))


    def test_multi_set_monomer_coords(self):

        ala = t.Molecule('ALA', ['N', 'CA', 'CB', 'C', 'O'])
        gly = t.Molecule('GLY', ['N', 'CA', 'C', 'O'])
        top = t.Polymer('poly', [ala, gly, ala])

        x = np.array(range(3 * top.num_atoms))
        
        ala = top.get_monomer('ALA')
        expected_ala_x = np.array(range(100,130))
        ala.set_coords(x, expected_ala_x)
        ala_x = ala.get_coords(x)
        self.assertEqual(len(list(ala_x)), len(list(expected_ala_x)))
        self.assertEqual(list(ala_x), list(expected_ala_x))


class MoleculeLiftTestCase(unittest.TestCase):

    def test_reorder_get_namemap(self):
        first_ala = t.Molecule('FirstALA', ['N', 'CA',  'C', 'O', 'G'])
        second_ala = t.Molecule('SecondALA', ['N', 'CA',  'C', 'O', 'CB'])

        first_coords = np.array(range(3 * first_ala.num_atoms))
        second_coords = np.array(range(0 * 3, 2 * 3) + range(3 * 3, 5 * 3) + range(2 * 3, 3 * 3))
        self.assertEqual(list(first_ala.get_atoms('C').get_coords(first_coords)), list(second_ala.get_atoms('CB').get_coords(second_coords)))

        first_to_second = {'C':'CB',
                          'O': 'C',
                          'G': 'O'}


        second_to_first = dict((kv[1], kv[0]) for kv in first_to_second.iteritems())

        first_lift_second = first_ala.lift_topology(second_ala,
                                                    namemap=t.namedict(second_to_first))

        
        self.assertEqual(list(first_coords), list(first_lift_second.lift_coords(second_coords)))


    def test_lift_subset_shape(self):
        first_ala = t.Molecule('FirstALA', ['N', 'CA',  'CB', 'C', 'O'])
        second_ala = t.Molecule('SecondALA', ['N', 'CA',  'C', 'O'])

        first_coords = np.array(range(3 * first_ala.num_atoms))
        second_coords = np.array(range(0 * 3, 2 * 3) + range(3 * 3, 5 * 3))

        self.assertEqual(list(first_ala.get_atoms('C').get_coords(first_coords)), list(second_ala.get_atoms('C').get_coords(second_coords)))

        first_lift_second = first_ala.lift_topology(second_ala)
        
        z = first_lift_second.get_coords(second_coords)

        self.assertEqual(z.shape, second_coords.shape)

    def test_lift_subset_coords(self):
        first_ala = t.Molecule('FirstALA', ['N', 'CA',  'CB', 'C', 'O'])
        second_ala = t.Molecule('SecondALA', ['N', 'CA',  'C', 'O'])


        first_coords = np.array(range(3 * first_ala.num_atoms))
        second_coords = np.array(range(0 * 3, 2 * 3) + range(3 * 3, 5 * 3))
        self.assertEqual(list(first_ala.get_atoms('C').get_coords(first_coords)), list(second_ala.get_atoms('C').get_coords(second_coords)))

        first_lift_second = first_ala.lift_topology(second_ala)
        subfirst_second = first_ala.get_atomset(second_ala.atoms)

        z = first_lift_second.get_coords(second_coords)
        subfirst_coords = subfirst_second.get_coords(first_coords)

        self.assertEqual(list(z), list(subfirst_coords))


    def test_lift_subset_listshape(self):
        first_ala = t.Molecule('FirstALA', ['N', 'CA',  'CB', 'C', 'O'])
        second_ala = t.Molecule('SecondALA', ['N', 'CA',  'C', 'O'])


        first_coords = np.array(range(3 * first_ala.num_atoms))
        second_coords = np.array(range(0 * 3, 2 * 3) + range(3 * 3, 5 * 3))
        self.assertEqual(list(first_ala.get_atoms('C').get_coords(first_coords)), list(second_ala.get_atoms('C').get_coords(second_coords)))

        first_lift_second = first_ala.lift_topology(second_ala)
        
        z = first_lift_second.lift_coords(second_coords)

        self.assertEqual(z.shape, first_coords.shape)

    def test_lift_subset_liftcoords(self):
        first_ala = t.Molecule('FirstALA', ['N', 'CA',  'CB', 'C', 'O'])
        second_ala = t.Molecule('SecondALA', ['N', 'CA',  'C', 'O'])

        first_coords = np.array(range(3 * first_ala.num_atoms))
        second_coords = np.array(range(0 * 3, 2 * 3) + range(3 * 3, 5 * 3))
        self.assertEqual(list(first_ala.get_atoms('C').get_coords(first_coords)), list(second_ala.get_atoms('C').get_coords(second_coords)))

        first_lift_second = first_ala.lift_topology(second_ala)
        subfirst_second = first_ala.get_atomset(second_ala.atoms)

        z = first_lift_second.lift_coords(second_coords)
        subfirst_coords = np.zeros(first_coords.shape)
        subfirst_second.set_coords(subfirst_coords, subfirst_second.get_coords(first_coords))

        self.assertEqual(list(first_ala.get_atoms('C').get_coords(z)), list(first_ala.get_atoms('C').get_coords(subfirst_coords)))

        self.assertEqual(list(z), list(subfirst_coords))
        
class PolymerLiftTestCase(unittest.TestCase):

    def make_tops(self):
        first_monomers = t.Monomers([t.Molecule('ALA', 
                                                ['N', 'CA', 'CB', 'C', 'O']),
                                     t.Molecule('GLY',
                                                ['N', 'CA', 'C', 'O'])])

        second_monomers = t.Monomers([t.Molecule('ALA', 
                                                 ['N', 'CA',  'C', 'O', 'CB']),
                                     t.Molecule('GLY',
                                                ['N', 'CA', 'C', 'O'])])

        first_polymer = t.Polymer('firstpoly', first_monomers.sequence(['ALA', 'GLY']))
        second_polymer = t.Polymer('secondpoly', second_monomers.sequence(['ALA', 'GLY']))

        return first_polymer, second_polymer
    
    def test_reorder(self):

        first_polymer, second_polymer = self.make_tops()

        # first_coords = np.array(range(3 * 0, 3 * 9))
        second_coords = np.array(range(3 * 0, 3 * 2)  + range(3 * 3, 3 * 5)  + range(3 * 2, 3 * 3) + range(3 * 5, 3 * 9))        



        first_lift_second = first_polymer.lift_topology(second_polymer)

        first_coords = first_lift_second.lift_coords(second_coords)
        

        first_c_atoms = first_polymer.get_atoms('C')
        second_c_atoms = second_polymer.get_atoms('C')
        
        first_c_x = first_c_atoms.get_coords(first_coords)
        second_c_x = second_c_atoms.get_coords(second_coords)

        self.assertEqual(list(first_c_x), list(second_c_x))


    def test_lift_subset_shape(self):

        first_polymer, second_polymer = self.make_tops()

        first_coords = np.array(range(3 * 0, 3 * 9))
        # second_coords = np.array(range(3 * 0, 3 * 2)  + range(3 * 3, 3 * 5)  + range(3 * 2, 3 * 3) + range(3 * 5, 3 * 9))        

        first_n = first_polymer.get_atoms('N')
        first_n_coords = first_n.get_coords(first_coords)

        self.assertEqual(first_n_coords.shape, (2 * 3,))

        first_lift_n = first_polymer.lift_topology(first_n.get_contiguous_topology())

        self.assertEqual(first_lift_n.shape, first_coords.shape)

        first_lift_n_liftcoords = first_lift_n.lift_coords(first_coords)

        self.assertEqual(first_lift_n_liftcoords.shape, first_coords.shape)


class MoleculeChangeNDOFTestCase(unittest.TestCase):

    initial_ndof = 3
    final_ndof = 1

    def make_top(self, ndof):
        return t.Molecule('water', ['H', 'O', 'H'], ndof=ndof)

    def test_default_offsets(self):
        initial_top = self.make_top(self.initial_ndof)

        final_top = initial_top.change_ndof(self.final_ndof)

        self.assertEqual(list(final_top.atom_offsets), range(3 * self.final_ndof))

    
    def test_get_atoms(self):
        initial_top = self.make_top(self.initial_ndof)

        top = initial_top.change_ndof(self.final_ndof)

        h_atoms = top.get_atoms('H')
        o_atoms = top.get_atoms('O')

        self.assertEqual(len(h_atoms), 2)
        self.assertEqual(len(o_atoms), 1)

    def test_get_atom_coords(self):
        initial_top = self.make_top(self.initial_ndof)

        top = initial_top.change_ndof(self.final_ndof)

        h_atoms = top.get_atoms('H')
        o_atoms = top.get_atoms('O')


        x = np.array(range(self.final_ndof * top.num_atoms))

        h_x = h_atoms.get_coords(x)
        o_x = o_atoms.get_coords(x)

        expected_h_x = np.array(range(0 * self.final_ndof, 1 * self.final_ndof) + range(2 * self.final_ndof, 3 * self.final_ndof))
        expected_o_x = np.array(range(1 * self.final_ndof, 2 * self.final_ndof))

        self.assertEqual(list(expected_h_x), list(h_x))
        self.assertEqual(list(expected_o_x), list(o_x))


if __name__ == "__main__":
    unittest.main()
