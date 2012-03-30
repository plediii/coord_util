
import unittest

import os

import aminoacids as aa
import static_files

import pdb as p


test_file = static_files.static_file_func(__file__, 'test_data', 
                                          {'1xfq': '1XFQ.pdb',
                                           '1xfq_atoms' : '1XFQ_atoms.dat',
                                           '1xfq_coords' : '1XFQ_coords.dat',
                                           '1xfq_residues' : '1XFQ_residues.dat',
                                           '1xfq_idcs' : '1XFQ_idcs.dat',
                                           'two_chain': 'two_chain.pdb',
                                           'two_chain_atoms': 'two_chain_atoms.dat',
                                           'two_chain_residues': 'two_chain_residues.dat',
                                           'two_chain_idcs': 'two_chain_idcs.dat',
                                           'two_chain_coords': 'two_chain_coords.dat'})


class MonomerAtomsTestCase(unittest.TestCase):

    pdb_file = test_file('1xfq')

    def test_monomer_atoms(self):
        top = p.read_topology(self.pdb_file, name='top')

        # Make sure we have something non-trivial to test
        self.assertGreater(top.monomers[0].num_monomers, 50)

        something_checked = False

        # iterate through the monoers in the first chain.  The second chain is cynamic acid
        for monomer in top.monomers[0].monomers:
            residue_name = monomer.name[:3]
            try:
                idx = int(monomer.name[3:])
            except ValueError:
                # print monomer.name, '"', monomer.name[3:], '"'
                raise

            # skip several residues which are be modified from the natural amino acid set.
            if idx > 1 and idx < 125 and residue_name in aa.aminoacids.monomer_dict and residue_name != 'CYS':
                something_checked = True
                aa_monomer = aa.aminoacids.monomer_dict[residue_name]

                self.assertEqual(monomer.num_atoms, aa_monomer.num_atoms)
                # if not set(monomer.atoms) == set(aa_monomer.atoms):
                    # print monomer.name
                self.assertEqual(set(monomer.atoms), set(aa_monomer.atoms))

        self.assertTrue(something_checked)


def get_list(filename):
    with open(filename) as f:
        return [s.strip() for s in f.read().split()]

class TopologyTestCase(unittest.TestCase):

    pdb_file = test_file('1xfq')

    atom_names = get_list(test_file('1xfq_atoms'))

    residue_names = get_list(test_file('1xfq_residues'))

    residue_idcs = get_list(test_file('1xfq_idcs'))

    def test_get_topology(self):
        top = p.read_topology(self.pdb_file, 'PYP')
        
        # self.assertEqual(top.num_atoms, prmtop.get_num_atoms())
        self.assertEqual(top.name, 'PYP')

        top = top.flatten()

        self.assertEqual(top.name, 'PYP')

        atom_names = []
        monomer_names = []

        for monomer in top.monomers:
            atom_names.extend(monomer.atoms)
            monomer_names.append(monomer.name)
        
        self.assertEqual(atom_names, self.atom_names)

        residue_names = [name + idx
                         for idx, name in zip(self.residue_idcs, 
                                              self.residue_names)]

        self.assertEqual(monomer_names, residue_names)


def get_float_list(filename):
    return [float(s) for s in get_list(filename)]

class ReadCoordsTestCase(unittest.TestCase):

    pdb_file = test_file('1xfq')

    num_coords_in_file = 20

    expected_coords = get_float_list(test_file('1xfq_coords'))

    def test_read_coords(self):
        coords = p.read_coords(self.pdb_file).next()
        self.assertEqual(list(coords), list(self.expected_coords))

    def test_num_coords(self):
        num_in_file = sum(1 for coords in p.read_coords(self.pdb_file))

        self.assertEqual(num_in_file, self.num_coords_in_file)

class ReadWriteCoordsTestCase(unittest.TestCase):

    initial_pdb_file = test_file('1xfq')
    test_pdb_file = 'test.pdb'

    def setup(self):
        test_pdb_file = self.test_pdb_file
        if os.path.exists(test_pdb_file):
            os.remove(test_pdb_file)

    def tearDown(self):
        test_pdb_file = self.test_pdb_file
        if os.path.exists(test_pdb_file):
            os.remove(test_pdb_file)
    


    def test_read_write_coords(self):
        top = p.read_topology(self.initial_pdb_file, name='pyp')

        p.write_coords('test.pdb', top, p.read_coords(self.initial_pdb_file))

        for idx, (read_coords, expected_coords) in enumerate(zip(p.read_coords('test.pdb'), p.read_coords(self.initial_pdb_file))):
            self.assertEqual(list(expected_coords), list(read_coords))

        


class TwoChainTopologyTestCase(unittest.TestCase):

    pdb_file = test_file('two_chain')
    atom_names = get_list(test_file('two_chain_atoms'))
    residue_names = get_list(test_file('two_chain_residues'))
    residue_idcs = get_list(test_file('two_chain_idcs'))
    expected_coords = get_float_list(test_file('two_chain_coords'))


    def test_get_topology(self):
        top = p.read_topology(self.pdb_file, name='two')
        
        # self.assertEqual(top.num_atoms, prmtop.get_num_atoms())

        atom_names = []
        monomer_names = []

        top = top.flatten()        

        for monomer in top.monomers:
            atom_names.extend(monomer.atoms)
            monomer_names.append(monomer.name)
        
        self.assertEqual(atom_names, self.atom_names)

        residue_names = [name + str(idx) 
                         for idx, name in zip(self.residue_idcs, 
                                              self.residue_names)]

        self.assertEqual(monomer_names, residue_names)
    

if __name__ == "__main__":
    unittest.main()




