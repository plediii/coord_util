
import topology as t

ala = t.Molecule('ALA', ['N', 'H', 'CA', 'HA', 'C', 'O', 'CB', 'HB1', 'HB2', 'HB3'])

arg = t.Molecule('ARG', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'HG3', 'HG2', 'CD', 'HD3', 'HD2', 'NE', 'HE', 'CZ', 'NH1', 'HH11', 'HH12', 'NH2', 'HH21', 'HH22', 'C', 'O'])

asn = t.Molecule('ASN', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'OD1', 'ND2', 'HD22', 'HD21', 'C', 'O'])

asp = t.Molecule('ASP', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'OD1', 'OD2', 'C', 'O'])

cys = t.Molecule('CYS', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'SG', 'HG', 'C', 'O'])

gln = t.Molecule('GLN', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'HG3', 'HG2', 'CD', 'OE1', 'NE2', 'HE22', 'HE21', 'C', 'O'])

glu = t.Molecule('GLU', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'HG3', 'HG2', 'CD', 'OE1', 'OE2', 'C', 'O'])

gly = t.Molecule('GLY', ['N', 'H', 'CA', 'HA3', 'HA2', 'C', 'O'])

his = t.Molecule('HIS', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'ND1', 'CE1', 'HE1', 'NE2', 'HE2', 'CD2', 'HD1', 'HD2', 'C', 'O'])

ile = t.Molecule('ILE', ['N', 'H', 'CA', 'HA', 'CB', 'HB', 'CG2', 'HG21', 'HG22', 'HG23', 'CG1', 'HG13', 'HG12', 'CD1', 'HD11', 'HD12', 'HD13', 'C', 'O'])

leu = t.Molecule('LEU', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'HG', 'CD1', 'HD11', 'HD12', 'HD13', 'CD2', 'HD21', 'HD22', 'HD23', 'C', 'O'])

lys = t.Molecule('LYS', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'HG3', 'HG2', 'CD', 'HD3', 'HD2', 'CE', 'HE3', 'HE2', 'NZ', 'HZ1', 'HZ2', 'HZ3', 'C', 'O'])

met = t.Molecule('MET', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'HG3', 'HG2', 'SD', 'CE', 'HE1', 'HE2', 'HE3', 'C', 'O'])

phe = t.Molecule('PHE', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'CD1', 'HD1', 'CE1', 'HE1', 'CZ', 'HZ', 'CE2', 'HE2', 'CD2', 'HD2', 'C', 'O'])

pro = t.Molecule('PRO', ['N', 'CD', 'HD3', 'HD2', 'CG', 'HG3', 'HG2', 'CB', 'HB3', 'HB2', 'CA', 'HA', 'C', 'O'])

ser = t.Molecule('SER', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'OG', 'HG', 'C', 'O'])

thr = t.Molecule('THR', ['N', 'H', 'CA', 'HA', 'CB', 'HB', 'CG2', 'HG21', 'HG22', 'HG23', 'OG1', 'HG1', 'C', 'O'])

trp = t.Molecule('TRP', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'CD1', 'HD1', 'NE1', 'HE1', 'CE2', 'CZ2', 'HZ2', 'CH2', 'HH2', 'CZ3', 'HZ3', 'CE3', 'HE3', 'CD2', 'C', 'O'])

tyr = t.Molecule('TYR', ['N', 'H', 'CA', 'HA', 'CB', 'HB3', 'HB2', 'CG', 'CD1', 'HD1', 'CE1', 'HE1', 'CZ', 'OH', 'HH', 'CE2', 'HE2', 'CD2', 'HD2', 'C', 'O'])

val = t.Molecule('VAL', ['N', 'H', 'CA', 'HA', 'CB', 'HB', 'CG1', 'HG11', 'HG12', 'HG13', 'CG2', 'HG21', 'HG22', 'HG23', 'C', 'O'])

aminoacids = t.Monomers([ala, arg, asn, asp, cys, gln, glu, gly, his, ile, leu, lys, met, phe, pro, ser, thr, trp, tyr, val])

# cpb = t.Molecule('CPB', ['N', 'CA', 'CB', 'SG', 'C1', 'O1', 'C2', 'C3', "C1'", "C2'", "C3'", "C4'", "C5'", "C6'", "H6'", "H5'", "O4'", 'HO4', "H3'", "H2'", 'H3', 'H2', 'HB2', 'HB3', 'HA', 'C', 'O'])
