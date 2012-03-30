


def do_extract(filename, outfile):
    with open(filename) as infile:
        with open(outfile, 'w') as outfile:
            for line in infile:
                if line[12].isdigit():
                    atom = line[13:16].strip() + line[12]
                else:
                    atom = line[12:16].strip()
                outfile.write(atom + '\n')



for (infile, outfile) in [('two_chain_atoms', 'two_chain_atoms.dat'),
                          ('1XFQ_atoms', '1XFQ_atoms.dat')]:
    do_extract(infile, outfile)

        
