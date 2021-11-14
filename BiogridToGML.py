import Biogreader as BR
import igraph as csar

AI = {} ## All internal dictionnaries

## this top-level dictionnary allows
## easiliy manage other dictionnaries, including
## printout the content ,s aving and loading the dictionnaries


AL = {} ## All internal litsts: the same as AI,
        ### but for internal lists (not docts)




AI['Refsi'] = {} ##     Reference singles: in this case, the singles are
           #####   entrez_gene id numbers

AI['EntrName'] = {} ## keys: entrez_gene id numbers
                    ## values :protein names

AI['RefEs'] = {}  ## Reference Edges (here the singles are edges)

AI['GR'] = {0:''}  ## graph objects

AI['First'] = {0:1,
               1:200
               }

AI['SE'] = {} ## "sentences", formed by reference singles,
              ##connected sequentially one-by-one


##{0:20000,
##               1:20400}
               ##1:'end'}

AI['Params'] = {'gml':''} ## parameters
                          ## 'gml': name of gml-file


###################################################


AL['Ol'] = [] ## Ol: Ordered (by frequency) list
               ## of reference singles (entrez_gene id numbers in this case)


AL['RawEL'] = [] ## Raw edges list: contains interaction pairs
                 ##   with entrez_gene id numbers

AL['Es']    = [] ## Edges with absolute indices, \
                 ## referred to Ol (freq-sorted list of reference singles)


AL['EsOl']  = [] ## freq-ordered list of reference edges

AL['CY']    = []  # cycles 


def WriteNames():

    fi = open('EntrezNames.txt', 'w')

    for k, v in AI['EntrName'].items():
        line = k + ' : ' + v +'\n'
        fi.write(line)
        
    fi.close()

    print 'WriteNames: done'        
        

def Add__vinx(vertex_index):

    vinx = vertex_index
####
    ol = AL['Ol'][vinx]
    entrez_gene = ol[1]
    si = entrez_gene

    if  'seinx'  in AI['Refsi'][si].keys():            
        ## seinx; sentence index
        ## sentence is formed by fusion of connected nodes
        ## to form lines (linear graphs            
        seinx = AI['Refsi'][si]['seinx']
        sent = AI['SE'][seinx] ## list of vertex indices connected one by one
        if vinx in sent:
            ## we have got the new cycle here
            ## AcceptCycle
            pos = sent.index(vinx)
            cycle = sent[pos:]
            AL['CY'].append(cycle)
            pass
        else:                
            AI['SE'][seinx].append(vinx)
    else:
        ## determine current sentence index
        seinx = len(AI['SE'])
        ## initialize current sentence
        AI['SE'][seinx] = [vinx]
        ## assign sent. index to reference single
        AI['Refsi'][si]['seinx'] = seinx

    

def BuildCYComplex():


    for edge_line in AL['EsOl']:
        
#        weight = edge_line[0]
        edge = edge_line[1]

        source = edge[0]
        target = edge[1]

###        Add__single(source)
        Add__vinx(source)

        Add__vinx(target)

        
        ## "si" means single
        
            
    print 'BuildCYComplex: done'    
        

def BuildGraph():

    GR = csar.Graph()

    amount_of_nodes = len(AL['Ol'])
    
    GR.add_vertices(amount_of_nodes)
    GR.delete_vertices(0)

    for vinx in range(len(AL['Ol'])):

        ## vinx - vertex index
        ol = AL['Ol'][vinx]
        entrez_gene = ol[1]
        prot_name = AI['EntrName'][entrez_gene]
        
        ## GR.vs()[vinx]['label'] = entrez_gene
        
        GR.vs()[vinx]['label']       = prot_name
        GR.vs()[vinx]['entrez_gene'] = entrez_gene
        GR.vs()[vinx]['prot_name']   = prot_name
        



    EdgesList = []
    for edge_line in AL['EsOl']:
        
#        weight = edge_line[0]
        edge = edge_line[1]
        EdgesList.append(edge)
        
    GR.add_edges(EdgesList)

    for einx in range(len(AL['EsOl'])):

        ## einx - edge index
        
        ol = AL['EsOl'][einx]
        weight = ol[0]

        GR.es()[einx]['weight'] = weight

    
    AI['GR'][0] = GR

    start = AI['First'][0]
    end   = AI['First'][1]
    
    graph_name = 'Biogrid_' + str(start) + '_'+str(end)+ '.gml'
    AI['GR'][0].write_gml(graph_name)
    AI['Params']['gml'] = graph_name
    
    print GR.summary()
    
#BuildGraph()
    


def Clean__list(list_name):

    if len(AL[list_name]) > 0:

        for y in range(len(AL[list_name])):
            AL[list_name].pop(0)

            


