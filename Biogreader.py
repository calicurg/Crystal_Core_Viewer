
fna = 'BIOGRID-ORGANISM-Arabidopsis_thaliana_Columbia-3.4.129.mitab'

FnaDI = {0:fna}

rl = []


def ReadBIOGRID():

    if len(rl) > 0:
        for y in range(len(rl)):
            rl.pop(0)

    fna = FnaDI[0]
    fi = open(fna, 'r')
    RL = fi.readlines()
    fi.close()

    for ls in RL:
        rl.append(ls)
        
        

    print 'Reading file:', fna, ': done'
    print 'total:', len(rl), 'lines in the file'

#print rl[0]

####def Start():
####
####    ReadBIOGRID()
####
####Start()
