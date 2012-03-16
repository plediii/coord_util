
# coord_util

coord_util is a library for reading, manipulating and writing molecule
geometries. coord_util can read and write geometries in several common
formats.  

## Dependencies

coord_util depends on my `tempfile_util` module.

coord_util also depends on `numpy` (tested with 1.6.1).  

coord_util contains a module for storing geometries in a useful
database format, `trajdb`.  In order to make use of this module, coord_util
depends on the presence of `sqlite3` and `h5py`.

Scripts for building all of the above dependencies in the user's home
directory (and thus not requring root permissions) are available in my
`build_scripts` repository.

## Configure and Build

Several geometry related functions included in coord_util have
optimized versions written purely in fortran.  To use these efficient
codes, it is necessary to compile and link with them using f2py (f2py
is included in numpy).  When coord_util is not able to successfully
link to these versions, a warning will be displayed, and coord_util
will use the less efficient versions written in pure python.

The makefile will 
Makefiles tailored to gfortran and ifort on the computers I used are
available in the configuration directory.  The program `configure.py`
will attempt to identify the best available compiler and link the
appropriate makefile.  It should be possible to build 

	./configure.py
	make



### Modules

#### coord_math

The coord_math module exposes several geometric functions which
interpret one-dimensional numpy arrays holding contiguous sequence of
atoms.  The arguments to the coord_math functions assume that the
numpy arrays are in the order:

      x = np.array([x1, y1, z1, x2, y2, z2, ..., xn, yn, zn]),

where `x1` is the x coordinate of the first atom, `y2` is the y
coordinate of the second atom, and `zn` is the z coordinate of the nth
atom.  The atom index in the following functions is 1-based, so that
the first atom has index 1.

##### get_atom_coords
get_atom_coords returns a 1x3 array containing the coordinates of the ith atom.

		get_atom_coords(np.array([1, 2, 3, 4, 5, 6]), 2) == np.array([4, 5, 6])

##### center_of_geometry

center_of_geometry returns a 1x3 array containing the coordinates at
the average of the atom coordinates in the system. 

For instance, the center of geometry of atoms arranged at the corners
of a square is the center of the square:

    center_of_geometry(np.array([0., 0., 0., 
                                 1., 0., 0.,
	                         0., 1., 0.,
	                         0., 0., 1.,]))
	                         == np.array([0.5, 0.5, 0.5])

##### rmsd

`rmsd` is a slight misnomer, since rmsd is the *least* root mean
square distance between two geometries.  However, the convention is to
simply refer to this measure as rmsd. The *non* least root mean square
distance between two geometries is simply the l2-norm of the
difference vector, divided by the square root of the number of atoms:

       rootmeansquare(v1, v2) == sqrt(dot(v1-v2, v1-v2)/(len(v1)/3)).

The *least* root mean square is the least root mean square between the
two vectors, amongst all possible rotations and translations of the
geometry.  The intuition for using the least rmsd is that, for
example, changes in a water molecule geometry by rotation or
translation are irrelevant to its dynamics.  

Since `rmsd` gives the least root mean square distance, we have, for
example, that

	rmsd(v1, v2) == rmsd(v1, translate(v2, anything))

and

	rmsd(v1, v2) == rmsd(v1, rotate(v2, anyangle)).


##### translate

`translate` displaces all atoms in a geometry by a uniform vector; for
example, if we translate a geometry via,

	    translate(geom, delta_vector).

Then, for any atom in the geometry

    get_atom_coords(geom, idx) - get_atom_coords(translate(geom, delta_vector)), idx) == delta_vector.

##### dihedral

`dihedral` calculates the dihedral angle between involving for atoms.  Example:

	   dihedral(geom, idx, jdx, kdx, ldx)

##### atom_dist

`atom_dist` calculates the distance between the idxth and jdxth atoms.  Example:

	    atom_dist(geom, idx, jdx).

##### rotate_euler

`rotate_euler` rotates the geometry about the origin according to the euler angles.  Example:

	       rotate_euler(geom, alpha, beta, gamma).


##### transform

`transform` applies a 3x3 transformation matrix to each atom in the geometry.  Example:

	    transform(geom, euler_rotation_matrix(alpha, beta, gamma)).

## topology

The `topology` module exposes classes and functions for selecting and
manipulating components of geometries, especially residues of
proteins.  The inspiration for the design of this module came from the
pattern used by `jQuery` for selecting and manipulating components of
the DOM.

The need for this module in my own projects arose in the context of
monte-carlo rotamer switching in protein dynamics. Rotamer switching
refers to changing the geometry of a single amino acid side chain in a
protein between different stable formations separated by energetic
frustration.  Monte-Carlo rotamer switching allows for rapid
exploration of a protein's dynamical space without requiring the time
normally required for transitions within the residues.

The usefulness of the `topology` module goes beyond just rotamer
switching.  When coupled with coordinates describing a protein
geometry, it can be used to extract specific atoms, or switch the atom
order in a clear way.

Use of the `topology` module centers around the `Topology` class.
Instances of the topology classes can be read by reading the topology
of a PDB file, or by creating them manually.  


### Creating topology instances

