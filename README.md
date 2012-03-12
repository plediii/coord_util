
# coord_util

coord_util is a library for reading, manipulating and writing molecule
geometries. coord_util can read and write geometries in several common
formats.  

## Dependecies

coord_util depends on my `tempfile_util` module.

coord_util also depends on `numpy` (tested with 1.6.1).  

coord_util contains a module for storing geometries in a useful
database format.  In order to make use of this module, coord_util
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

 For instance, if the center of geometry of atoms arranged in the
corners of a square is the center of the square:

    center_of_geometry(np.array([0., 0., 0., 
                                 1., 0., 0.,
				 0., 1., 0.,
				 0., 0., 1.,]))
				 == np.array([0.5, 0.5, 0.5])

##### rmsd

rmsd returns the *least* root mean square distance between two
geometries.


##### translate
##### dihedral

##### atom_dist
##### rotate_euler
##### transform



## topology

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