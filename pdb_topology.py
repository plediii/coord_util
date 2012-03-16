
import numpy as np
import topology as t

import os

# def is_multichain(pdb_file_name):
#     with open(pdb_file_name) as pdb_file:
#         for line in pdb_file:
#             line_type = line[:6].strip()
#             if line_type == 'TER':
#                 return True
#     return False

def read_topology_parts(pdb_file_name):
    with open(pdb_file_name) as pdb_file:
        for line in pdb_file:
            line_type = line[:6].strip()

            if line_type == 'ATOM' or line_type == 'HETATM':
                if line[12].isdigit():
                    atom_name = (line[13:16].strip() + line[12]).strip()
                else:
                    atom_name = line[12:16].strip()
                resname = line[17:20].strip()
                res_idx = int(line[23:26])
                
                # print '      yielding ', atom_name, resname, res_idx
                yield atom_name, resname, res_idx

            elif line_type == 'TER':
                yield None
            elif line_type == 'ENDMDL':
                return 
                

def read_residues(pdb_file_name):
    """Return a sequence of resname, atom_names for each molecule in the geometry or None.

    Chain separations are denoted by Nones.

    """
    atom_names = []
    res_idcs_seen = set()

    last_resname = None
    last_res_idx = -1e100

    for part in read_topology_parts(pdb_file_name):
        # print 'part = ', part
        if not part:
            last_resname += str(last_res_idx)
            yield last_resname, atom_names
            yield None
            atom_names = []
            continue

        atom_name, resname, res_idx = part
        if last_res_idx != res_idx and atom_names != []:
            assert last_resname is not None

            last_resname += str(last_res_idx)

            yield last_resname, atom_names

            atom_names = []
            res_idcs_seen.add(res_idx)

        atom_names.append(atom_name)

        last_res_idx = res_idx
        last_resname = resname

    if atom_names != []:
        last_resname += str(last_res_idx)
        yield last_resname, atom_names

         

def read_topology(pdb_file_name, name=None):
    if name is None:
        name = os.path.splitext(pdb_file_name)[0]
    chain_idx = 0
    chain_monomers = []
    monomers = []
    for residue in read_residues(pdb_file_name):
        if residue is None:
            chain_monomers.append(t.Polymer('%s_CHAIN%d' % (name, chain_idx), monomers))
            chain_idx += 1
            monomers = []
        else:
            resname, atoms = residue
            monomers.append(t.Molecule(resname, atoms))
            
    if chain_monomers != []:
        if monomers != []:
            chain_monomers.append(t.Polymer('%s_CHAIN%d' % (name, chain_idx), monomers))

        return t.Polymer(name, chain_monomers)

    else:
        return t.Polymer(name, monomers)


def read_coord_parts(pdb_file_name):
    with open(pdb_file_name) as pdb_file:
        for line in pdb_file:
            line_type = line[:6].strip()

            if line_type == 'ATOM' or line_type == 'HETATM':
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])

                yield [x, y, z]

            elif line_type == 'ENDMDL':
                yield None


def read_coords(pdb_file_name):

    coords = []

    for coord in read_coord_parts(pdb_file_name):
        if coord is None:
            if coords != []:
                yield np.array(coords)
                # print 'yield reset'
                coords = []
        else:
            coords.extend(coord)

    if coords != []:
        yield np.array(coords)
        # print 'yield final'

    # print 'done'


class PDBError(Exception):
    pass

def molecule_coords_to_pdb(monomer, coords, adx=1, mdx=1):
    resname = monomer.name[:3]
    pdb_lines = []
    for atom in monomer.atoms:
        if len(atom) < 4:
            atom_name = ' %-3s' % atom
        elif len(atom) == 4:
            atom_name = atom
        else:
            raise PDBError("Atom name too long: '%s'" % atom)

        x, y, z = coords[3 * (adx - 1):3 * adx]
        pdb_lines.append('ATOM  %(adx)5d %(atom_name)s %(resname)3s   %(mdx)3d   %(x)8.3f%(y)8.3f%(z)8.3f' % locals())

        adx += 1
    return '\n'.join(pdb_lines)
        
    

def single_chain_coords_to_pdb(top, coords):
    if len(coords) != 3 * top.num_atoms:
        raise PDBError("Wrong number of atoms in coords to match topology: %s != %s" % (len(coords), 3 * top.num_atoms))
    
    adx = 1
    monomer_parts = []
    for mdx, monomer in enumerate(top.monomers, 1):
        monomer_parts.append(molecule_coords_to_pdb(monomer, coords, adx=adx, mdx=mdx))
        adx += monomer.num_atoms
    return '\n'.join(monomer_parts)

def multi_chain_coords_to_pdb(top, coords):
    if len(coords) != 3 * top.num_atoms:
        raise PDBError("Wrong number of atoms in coords to match topology: %s != %s" % (len(coords), 3 * top.num_atoms))

    single_chain_parts = []
    
    for polymer in top.monomers:
        chain_coords = polymer.get_coords(coords)
        single_chain_parts.append(single_chain_coords_to_pdb(polymer, chain_coords))

    return '\nTER\n'.join(single_chain_parts)

def coords_to_pdb(top, coords):
    if isinstance(top, t.Molecule):
        return molecule_coords_to_pdb(top, coords)
    elif isinstance(top, t.Polymer):
        if isinstance(top.monomers[0], t.Polymer):
            return multi_chain_coords_to_pdb(top, coords)
        else:
            return single_chain_coords_to_pdb(top, coords)
    else:
        raise Exception("Unrecognized Topology type.")

def write_coords(pdb_file_name, top, coords_iter):
    with open(pdb_file_name, 'w') as pdb_file:
        for coords in coords_iter:
            pdb_file.write(coords_to_pdb(top, coords))
            pdb_file.write('\nENDMDL\n')