def GetRefEdges():

    Clean__list('EsOl')
    AI['RefEs'].clear()
    

    for raw_edge in AL['RawEL']:

        source_entrez = raw_edge[0]
        target_entrez = raw_edge[1]

        source = AI['Refsi'][source_entrez]['inx']
        target = AI['Refsi'][target_entrez]['inx']

        li_edge  = [source,  target] ## edge as list

        li_edge.sort() ### source -> target = target -> source

        edge = tuple(li_edge) ## to enter as a key of dictionnary 

        if edge in AI['RefEs']:
            
            AI['RefEs'][edge] += 1
        else:
            AI['RefEs'][edge] = 1
            
             
    print 'Fill RefEs: done'

    

    for edge, inci in AI['RefEs'].items():
        ol = [inci, edge]
        
        AL['EsOl'].append(ol)

    AL['EsOl'].sort()
    AL['EsOl'].reverse()
    

    print 'Get reference edges: done'

    


def FillOl():


    Clean__list('Ol')
    
    for k, v in AI['Refsi'].items():

        ol = [v['inci'], k] ## frequency, single
        AL['Ol'].append(ol)

    AL['Ol'].sort()
    AL['Ol'].reverse()  ## here we have got the list of singles
                  ## sorted by frequency in descending manner
            
#### Update indices of reference singles in Refsi:

    for y in range(len(AL['Ol'])):
        ol = AL['Ol'][y]
        si = ol[1]
        ## here and everywhere: "si" means "single"
        
        AI['Refsi'][si]['inx'] = y
        ## here and everywhere: "inx" means "index"
    
    print 'Fill Ol: done'        

        

        


def Get_prot_name(ls):


#    ls = 'biogrid:13519|entrez gene/locuslink:"BRCA2(IV)"|entrez gene/locuslink:AT4G00020'
    sl = ls.split(':')
    prot_name = sl[2].split('|')[0]
    if '"' in prot_name:
        prot_name = prot_name.replace('"', '')

    return prot_name
    


def GetEntrezGene(ls):

#    ls = 'entrez gene/locuslink:828230'
    ls = ls.strip()
#    print 'ls:', ls
    entrez_gene = ls.split(':')[1]

    return entrez_gene

    
    


def FillEntrezDI():

    AI['Refsi'].clear()
    AI['EntrName'].clear()
    
    Clean__list('RawEL')

    start = AI['First'][0]
    end   = AI['First'][1]

    print 'len(BR.rl):', len(BR.rl)
    if end == 'end':
        end = len(BR.rl)
        
    for y in range(start, end):
        print y
        ls = BR.rl[y]
        
        sl = ls.split('\t')
#        print 'sl:', sl
        source = sl[0]
        target = sl[1]

        ### 08/08/2017

        if source == target:
##            print y
##            print ls
##            print ''
##            print '=============='

            continue
                  

##        print 'source:', source
##        print 'target:', target

        source_entrez_gene = GetEntrezGene(source)
        target_entrez_gene = GetEntrezGene(target)

##        print 'source: ', source_entrez_gene
##        print 'target:', target_entrez_gene
##        print ''
##        print '==================================='

        raw_edge = [source_entrez_gene, target_entrez_gene]

        AL['RawEL'].append(raw_edge)
        

        if source_entrez_gene in AI['Refsi']:
            AI['Refsi'][source_entrez_gene]['inci'] += 1

            ### 'inci': incidence (frequency)
            
        else:
            AI['Refsi'][source_entrez_gene] = {'inci': 1}



        if target_entrez_gene in AI['Refsi']:
            AI['Refsi'][target_entrez_gene]['inci'] += 1
        else:
            AI['Refsi'][target_entrez_gene] = {'inci': 1}
##
##
############## protein names
##
##            
        source_name_line = sl[2]
        target_name_line = sl[3]

        source_prot_name = Get_prot_name(source_name_line)
        target_prot_name = Get_prot_name(target_name_line)
        
        AI['EntrName'][source_entrez_gene] =  source_prot_name
        AI['EntrName'][target_entrez_gene] =  target_prot_name
        

    print 'Fill Entrez dictionnary: done '

    WriteNames()

    


def ShowHeader():
    header = BR.rl[0]
    sl = header.split('\t')
    for el in enumerate(sl):
        print el

    print '================='

    line = BR.rl[1]
    sl = line.split('\t')
    for el in enumerate(sl):
        print el



def Start():

#    BR.FnaDI[0] = 'C:/Il/__0__Crystal/BiogridSource/BIOGRID-ORGANISM-Bos_taurus-3.4.150.tab2.txt'


    BR.ReadBIOGRID()
    FillEntrezDI()
    FillOl()
    GetRefEdges()
    BuildGraph()
#    BuildCYComplex()

#Start()



    


        
