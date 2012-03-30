
filename = 'two_chain_atoms'

outfile = 'two_chain_coords.dat'

with open(filename) as infile:
    with open(outfile, 'w') as outfile:
        lastidx = -1
        for line in infile:
            x = line[31:38]
            y = line[38:46]
            z = line[46:54]
            for c in [x, y, z]:
                outfile.write(c + '\n')

        