For example, to obtain the topology describing the model in  "protein.pdb":

    import coord_util.pdb_topology as pt
    
    top = pt.read_topology('protein.pdb')


Alternatively, specific topologies can be constructed manually.  For
instance, we can construct a toplogy for a glycine residue, or a water
molecule:

	import topology as t

	gly = t.Molecule('GLY', ['N', 'CA', 'C', 'O'])
	water = t.Molecule('HOH', ['H', 'O', 'H'])

Individual molecules can be composed to create polymers.  A glycine dipeptide can be constructed via:

	   digly = t.Polymer('GLYGLY', [gly, gly])

Polymers can be composed with water molecules to create a dipeptide solvated in 100 water molecules:

	 system = t.Polymer('solvagted gly', [digly] + [water] * 100)

Alternatively, chains can be constructed by creating a monomer set, and using its sequence method.

	ala = t.Molecule('ALA', ['N', 'CA', 'CB', 'C', 'O'])

	  monomers = t.Monomers([gly, ala])

	  gly_ala_gly = t.Polymer('GLYALAGLY', monomers.sequence(['GLY', 'ALA', 'GLY']))

The `coord_util` project includes a module `aminoacids` with the standard set of aminoacids:

    from aminoacids import aminoacids

    gly_ala_gly = aminoacids.sequence(['ALA', 'GLY', 'ALA'])

	  
### Selecting and extracting substructures

A `Topology` instance, when coupled with the coordinates in the PDB
file, allows us to select specific components.  

Suppose we already have the topology in "protein.pdb", "top" from
above.  The trajectory of geometries in the PDB file can be obtained
via:

	   xs = list(pt.read_coords('protein.pdb'))

The coordinates of specific components of the geometry can be
extracted by coupling a topology instance with the coordinate
described.  For instance, to extract only the CA atoms in the protein,
we can use the `Topolgy.get_atoms` method to create a subtopology, and
`Topology.get_coords` to extract the coordinates for those atoms from
a numpy array:


      ca_top = top.get_atoms('CA')
      ca_xs = [ca_top.get_coords(x) for x in xs]
	   

After the above, assuming the protein consists of N residues with CA
atoms, each of the ca_xs are numpy arrays of length 3N containing
the coordinates of the CA atoms.

Alternatively, we could extract just the backbone of the geometry
using the `Topology.get_atomset` method:


	       backbone_top = top.get_atomset(['CA', 'CB', 'C', 'N', 'O'])

Atoms can also be selected with regular expressions (regex).  We could
have selected the backbone atoms using a regex instead:

	       backbone_top = top.regex_get_atoms('^(CA|CB|C|N|O)$')

We could also select for specific monomers by name using
`Polymer.get_monomer(resname)`, `Polymer.monomers_slice(idx, jdx)` and
`Polymer.get_monomer_by_index(idx, jdx)`.

### Replacing substructures

Besides extracting substructures from a geometry, replacing those
substructures into a geometry is also useful.  In the case of the
rotamer switching problem, for instance, we want to change the
coordinates of specific side chains in the protein.  This operation is
implemented by the `Topology.set_coords` method.

For instance, suppose we have the subtopology for the first monomer in a Polymer:

    first = top.get_monomer_by_index(0).

If `x` is an numpy array of length 3N (corresponding to the N atoms
described by `top`), and `x1` is a numpy array of length 3M
(corresponding to the M atoms of the first residue), we can change the
geometry of the first residue to that of `x1` by

	 first.set_coords(x, x1).


### Lifting and reordering atoms

When building a geometry from scratch from its constituent
substructures, a common operation is to build a new array for the
entire geometry, and fill in each of the substructures using
subtopologies For instance, suppose we are beginning to reconstruct a
geometry from its CA atoms.  We can create a numpy array for the
entire geometry, with the CA atoms already filled in using
`Topology.lift_coords` like so:


		       lift_ca = top.lift_coords(top.get_atoms('CA'))
		       
		       full_x = lift_ca.lift_coords(ca_x)

Then, assuming `ca_x` is a numpy array of length 3M corresponding to
the M CA atoms, `full_x` will be a numpy array of length 3N
corresponding to the N atoms in the complete geometry, with the CA
coordinates fill in, and the coordinates for the remaining atoms set
to zero.

A related situation is when we have coordinates for a molecule with
atoms in a different order.  Suppose `top2` contains a topology for
the same molecule as `top`, except that the atom names are in a
different order.  Additionally, suppose `x2` contains a geometry for
the atoms in the order of `top2`.  Then we can change order of the
atoms to that of `top` via:

      top_lift_top2 = top.lift_topology(top2, reorder=True)
      x = top_lift_top2.lift_coords(x2)

The extra argument to `lift_topology`, `reorder`, is not strictly
necessary, but it dictates that `lift_topology` should raise an
exception if the topology to be lifted does not contain the same
number of atoms.

Topology lifting considers only the names of atoms in molecules, so it
can be used between Polymers with different names as long as the
Molecules in the corresponding positions in the Polymer tree can be
lifted to one another.

## mol_reader/writer

mol_reader is a generic interface for reading geometries from files.  It supports a number of formats.  

### AMBER formats

mdcrd and rst

### pdb

### trr

### gaussian

### trajdb

## geometry



## trajdb

## gnat