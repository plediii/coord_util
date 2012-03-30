
filename = 'two_chain_atoms'

outfile = 'two_chain_residues.dat'

with open(filename) as infile:
    with open(outfile, 'w') as outfile:
        lastidx = -1
        for line in infile:
            res = line[17:20]
            residx = int(line[23:26])
            if residx != lastidx:
                outfile.write(res + '\n')
                lastidx = residx
        
