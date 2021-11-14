#!/usr/bin/python

## ---  Copyright (c) 2017 Ilya Levin. All rights reserved


import LightLinter as LL
import igraph as csar
import tkFileDialog as TF
import BiogridToGML as BIOGR
import tkColorChooser as TC



TK = LL.TK

###################################

## AI : All Internal dIctionnaries
AI = {}


## AL : All internal Lists
AL = {}

TagsDI = {}

GrDI = {}
GrLI = []

AI['LT'] = {'current':0}
AI['WS'] = {'dim':1, 'size':20, 'nei':1, 'p':0.1}
AI['ES'] = {'n':10, 'p':0.7, 'directed':False, 'loops' : True}


###########################################


AI['Script'] = {'WattsStrogatz':
                    {'lin':'Create Watts Strogatz graph',
                      'ai':'WS'
                     },
                'ErdosRenyi':
                    {'lin':'Create Erdos Renyi graph',
                     'ai':'ES'
                        }
                }

#### reverse commands

AI['RevComm'] = {'Create Erdos Renyi graph':'ErdosRenyi',
                 'Create Watts Strogatz graph':'WattsStrogatz'
                 }

CurrDI = {'graph':0,
          'command':'ErdosRenyi',
          'label':'id'}



##AI['RefKCore'] = {} ## Refsi dict. with k-core values as keys (reference singles) 

AI['Shell']    = {} ## key: graph index, value: shell_index list

AI['KCoreOl'] = {} ## key: graph index, value: Ol (frequency-ordered
                    ## list) of coreness (shell index) values


AI['KCoreRefsi'] = {} ## key: graph index,
                      ## value: Refsi for k-core values
                    

############  AL  ############################

AL['VsOl'] = []

AL['CurShell'] = []  ## current shell index list 


##########################################

def SelectColor():
    
    color = TC.askcolor()
    LL.TKDI['en']['color']['bg'] = color[1]
    

def CreateLayoutWholeGraph():

    lt_name = LL.TKDI['en']['layouts'].get()
    if lt_name == 'FR':
        LT_FR()
    elif lt_name == 'Graphopt':
        LT_graphopt()
    elif lt_name == 'GridFR':
        LT_grid_FR()
    elif lt_name == 'Circle':
        LT_circle()
        
    print 'Layout ', lt_name, ' : done'
        

def ResizeCanvas():

    canvas_width  = int(LL.TKDI['en']['cv_width'].get())
    canvas_height = int(LL.TKDI['en']['cv_height'].get())
    LL.TKDI['cv'][0]['width'] = canvas_width
    LL.TKDI['cv'][0]['height'] = canvas_height

    LL.TKDI['en']['scale_length'].delete(0, TK.END)
    LL.TKDI['en']['scale_length'].insert(0, canvas_height)
    LL.TKDI['sc'][0]['length'] = canvas_height

    lt_center_x = canvas_width / 2
    LL.TKDI['en']['lt_center_x'].delete(0, TK.END)
    LL.TKDI['en']['lt_center_x'].insert(0, lt_center_x)
    
    lt_center_y = canvas_height / 2
    LL.TKDI['en']['lt_center_y'].delete(0, TK.END)
    LL.TKDI['en']['lt_center_y'].insert(0, lt_center_y)
    

def Cliques():

    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])
    Gr = GrDI[graph_index]

    ClLI = Gr.cliques()

    LL.TKDI['tx'][0].delete('1.0', TK.END)
        
    for y in range(len(ClLI)):
        cl = ClLI[y]
        if len(cl) < 4:
            continue
        LL.TKDI['tx'][0].insert(TK.END, cl)
        LL.TKDI['tx'][0].insert(TK.END, '\n')
        
    

def BC():

#    pass
    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])
    Gr = GrDI[graph_index]

    BcLI = Gr.bibcoupling()

    LL.TKDI['tx'][0].delete('1.0', TK.END)
        
    for y in range(len(BcLI)):
        bc = BcLI[y]
        header = str(y)+'\n\n'
        LL.TKDI['tx'][0].insert(TK.END, header)
        LL.TKDI['tx'][0].insert(TK.END, bc)
        sep = '\n=======================\n\n'
        LL.TKDI['tx'][0].insert(TK.END, sep)




def Betweenness():

    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])
    CurrentGraph = GrDI[graph_index]
    BwLI = CurrentGraph.betweenness()

    LL.TKDI['tx'][0].delete('1.0', TK.END)
        
    for y in range(len(BwLI)):
        si = BwLI[y]
        si = round(si, 2)
        ls = 'vertex '+str(y)+ ', betw.: '+  str(si)+'\n'
        LL.TKDI['tx'][0].insert(TK.END, ls)
    
    

##BW = Gr.betweenness()

def ArticulationPoints():

    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])
    CurrentGraph = GrDI[graph_index]
    ApLI = CurrentGraph.articulation_points()

    LL.TKDI['tx'][0].delete('1.0', TK.END)
        
    for si in ApLI:
        ls = str(si)+'\n'
        LL.TKDI['tx'][0].insert(TK.END, ls)
    

def AdjustScaleLength():
    
    sc_len = int(LL.TKDI['en']['scale_length'].get())
    LL.TKDI['sc'][0]['length'] = sc_len

def ResizeScale():

    scale_start = int(LL.TKDI['en']['scale_start'].get())
    scale_end = int(LL.TKDI['en']['scale_end'].get())
    scale_step = int(LL.TKDI['en']['scale_step'].get())

    LL.TKDI['sc'][0]['from'] = scale_start
    LL.TKDI['sc'][0]['to']   = scale_end
    LL.TKDI['sc'][0]['tickinterval'] = scale_step
    

def ResizeScaleToDefaultValues():

    LL.TKDI['en']['scale_start'].put(0)
    LL.TKDI['en']['scale_end'].put(50)
    LL.TKDI['en']['scale_step'].put(5)

    ResizeScale()
        
    
def ResizeScaleToCoreness():

    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])

    #########################################
    ### AI['KCoreOl'][graph_index] = Ol 

    if graph_index not in AI['KCoreOl']:
        FillRefKCores()

    Ol = AI['KCoreOl'][graph_index]
    max_coreness = Ol[0][0]

    if max_coreness <= 10:
        scale_step = 1
    elif max_coreness > 10:
        scale_step = max_coreness/10
        
    LL.TKDI['en']['scale_end'].put(max_coreness)
    LL.TKDI['en']['scale_step'].put(scale_step)

    ResizeScale()
    
        

def FillRefKCores():


    Refsi = {}
    Ol = []
    
    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])
    CurrentGraph = GrDI[graph_index]

    if graph_index not in AI['Shell']:
        ShellLI = GetShellIndex()
    else:
        ShellLI = AI['Shell'][graph_index]


    for vinx in range(len(ShellLI)):
        coreness = ShellLI[vinx]

        if coreness in Refsi:
            ## 'inci': incidence (frequency)
            ## "vinxx' : list of vertex indices
            Refsi[coreness]['inci'] += 1
            Refsi[coreness]['vinxx'].append(vinx)
        else:
            Refsi[coreness] = {'inci': 1, 'vinxx':[vinx]}
            
            
    AI['KCoreRefsi'][graph_index] = Refsi
                
    print 'Refsi for k-cores: filled'

    for k, v in Refsi.items():
        ol = [k, v['inci']]
        Ol.append(ol)
                       
    Ol.sort()
    Ol.reverse()
    
    AI['KCoreOl'][graph_index] = Ol        

    print 'Ol for k-cores: filled'

    LL.TKDI['tx'][0].delete('1.0', TK.END)
        
    for ol in Ol:
        ls = 'for coreness: '+str(ol[0])+' the graph has '+str(ol[1])+ ' vertices\n'
        LL.TKDI['tx'][0].insert(TK.END, ls)
        
    

def GetShellIndex():

    AL['CurShell'] = []
    
    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])
    CurrentGraph = GrDI[graph_index]
    LL.TKDI['tx'][0].delete('1.0', TK.END)

    ShellLI = CurrentGraph.shell_index()

    AI['Shell'][graph_index] = ShellLI
    AL['CurShell'] = ShellLI

    

    for el in enumerate(AL['CurShell']):
        ls = 'vertex '+str(el[0])+' : coreness '+str(el[1])+ '\n'
        LL.TKDI['tx'][0].insert(TK.END, ls)
        
    return ShellLI

    print 'GetShellIndex: done'
    


def PrintVsOl():

    LL.TKDI['tx'][0].delete('1.0', TK.END)

    for ol in AL['VsOl']:
        LL.TKDI['tx'][0].insert(TK.END, ol)
        LL.TKDI['tx'][0].insert(TK.END, '\n')
    
    
def FillVsOl():

    AL['VsOl'] = []

    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])
    CurrentGraph = GrDI[graph_index]

    DegLI = CurrentGraph.vs().degree()

    for vinx in range(len(DegLI)):

        degree = DegLI[vinx]

        ol = [degree, vinx]
        AL['VsOl'].append(ol)
        
    AL['VsOl'].sort()
    AL['VsOl'].reverse()
        
    

def PrintEsOl():

    LL.TKDI['tx'][0].delete('1.0', TK.END)

    for ol in BIOGR.AL['EsOl']:
        LL.TKDI['tx'][0].insert(TK.END, ol)
        LL.TKDI['tx'][0].insert(TK.END, '\n')
        
        
    

def PrintVsDegrees():

    LL.TKDI['tx'][0].delete('1.0', TK.END)
    
    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])

    CurrentGraph = GrDI[graph_index]

    DegLI = CurrentGraph.vs().degree()

    for y in range(len(DegLI)):
        ls = str(y)+' : '+str(DegLI[y])+'\n'
        LL.TKDI['tx'][0].insert(TK.END, ls)
        
        

def PrintRefsiOl():

    LL.TKDI['tx'][0].delete('1.0', TK.END)

    print len(BIOGR.AL['Ol'])
    print len(BIOGR.AI['Refsi'])
    
    for ol in BIOGR.AL['Ol']:

        print ol
        

    


def GetGraphAttrValues():

    pass
    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])

    CurrentGraph = GrDI[graph_index]
    GR = CurrentGraph
    vertex_count = GR.vcount()

    current_attr = LL.TKDI['en']['vertex_attrs'].get()

    AttrValuesLI = []
    
    for vinx in range(vertex_count):
        attr_value = GR.vs()[vinx][current_attr]
#	print vinx, attr_value
        AttrValuesLI.append(attr_value)

    LL.Fill__lx(AttrValuesLI, 'attr_values')    
    

def ShowVertexAttrs():

    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])

    CurrentGraph = GrDI[graph_index]
    
    AttrsLI = CurrentGraph.vs.attribute_names()
    LL.Fill__lx(AttrsLI, 'vertex_attrs')
##    LL.Add__lx('vertex_attrs')

def SaveSubgraph():

    pass
    scale_value = LL.TKDI['sc'][0].get()
    graph_name =  LL.TKDI['en']['graph_list'].get()
    graph_name = graph_name.split('.')[0]
    sugr_name = 'sugr_'+graph_name+'_first_'+str(scale_value)+'.gml'
    GrDI['sugr'].write_gml(sugr_name)

    print 'subgraph '+sugr_name+' was written!'



def move__down():

    graph_name = LL.TKDI['en']['graph_list'].get()
    shift_factor = float(LL.TKDI['en']['shift'].get())
    LL.TKDI['cv'][0].move(graph_name, 0, shift_factor)
    

def move__up():

    graph_name = LL.TKDI['en']['graph_list'].get()
    shift_factor = -1*float(LL.TKDI['en']['shift'].get())
    LL.TKDI['cv'][0].move(graph_name, 0, shift_factor)


def move__right():

    graph_name = LL.TKDI['en']['graph_list'].get()
    shift_factor = float(LL.TKDI['en']['shift'].get())
    LL.TKDI['cv'][0].move(graph_name, shift_factor, 0)
    

def move__left():

##    si = Get__surrent__single()
#    gr__inx = int(TKEN['current'].get())
##    LT = csar.Layout(AI['LT'][gr__inx])
##    center = LT.centroid()
##    x, y = center[0], center[1]
    graph_name = LL.TKDI['en']['graph_list'].get()
    shift_factor = -1*float(LL.TKDI['en']['shift'].get())
##    if gr__inx == 0:
##        name = 'gr'
##    else:
##        name = 'sugr'
    LL.TKDI['cv'][0].move(graph_name, shift_factor, 0)


def ReadBiogrid():

#### Biogrid file name
    fna = LL.TKDI['en']['path_to_file'].get()
    BIOGR.BR.FnaDI[0] = fna

    biogr_start = int(LL.TKDI['en']['biogr_start'].get())
    biogr_end   = LL.TKDI['en']['biogr_end'].get()
    if biogr_end.isdigit() == True:
        biogr_end = int(biogr_end)
        

####AI['First'] = {0:2000,
####               1:2300
####               }
    BIOGR.AI['First'][0] = biogr_start
    BIOGR.AI['First'][1] = biogr_end
    
    BIOGR.Start()

    gml_file_name = BIOGR.AI['Params']['gml']    
    fna = LL.TKDI['en']['path_to_file'].get()
    sl = fna.split('/')[:-1]    
    sl.append(gml_file_name)

    gml_fna = '/'.join(sl)
    LL.TKDI['en']['path_to_file'].delete(0, TK.END)
    LL.TKDI['en']['path_to_file'].insert(0, gml_fna)

    ReadGML()
    
    

def ZoomMinus():

    graph_name = LL.TKDI['en']['graph_list'].get()
##    graph_index = int(graph_name.split('__')[0])
    
    x = int(LL.TKDI['en']['lt_center_x'].get())
    y = int(LL.TKDI['en']['lt_center_y'].get())

    zoom_factor = float(1)/float(LL.TKDI['en']['zoom_factor'].get())
    LL.TKDI['cv'][0].scale(graph_name, x, y, zoom_factor, zoom_factor)



def ZoomPlus():

    graph_name = LL.TKDI['en']['graph_list'].get()
##    graph_index = int(graph_name.split('__')[0])
    
    x = int(LL.TKDI['en']['lt_center_x'].get())
    y = int(LL.TKDI['en']['lt_center_y'].get())

    zoom_factor = float(LL.TKDI['en']['zoom_factor'].get())
    LL.TKDI['cv'][0].scale(graph_name, x, y, zoom_factor, zoom_factor)
    
###def ZoomUp():
    
##    zoom_factor = 1.2
##    center = LtDI[0].centroid()
##    x, y = center[0], center[1]    
##    LL.TKDI['cv'][0].scale('GR', x, y, zoom_factor, zoom_factor)
##    LL.TKDI['cv'][0].


def HideLabels():

    line = LL.TKDI['en']['graph_list'].get()
    inx = int(line.split('__')[0])

    la_tag  = str(inx)+'__la'

    LL.TKDI['cv'][0].itemconfig(la_tag, state = LL.TK.HIDDEN)
    

def ShowLabels():

    line = LL.TKDI['en']['graph_list'].get()
    inx = int(line.split('__')[0])

    la_tag  = str(inx)+'__la'

    LL.TKDI['cv'][0].itemconfig(la_tag, state = LL.TK.NORMAL)
    

    

def Select_file():

    file_answer = TF.askopenfile()
    file_path = str(file_answer.name)
    LL.TKDI['en']['path_to_file'].delete(0, TK.END)
    LL.TKDI['en']['path_to_file'].insert(0, file_path)
    


def ReadGML():

##    fna = 'c:/Il/__0__Crystal/Barabasi_200_1.gml'
    fna = LL.TKDI['en']['path_to_file'].get()
    GmlGR = csar.Graph().Read_GML(fna)
    
    sz = LL.TKDI['lx']['graph_list'].size()
    
    inx = str(sz)
    
    
    graph_name = inx + '__' +fna.split('/')[-1]
    GrDI[sz] = GmlGR

    
    
    LL.TKDI['lx']['graph_list'].insert(TK.END, graph_name)
    LL.TKDI['en']['graph_list'].insert(0, graph_name)

    FillVsOl()


########################################

def ExecuteScript():

    line = LL.TKDI['tx'][1].get('1.0', TK.END)
    line = line.strip()
    CommLI = line.split('\n')

    for current_command in CommLI:
        print current_command
        sl = current_command.split('___')
        com_line    = sl[0]
        params_line = sl[1]

        if com_line == 'Create_Erdos_Renyi_graph':
            com_name = AI['RevComm'][com_line]
##            ai = 

        

def Load_script():

#    line =  LL.TKDI['tx'][1].get('1.0', TK.END)
    fi = open('script.txt', 'r')
    line = fi.read()
    fi.close()

    LL.TKDI['tx'][1].delete('1.0', TK.END)
    LL.TKDI['tx'][1].insert('1.0', line)
    

    print 'Load_script: done'


def Save_script():

    line =  LL.TKDI['tx'][1].get('1.0', TK.END)
    fi = open('script.txt', 'w')
    fi.write(line)
    fi.close()

    print 'Save_script: done'


def Get__command__line():

    current_command = CurrDI['command']
    lin_command = AI['Script'][current_command]['lin']
    ai = AI['Script'][current_command]['ai']
    ParamsDI  = AI[ai]

    ParamArray = []
    for k, v in ParamsDI.items():
        # fr  = fragment
        fr = k + ':'+str(v)
        ParamArray.append(fr)

    line =  lin_command +'___' +', '.join(ParamArray)	       

    LL.TKDI['tx'][1].insert(TK.END, '\n')
    LL.TKDI['tx'][1].insert(TK.END, line)
    
        

    
    

def Get__layout__current__graph():

    lt_name = LL.TKDI['en']['layouts'].get()
    line = LL.TKDI['en']['graph_list'].get()
    inx = int(line.split('__')[0])
   
    LtLI = AI['LT'][inx][lt_name]

    return LtLI


def CreateLines():
    
    ecounter = 0
    ### ecounter: edges conuter
    
    lt_name = LL.TKDI['en']['layouts'].get()
    line = LL.TKDI['en']['graph_list'].get()
    graph_name = LL.TKDI['en']['graph_list'].get()
    LL.TKDI['cv'][0].delete(graph_name)
    graph_index = int(line.split('__')[0])

        ## inx: graph index

    TagsDI[graph_index] = {'la':[], 'li':[], 'at':[]}

    #####  la - labels
    ###### li - lines
    #####  at - "atoms" (nodes)

   
    LT = AI['LT'][graph_index][lt_name]

    Gr = GrDI[graph_index]
##    EdgesLI = Gr.get_edgelist()


#######
    
    edge_color = LL.TKDI['en']['color']['bg']
    
        
    ecount = Gr.ecount()
    
#   for pair in EdgesLI:
#    for einx in range(len(EdgesLI)):
    for einx in range(ecount):
        #pair = EdgesLI[einx]
        
##        vinx0 =  pair[0] ## vinx: vertex index
##        vinx1 =  pair[1]
        vinx0 =   Gr.es[einx].source
        vinx1 =   Gr.es[einx].target
        weight_factor = 1
        line_weight = 2 ###weight_factor * inci

##        LT = LtDI[0]
        start = LT[vinx0]
        finish = LT[vinx1]
        
        x0, y0 = start[0], start[1]
        x1, y1 = finish[0], finish[1]

        current_tag = str(graph_index)+'_li_'+str(ecounter)

        edge_dir_name = LL.TKDI['en']['arrows'].get()
        
        ## 06.11.017 -->
        if edge_dir_name == 'arrows':
            edge_direction = LL.TK.LAST
        else:
            edge_direction = None      
        ## 06.11.017 <--    
        
        
        lind = LL.TKDI['cv'][0].create_line(x0, y0, x1, y1,\
                        fill = edge_color,\
                        width = line_weight,\
                ## 06.11.017 -->                                            
                ##        arrow = LL.TK.LAST,\
                          arrow = edge_direction,\
                ## 06.11.017 <--
                        #arrowshape = (13, 17, 7), \
                        tags = current_tag )
#        print 'lind = ', lind

        ecounter += 1

            ##     28/07/2017
    ##    LL.TKDI['cv'][0].addtag_all('GR')
        
        TagsDI[graph_index]['li'].append(current_tag)

    ### total graph tag
        
        LL.TKDI['cv'][0].addtag_withtag(graph_name, current_tag)

    ###all labels of current graph
####        all_lines_tag = str(graph_index)+'__li'
####        
####        LL.TKDI['cv'][0].addtag_withtag(all_lines_tag, current_tag)


#    LL.TKDI['cv'][0].addtag_all('gr')



def CreateLabels():

#    LL.TKDI['cv'][0].delete('GR')
    

    lt_name = LL.TKDI['en']['layouts'].get()
    line = LL.TKDI['en']['graph_list'].get()
    graph_name = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])

    ##############################################

    GR = GrDI[graph_index]


    ##############################################
    LtLI = AI['LT'][graph_index][lt_name]

    ### vinx: vertex index
    all_labels_tag = str(graph_index)+'__la'

    vertex_count = GR.vcount()
    vertex_attr = CurrDI['label'] ## currently displayed attribute
    
    for vinx in range(len(LtLI)):
        pair = LtLI[vinx]
##        si = RefsiOl[vinx][1]

###     07/08/2017        
##        si = str(vinx)
        if vertex_attr == 'id':
            si = int(GR.vs()[vinx]['id'])
        else:
            si = GR.vs()[vinx][vertex_attr]

        current_tag = str(graph_index)+'_la_'+str(vinx)
        
        LL.TKDI['cv'][0].create_text(pair[0], pair[1], \
                              text = si,\
                              fill = 'white',\
                              font = 'Courier 10',\
                                 #     state=LINTER.TK.HIDDEN,\
                                      tags = current_tag)

    ##     28/07/2017
    ##    LL.TKDI['cv'][0].addtag_all('GR')

        TagsDI[graph_index]['la'].append(current_tag)

    ### total graph tag
        LL.TKDI['cv'][0].addtag_withtag(graph_name, current_tag)

    ###all labels of current graph
        
        
        LL.TKDI['cv'][0].addtag_withtag(all_labels_tag, current_tag)
        
    x = int(LL.TKDI['en']['lt_center_x'].get())
    y = int(LL.TKDI['en']['lt_center_y'].get())

    zoom_factor = float(LL.TKDI['en']['init_zoom_factor'].get())
    LL.TKDI['cv'][0].scale(graph_name, x, y, zoom_factor, zoom_factor)

##    LL.TKDI['cv'][0].itemconfig(graph_name, fill = 'red')
    LL.TKDI['cv'][0].itemconfig(all_labels_tag, state = LL.TK.HIDDEN)
    
    CurrDI['graph'] = graph_name



def Visualize():


    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])

##  06.11.2017 --> commented
    
#    if graph_index not in AI['LT']:
    lt_name = LL.TKDI['en']['layouts'].get()
    if lt_name == '':
        LL.TKDI['en']['layouts'].insert(0, 'FR')
        
    CreateLayoutWholeGraph()
##    LT_FR()        
##  06.11.2017 <-- commented

    CreateLines()
    CreateLabels()

    
    
def ShowAllLayoutsForOneGraph(graph_index):

    LL.TKDI['lx']['layouts'].delete(0, TK.END)
    inx = graph_index
    if inx in AI['LT']:
        AllLayoutsLI = AI['LT'][inx].keys()
        LL.Fill__lx(AllLayoutsLI, 'layouts')  
        
    


def PrintSummary():

    line = LL.TKDI['en']['graph_list'].get()
    inx = int(line.split('__')[0])

    CurrentGraph = GrDI[inx]

    TxSummary = CurrentGraph.summary()

    LL.TKDI['tx'][0].delete('1.0', TK.END)
    LL.TKDI['tx'][0].insert(TK.END, TxSummary)
    


def PrintCurrentLayout():

    lt = AI['LT']['current']
    print lt
    print '================================'

    
def LT_circle():

    line = LL.TKDI['en']['graph_list'].get()
    inx = int(line.split('__')[0])

    lt = GrDI[inx].layout_circle()


    LT = csar.Layout(lt)

    x = int(LL.TKDI['en']['lt_center_x'].get())
    y = int(LL.TKDI['en']['lt_center_y'].get())

    LT.center([x, y])
#    LT.scale(5)
#    print LT.coords
    lt  = LT.coords    
    
    
    AI['LT']['current'] = lt
    if inx in AI['LT']:
        AI['LT'][inx]['Circle'] = lt
    else:
        AI['LT'][inx] = {'Circle': lt}

    ShowAllLayoutsForOneGraph(inx)
        
    

    print 'layout circle for graph #', inx, ': done\n'
    print '================================'


def LT_grid_FR():

    line = LL.TKDI['en']['graph_list'].get()
    inx = int(line.split('__')[0])

    lt = GrDI[inx].layout_grid_fruchterman_reingold()


    LT = csar.Layout(lt)

    x = int(LL.TKDI['en']['lt_center_x'].get())
    y = int(LL.TKDI['en']['lt_center_y'].get())

    LT.center([x, y])
#    LT.scale(5)
#    print LT.coords
    lt  = LT.coords    
    
    
    AI['LT']['current'] = lt
    if inx in AI['LT']:
        AI['LT'][inx]['GridFR'] = lt
    else:
        AI['LT'][inx] = {'GridFR': lt}

    ShowAllLayoutsForOneGraph(inx)
        
    

    print 'layout Grid Fruchterman-Reingold for graph #', inx, ': done\n'
    print '================================'

     

def LT_graphopt():


##    lt__kk = Gr.layout_kamada_kawai()
#######################################
    line = LL.TKDI['en']['graph_list'].get()
    inx = int(line.split('__')[0])

    lt = GrDI[inx].layout_graphopt()


    LT = csar.Layout(lt)

    x = int(LL.TKDI['en']['lt_center_x'].get())
    y = int(LL.TKDI['en']['lt_center_y'].get())

    LT.center([x, y])
#    LT.scale(5)
#    print LT.coords
    lt  = LT.coords    
    
    
    AI['LT']['current'] = lt
    if inx in AI['LT']:
        AI['LT'][inx]['Graphopt'] = lt
    else:
        AI['LT'][inx] = {'Graphopt': lt}

    ShowAllLayoutsForOneGraph(inx)
        
    

    print 'layout graphopt for graph #', inx, ': done\n'
    print '================================'
    





def LT_KK():


##    lt__kk = Gr.layout_kamada_kawai()
#######################################
    line = LL.TKDI['en']['graph_list'].get()
    inx = int(line.split('__')[0])

    lt_kk = GrDI[inx].layout_kamada_kawai()


    LT = csar.Layout(lt_kk)

    x = int(LL.TKDI['en']['lt_center_x'].get())
    y = int(LL.TKDI['en']['lt_center_y'].get())

    LT.center([x, y])
#    LT.scale(5)
#    print LT.coords
    lt  = LT.coords    
    
    
    AI['LT']['current'] = lt
    if inx in AI['LT']:
        AI['LT'][inx]['KK'] = lt
    else:
        AI['LT'][inx] = {'KK': lt}

    ShowAllLayoutsForOneGraph(inx)
        
    

    print 'layout Kamada-Kawai for graph #', inx, ': done\n'
    print '================================'
    



def LT_FR():

    line = LL.TKDI['en']['graph_list'].get()
    inx = int(line.split('__')[0])

    lt = GrDI[inx].layout_fruchterman_reingold()


    LT = csar.Layout(lt)

    x = int(LL.TKDI['en']['lt_center_x'].get())
    y = int(LL.TKDI['en']['lt_center_y'].get())

    LT.center([x, y])
#    LT.scale(5)
#    print LT.coords
    lt  = LT.coords    
    
    
    AI['LT']['current'] = lt
    if inx in AI['LT']:
        AI['LT'][inx]['FR'] = lt
    else:
        AI['LT'][inx] = {'FR': lt}

    ShowAllLayoutsForOneGraph(inx)
        
    

    print 'layout Fruchterman-Reingold for graph #', inx, ': done\n'
    print '================================'
    
    
##############  Modeling  ##########################


#WSDI = {'dim':0, 'size':0}

def CreateWSGraph():

    CurrDI['command'] = 'WattsStrogatz'
    
    WS_dim  = AI['WS']['dim']
    WS_size = AI['WS']['size']
    WS_nei  = AI['WS']['nei']
    WS_p    = AI['WS']['p']
    
    


    GR = csar.Graph().Watts_Strogatz(dim = WS_dim, \
                                   size = WS_size,\
                                   nei = WS_nei,\
                                   p = WS_p)

    
    print GR.summary()


    

    sz = LL.TKDI['lx']['graph_list'].size()

    GrDI[sz] = GR
    
    inx = str(sz)
    
    
    graph_name = inx + '__Watts_Strogatz'
    LL.TKDI['lx']['graph_list'].insert(TK.END, graph_name)

#    Get__command__line()


    
def ChangeWSParams():

    AI['WS']['dim']  = int(LL.TKDI['en']['WS_dim'].get())
    AI['WS']['size'] = int(LL.TKDI['en']['WS_size'].get())
    AI['WS']['nei']  = int(LL.TKDI['en']['WS_nei'].get())
    AI['WS']['p']    = float(LL.TKDI['en']['WS_p'].get())

    print 'Watts_Strogatz default parmeters changed:'
    for k, v in AI['WS'].items():
        print k, ':', v
    

def GetWSParams():

    AI['WS']['dim']  = int(LL.TKDI['en']['WS_dim'].get())
    AI['WS']['size'] = int(LL.TKDI['en']['WS_size'].get())
    AI['WS']['nei']  = int(LL.TKDI['en']['WS_nei'].get())
    AI['WS']['p']    = float(LL.TKDI['en']['WS_p'].get())

#    print AI['WS']

    CreateWSGraph()

    LL.TKDI['fr']['WSFrame'].destroy()

    
def AboutCrystalFrame():

    AFrame = LL.TK.Tk()
    AFrame.title('About this program')

    la = LL.TK.Label(AFrame)
    la['text'] = '\t Crystal Core Viewer \t '
    la['font'] = 'Arial 14'
    la.pack()

    la = LL.TK.Label(AFrame)
    la['text'] = ' written by:'
    la['font'] = 'Courier 12'
    la.pack()

    la = LL.TK.Label(AFrame)
    la['text'] = 'Ilya Levin  ilyal_01@yahoo.com'
    la['font'] = 'Courier 14 bold'
    la.pack()

    la = LL.TK.Label(AFrame)
    la['text'] = 'based on'
    la['font'] = 'Courier 12'
    la.pack()
    
    la = LL.TK.Label(AFrame)
    la['text'] = 'Igraph'
    la['font'] = 'Arial 14'
    la.pack()
    
    la = LL.TK.Label(AFrame)
    la['text'] = 'Igraph was written by:'
    la['font'] = 'Courier 12'
    la.pack()
    
    la = LL.TK.Label(AFrame)
    la['text'] = 'Gabor Csardi and Tamas Nepusz'
    la['font'] = 'Courier 14 bold'
    la.pack()
    

def GetWSFrame():

    WSFrame = LL.TK.Tk()
    WSFrame.title('Watts-Strogatz parameters')
    LL.TKDI['fr']['WSFrame'] = WSFrame
    
    LL.TKDI['fr']['WS'] = TK.Frame(WSFrame)
    LL.TKDI['fr']['WS'].grid(row = 1, column = 1)
##    LL.TKDI['fr']['WS']['bd'] = 7
##    LL.TKDI['fr']['WS']['relief'] = TK.RAISED
    
##    LL.TKDI['fr']['WS']['bd'] = 7
##    LL.TKDI['fr']['WS']['relief'] = TK.RAISED
    
    LL.Add__entry('WS_dim',  'WS', 1, 1, 5, 'Arial 10')
    LL.TKDI['en']['WS_dim'].insert(0, AI['WS']['dim'])

    LL.Add__entry('WS_size', 'WS', 2, 1, 5, 'Arial 10')
    LL.TKDI['en']['WS_size'].insert(0, AI['WS']['size'])
    
    LL.Add__entry('WS_nei',  'WS', 3, 1, 5, 'Arial 10')
    LL.TKDI['en']['WS_nei'].insert(0, AI['WS']['nei'])

        
    LL.Add__entry('WS_p',    'WS', 4, 1, 5, 'Arial 10')
    LL.TKDI['en']['WS_p'].insert(0, AI['WS']['p'])
    

    LL.Add__button('GetWSParams', 'WS', 5, 3, 10, '  OK  ')  
    LL.TKDI['bu']['GetWSParams']['command'] = GetWSParams

    LL.Add__button('ChangeWSParams', 'WS', 0, 3, 15, 'Change defaults')  
    LL.TKDI['bu']['ChangeWSParams']['command'] = ChangeWSParams


###############################################################

#    LL.Add__one__frame('WS', 'mod_0', 2, 1)
    



def Watts_Strogatz():

##    WS_dim = int(LL.TKDI['en']['WS_dim'].get())
##    WS_size = int(LL.TKDI['en']['WS_size'].get())    
##    WS_nei = int(LL.TKDI['en']['WS_nei'].get())
##    WS_p = float(LL.TKDI['en']['WS_p'].get())

    GetWSFrame()

    
    

def Erdos_Renyi():

    CurrDI['command'] = 'ErdosRenyi'


    amount_vs = 10 ## amount of vertices
    edges_p = 0.7  ## edges probability
    GR = csar.Graph().Erdos_Renyi(n = amount_vs, \
                                  p = edges_p, \
                                  directed = False,\
                                  loops = True)
    print GR.summary()


    

    sz = LL.TKDI['lx']['graph_list'].size()

    GrDI[sz] = GR
    
    inx = str(sz)
    
    
    graph_name = inx + '__Erdos_Renyi'
    LL.TKDI['lx']['graph_list'].insert(TK.END, graph_name)

    Get__command__line()
    

## Add text windows
    
def Add__txx():
    

    LL.Add__tx(0, 'report',  1, 1, 59, 20, 'blue', 'white', 'Arial 12')
#    LL.Add__tx(1, 'console', 1, 1, 70, 20, '#000062', 'white', 'Courier 10')

    


def reflect_layout(event):

    LL.reflect__lx__in__entry('layouts')
    lt_name = LL.TKDI['en']['layouts'].get()
    line = LL.TKDI['en']['graph_list'].get()
    inx = int(line.split('__')[0])

    LtLI = AI['LT'][inx][lt_name]

    lt__array = []

    for lt_line in LtLI:
        
        x = lt_line[0]
        y = lt_line[1]
        
        xr = round(x, 2)
        yr = round(y, 2)

        lin_x = str(xr)
        lin_y = str(yr)

        lx__line = lin_x +' , '+lin_y
        lt__array.append(lx__line)
        

    LL.Fill__lx(lt__array, 'lt')
    
    
def reflect_curr_graph(event):


#    graph_name = LL.TKDI['en']['graph_list'].get()
    prev_graph_name = CurrDI['graph']
##    print 'prev_graph_name', prev_graph_name
#    LL.TKDI['cv'][0].itemconfig(prev_graph_name, fill = 'yellow')
    LL.TKDI['cv'][0].itemconfig(prev_graph_name, state = LL.TK.HIDDEN)

##    CurrDI['graph'] = graph_name



    pass
    pair = LL.reflect__lx__in__entry('graph_list')
##    line = LL.TKDI['en']['graph_list'].get()
##    inx = int(line.split('__')[0])
    graph_index = pair[0]
    
    ShowAllLayoutsForOneGraph(graph_index)

    current_graph_name =  LL.TKDI['en']['graph_list'].get()
    LL.TKDI['cv'][0].itemconfig(current_graph_name, state = LL.TK.NORMAL)

        
    CurrDI['graph'] =  current_graph_name

    HideLabels()    
    

def reflect_current_attr(event):

    pair = LL.reflect__lx__in__entry('vertex_attrs')
    attr = pair[1]
#    print 'attr', attr
    CurrDI['label'] = attr
    
    GetGraphAttrValues()

    

def reflect_explore(event):

    pair = LL.reflect__lx__in__entry('explore')
    mode = pair[1]

    if mode   == 'vertex_degree':
        ResizeScaleToDefaultValues()
        
    elif mode == 'coreness':
        ResizeScaleToCoreness()
        
    
    

########################################################    

def Add__lxx():

##    LL.Add__lx('AI', 'zero', 1, 1, 20, 7, 'Arial 14')
##    LL.Add__lx('AL', 'zero', 1, 2, 20, 7, 'Arial 14')

    LL.Add__lx('graph_list', 'graph_list', 2, 1, 20, 10, 'Arial 10')
    LL.TKDI['la']['graph_list']['text'] = 'list of graphs'
    LL.TKDI['lx']['graph_list'].bind('<KeyRelease>',    reflect_curr_graph)
    LL.TKDI['lx']['graph_list'].bind('<ButtonRelease>', reflect_curr_graph)


    LL.Add__lx('explore', 'explore', 1, 1, 15, 4, 'Arial 9')
    LL.TKDI['la']['explore']['text'] = 'explore by:'
    LL.TKDI['lx']['explore'].insert(0, 'vertex_degree')
    LL.TKDI['en']['explore'].insert(0, 'vertex_degree')
    LL.TKDI['lx']['explore'].insert(TK.END, 'coreness')
    LL.TKDI['lx']['explore'].bind('<KeyRelease>',    reflect_explore)
    LL.TKDI['lx']['explore'].bind('<ButtonRelease>', reflect_explore)


    LL.Add__lx('vertex_attrs', 'cur_gr_lxx', 1, 1, 15, 7, 'Arial 10')
    LL.TKDI['la']['vertex_attrs']['text'] = 'vertex attributes'
    LL.TKDI['lx']['vertex_attrs'].bind('<KeyRelease>',    reflect_current_attr)
    LL.TKDI['lx']['vertex_attrs'].bind('<ButtonRelease>', reflect_current_attr)

    LL.Add__lx('attr_values',  'cur_gr_lxx', 1, 2, 15, 7, 'Arial 10')
    LL.TKDI['la']['attr_values']['text'] = 'values'

    LL.Add__lx('arrows',  'cur_gr_lxx',      1, 3, 15, 7, 'Arial 10')
    LL.TKDI['lx']['arrows'].insert(0, 'lines')
    LL.TKDI['en']['arrows'].insert(0, 'lines')
    LL.TKDI['lx']['arrows'].insert(0, 'arrows')
    LL.TKDI['la']['arrows']['text'] = 'edge direction'
#    LL.TKDI['la']['arrows']['font'] = 'Arial 9'

    LL.Add__entry('color', 'cur_gr_color', 1, 1, 15, 'Arial 10')
    LL.TKDI['en']['color']['bg'] = 'red'
    LL.Add__button('color', 'cur_gr_color', 1, 4, 15, 'Select color')
    LL.TKDI['bu']['color']['command'] = SelectColor
    LL.TKDI['bu']['color']['font'] = 'Arial 8'


    LL.Add__lx('layouts', 'lt_0', 1, 1, 10, 10, 'Arial 10')
    LL.TKDI['lx']['layouts'].bind('<KeyRelease>',    reflect_layout)
    LL.TKDI['lx']['layouts'].bind('<ButtonRelease>', reflect_layout)

    
    LL.Add__lx('lt',      'lt_1', 1, 1, 20, 10, 'Arial 10')
    LL.TKDI['la']['lt']['text'] = 'coordinates'
     
##########Create sugr labels

def CreateSugrLabels():

#    LL.TKDI['cv'][0].delete('GR')
    

    lt_name = LL.TKDI['en']['layouts'].get()
    line = LL.TKDI['en']['graph_list'].get()
    graph_name = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])

    
    LtLI = AI['LT'][graph_index][lt_name]

    ### vinx: vertex index
    all_labels_tag = str(graph_index)+'__la'

    GR =  GrDI['sugr']

    vertex_count = GR.vcount()
    vertex_attr = CurrDI['label'] ## currently displayed attribute
    
    for vinx in range(len(LtLI)):
        pair = LtLI[vinx]

###     07/08/2017        
##        si = str(vinx)
        if vertex_attr == 'id':
            si = str(vinx)
        else:
            si = GR.vs()[vinx][vertex_attr]
            

        current_tag = str(graph_index)+'_la_'+str(vinx)
        
        LL.TKDI['cv'][0].create_text(pair[0], pair[1], \
                              text = si,\
                              fill = 'white',\
                              font = 'Courier 10',\
                                 #     state=LINTER.TK.HIDDEN,\
                                      tags = current_tag)

    ##     28/07/2017
    ##    LL.TKDI['cv'][0].addtag_all('GR')

        TagsDI[graph_index]['la'].append(current_tag)

    ### total graph tag
        LL.TKDI['cv'][0].addtag_withtag(graph_name, current_tag)

    ###all labels of current graph
        
        
        LL.TKDI['cv'][0].addtag_withtag(all_labels_tag, current_tag)
        
    x = int(LL.TKDI['en']['lt_center_x'].get())
    y = int(LL.TKDI['en']['lt_center_y'].get())

    zoom_factor = int(LL.TKDI['en']['init_zoom_factor'].get())
    LL.TKDI['cv'][0].scale(graph_name, x, y, zoom_factor, zoom_factor)

##    LL.TKDI['cv'][0].itemconfig(graph_name, fill = 'red')
    LL.TKDI['cv'][0].itemconfig(all_labels_tag, state = LL.TK.HIDDEN)
    
    CurrDI['graph'] = graph_name


    
def CreateSugrLines():

    
    ecounter = 0
    ### ecounter: edges conuter
    
##    for pair, inci in RefEsDI.items():
    lt_name = LL.TKDI['en']['layouts'].get()
    line = LL.TKDI['en']['graph_list'].get()
    graph_name = LL.TKDI['en']['graph_list'].get()
    LL.TKDI['cv'][0].delete(graph_name)
    graph_index = int(line.split('__')[0])
    
    

        ## inx: graph index

    TagsDI[graph_index] = {'la':[], 'li':[], 'at':[]}

    #####  la - labels
    ###### li - lines
    #####  at - "atoms" (nodes)

   
    LT = AI['LT'][graph_index][lt_name]

    Gr = GrDI['sugr']
    EdgesLI = Gr.get_edgelist()
    for pair in EdgesLI:
        
        vinx0 =  pair[0] ## vinx: vertex index
        vinx1 =  pair[1]
        weight_factor = 1
        line_weight = 1 ###weight_factor * inci

##        LT = LtDI[0]
        start = LT[vinx0]
        finish = LT[vinx1]
        
        x0, y0 = start[0], start[1]
        x1, y1 = finish[0], finish[1]

        current_tag = str(graph_index)+'_li_'+str(ecounter)

        ## 06.11.017 -->
        edge_dir_name = LL.TKDI['en']['arrows'].get()
        if edge_dir_name == 'arrows':
            edge_direction = LL.TK.LAST
        else:
            edge_direction = None

        edge_color = LL.TKDI['en']['color']['bg']
        ## 06.11.017 <--    

        
        lind = LL.TKDI['cv'][0].create_line(x0, y0, x1, y1,\

                        fill = edge_color,\
                        #width = 2,\
                                      
        #### hiding the line width: 22.05.2017 for Anton Artur.
                        width = line_weight,\
                ## 06.11.017 -->                                            
                ##        arrow = LL.TK.LAST,\
                          arrow = edge_direction,\
                        #arrowshape = (13, 17, 7), \
                ## 06.11.017 <-- 
                        tags = current_tag )
#        print 'lind = ', lind

        ecounter += 1

            ##     28/07/2017
    ##    LL.TKDI['cv'][0].addtag_all('GR')
        
        TagsDI[graph_index]['li'].append(current_tag)

    ### total graph tag
        
        LL.TKDI['cv'][0].addtag_withtag(graph_name, current_tag)

    ###all labels of current graph
####        all_lines_tag = str(graph_index)+'__li'
####        
####        LL.TKDI['cv'][0].addtag_withtag(all_lines_tag, current_tag)


#    LL.TKDI['cv'][0].addtag_all('gr')



def VisualizeSugr():

    CreateSugrLines()
    CreateSugrLabels()
    

def VertexDegreeSubgraph(graph_index):

    current_graph = GrDI[graph_index]
    vert_limit = LL.TKDI['sc'][0].get()

        ############  08/08/2017  -->>
    ###selection = current_graph.vs.select(id_le=vert_limit)
    VsOl = AL['VsOl'][:vert_limit]
#    print VsOl
    VsLI = [ol[1] for ol in VsOl]
#    print VsLI
    
    sugr = current_graph.subgraph(VsLI)   
##    gr = selection.subgraph()
    
###############  <<--  08/08/2017 ############
    
    GrDI['sugr'] = sugr

    lt = sugr.layout_fruchterman_reingold()
    LT = csar.Layout(lt)
    x = int(LL.TKDI['en']['lt_center_x'].get())
    y = int(LL.TKDI['en']['lt_center_y'].get())

    LT.center([x, y])
#####    LT.scale(5)
#####    print LT.coords
    lt  = LT.coords    
    AI['LT']['current'] = lt
    AI['LT'][graph_index] = {'FR': lt}
    LL.TKDI['lx']['layouts'].delete(0, TK.END)
    LL.TKDI['en']['layouts'].delete(0, TK.END)
    LL.TKDI['lx']['layouts'].insert(0, 'FR')
    LL.TKDI['en']['layouts'].insert(0, 'FR')
    

    VisualizeSugr()
        



def KCoreSubgraph(graph_index):

    current_graph = GrDI[graph_index]
    coreness = LL.TKDI['sc'][0].get()

####################################################
##        if coreness in Refsi:
##            ## 'inci': incidence (frequency)
##            ## "vinxx' : list of vertex indices
##            Refsi[coreness]['inci'] += 1
##            Refsi[coreness]['vinxx'].append(vinx)
##        else:
##            Refsi[coreness] = {'inci': 1, 'vinxx':[vinx]}
##            
##            
##    AI['KCoreRefsi'][graph_index] = Refsi

####################################################
    if graph_index not in AI['KCoreRefsi']:
        FillRefKCores()
        
    Refsi = AI['KCoreRefsi'][graph_index]
#    print Refsi

    VsLI = Refsi[coreness]['vinxx']
    
###    if coreness not in Refsi:
        
####        VsLI = 
####        
####    VsOl = AI[] ##AL['VsOl'][:vert_limit]
#####    print VsOl
####    VsLI = [ol[1] for ol in VsOl]
####    #print VsLI
####    
    sugr = current_graph.subgraph(VsLI)   
    
    
    GrDI['sugr'] = sugr

    lt = sugr.layout_fruchterman_reingold()
    LT = csar.Layout(lt)
    x = int(LL.TKDI['en']['lt_center_x'].get())
    y = int(LL.TKDI['en']['lt_center_y'].get())

    LT.center([x, y])
#####    LT.scale(5)
#####    print LT.coords
    lt  = LT.coords    
    AI['LT']['current'] = lt
    AI['LT'][graph_index] = {'FR': lt}
    LL.TKDI['lx']['layouts'].delete(0, TK.END)
    LL.TKDI['en']['layouts'].delete(0, TK.END)
    LL.TKDI['lx']['layouts'].insert(0, 'FR')
    LL.TKDI['en']['layouts'].insert(0, 'FR')
    

    VisualizeSugr()
    


def reflect__gr_sel_scale(event):

    ## cs: current selection
    
    line = LL.TKDI['en']['graph_list'].get()
    graph_index = int(line.split('__')[0])

    explore = LL.TKDI['en']['explore'].get()
        
    if explore == 'vertex_degree':
        VertexDegreeSubgraph(graph_index)
    elif explore == 'coreness':
        KCoreSubgraph(graph_index)

               

def CreateCanvas():

    #### gr_sel_scale: Graph Selection Scale

    LL.TKDI['sc'][0] = TK.Scale(LL.TKDI['fr']['cv'])
    LL.TKDI['sc'][0].grid(row = 1, column = 0)
    LL.TKDI['sc'][0]['orient'] = TK.VERTICAL
    LL.TKDI['sc'][0]['from'] = 0
    LL.TKDI['sc'][0]['to'] = 50
    LL.TKDI['sc'][0]['length'] = 500 #400
    LL.TKDI['sc'][0]['tickinterval'] = 5

    LL.TKDI['sc'][0].bind('<KeyRelease>', reflect__gr_sel_scale)
    LL.TKDI['sc'][0].bind('<ButtonRelease>', reflect__gr_sel_scale)
    
        
    LL.TKDI['cv'] = {0:TK.Canvas(LL.TKDI['fr']['cv'])}
    LL.TKDI['cv'][0].grid(row = 1, column = 1) ##, sticky = TK.N+TK.E+TK.S+TK.W)
    LL.TKDI['cv'][0]['bg'] = 'black'
    LL.TKDI['cv'][0]['width'] = 600 ##500
    LL.TKDI['cv'][0]['height'] = 500 ##400
    
                    

def CreateInternalFrame():

    LL.TKDI['fr']['zero'] = LL.TK.Frame(LL.TKDI['nb'][0])
    LL.TKDI['fr']['zero'] = LL.TK.Frame(LL.TKDI['nb'][0])    
    LL.TKDI['nb'][0].add(LL.TKDI['fr']['zero'], text = 'Internal')
    


def CreateFrames():

    LL.TKDI['fr']['file'] = LL.TK.Frame(LL.TKDI['fr']['root'])
    LL.TKDI['fr']['file'].grid(row = 0, column = 1, sticky = TK.N+TK.E+TK.S+TK.W)
    LL.Add__entry('path_to_file', 'file', 1,1,  70, 'Arial 10')
    LL.TKDI['la']['path_to_file']['text'] = 'Path to file'
    
    LL.Add__button('select_file', 'file', 1, 3, 15, 'Select file')
    LL.TKDI['bu']['select_file']['command'] = Select_file

    LL.TKDI['fr']['0'] = LL.TK.Frame(LL.TKDI['fr']['root'])
    LL.TKDI['fr']['0'].grid(row = 1, column = 1, sticky = TK.N+TK.E+TK.S+TK.W)

    LL.TKDI['fr']['00'] = LL.TK.Frame(LL.TKDI['fr']['0'])
    LL.TKDI['fr']['00'].grid(row = 1, column = 1, sticky = TK.N+TK.E+TK.S+TK.W)
    
####    LL.Add__one__frame('0', 'root', 1, 1)
####    LL.Add__one__frame('00', '0', 1, 1) ## path --> Notebook
##       LL.Add__one__frame('00', 'root', 1, 1)
    LL.TKDI['nb'] = {0:LL.ttk.Notebook(LL.TKDI['fr']['00'])}    
    LL.TKDI['nb'][0].grid(row = 1, column = 1, sticky = TK.N+TK.E+TK.S+TK.W)


    
    LL.Add__one__frame('graph_list',    '00', 1, 0)

    LL.Add__one__frame('explore', 'graph_list', 1, 1)
    LL.Add__one__frame('graph_control', 'graph_list', 5, 1)
    
    LL.Add__button('ZoomPlus', 'graph_control', 1, 1, 10, ' Zoom + ')
    LL.TKDI['bu']['ZoomPlus']['command'] = ZoomPlus

    LL.Add__button('ZoomMinus', 'graph_control', 1, 2, 10, ' > < ')
    LL.TKDI['bu']['ZoomMinus']['command'] = ZoomMinus

    LL.Add__button('move__down', 'graph_control', 2, 2, 10, ' \\/ ')
    LL.TKDI['bu']['move__down']['command'] = move__down

    LL.Add__button('move__up', 'graph_control', 2, 1, 10, ' /\\ ')
    LL.TKDI['bu']['move__up']['command'] = move__up

    LL.Add__button('move__right', 'graph_control', 3, 2, 10, ' --> ')
    LL.TKDI['bu']['move__right']['command'] = move__right

    LL.Add__button('move__left', 'graph_control', 3, 1, 10, ' <-- ')
    LL.TKDI['bu']['move__left']['command'] = move__left

    
##    LL.TKDI['fr']['zero'] = LL.TK.Frame(LL.TKDI['nb'][0])
##    LL.TKDI['fr']['zero'] = LL.TK.Frame(LL.TKDI['nb'][0])    
##    LL.TKDI['nb'][0].add(LL.TKDI['fr']['zero'], text = 'Concordance')

    LL.TKDI['fr']['one'] = LL.TK.Frame(LL.TKDI['nb'][0])    
    LL.TKDI['nb'][0].add(LL.TKDI['fr']['one'], text = 'Graph')

    LL.TKDI['fr']['cv'] = LL.TK.Frame(LL.TKDI['fr']['one'])
    LL.TKDI['fr']['cv'].grid(row = 1, column = 1, sticky = TK.N+TK.E+TK.S+TK.W)
     
##    LL.Add__one__frame('cv', 'one', 1, 1)
##
    LL.TKDI['fr']['two'] = LL.TK.Frame(LL.TKDI['nb'][0])    
    LL.TKDI['nb'][0].add(LL.TKDI['fr']['two'], text = 'Parameters')
    LL.TKDI['fr']['two']['bd'] = 7

    LL.Add__entry('cv_width', 'two', 1, 1, 10, 'Arial 10')
    LL.TKDI['la']['cv_width']['text'] = '  Canvas width  '
    LL.TKDI['en']['cv_width'].insert(0, 600)
    

    
    LL.Add__entry('cv_height', 'two', 2, 1, 10, 'Arial 10')
    LL.TKDI['la']['cv_height']['text'] = '  Canvas height  '
    LL.TKDI['en']['cv_height'].insert(0, 500)


    LL.Add__entry('lt_center_x', 'two', 3, 1, 7, 'Arial 10')
    LL.TKDI['la']['lt_center_x']['text'] = '  Layout center X  '
    LL.TKDI['en']['lt_center_x'].insert(0, 300)
    
    LL.Add__entry('lt_center_y', 'two', 4, 1, 7, 'Arial 10')
    LL.TKDI['la']['lt_center_y']['text'] = '  Layout center Y  '
    LL.TKDI['en']['lt_center_y'].insert(0, 250)

    LL.Add__entry('init_zoom_factor', 'two', 5, 1, 7, 'Arial 10')
    LL.TKDI['la']['init_zoom_factor']['text'] = 'Initial zoom factor '
    LL.TKDI['en']['init_zoom_factor'].insert(0, 20)

    LL.Add__entry('zoom_factor', 'two', 7, 1, 7, 'Arial 10')
    LL.TKDI['la']['zoom_factor']['text'] = '   Zoom factor   '
    LL.TKDI['en']['zoom_factor'].insert(0, 1.2)
    
    LL.Add__entry('shift', 'two', 8, 1, 7, 'Arial 10')
    LL.TKDI['la']['shift']['text'] = '   Shift   '
    LL.TKDI['en']['shift'].insert(0, 5)
    
    LL.Add__entry('biogr_start', 'two', 9, 1, 7, 'Arial 10')
    LL.TKDI['la']['biogr_start']['text'] = ' Biogrid start '
    LL.TKDI['en']['biogr_start'].insert(0, 1)

    LL.Add__entry('biogr_end', 'two', 10, 1, 7, 'Arial 10')
    LL.TKDI['la']['biogr_end']['text'] = ' Biogrid end '
    LL.TKDI['en']['biogr_end'].insert(0, 200)

    LL.Add__entry('scale_start', 'two', 11, 1, 7, 'Arial 10')
    LL.TKDI['la']['scale_start']['text'] = ' Scale start '
    LL.TKDI['en']['scale_start'].insert(0, 0)

    LL.Add__entry('scale_end', 'two', 12, 1, 7, 'Arial 10')
    LL.TKDI['la']['scale_end']['text'] = ' Scale end '
    LL.TKDI['en']['scale_end'].insert(0, 50)

    LL.Add__entry('scale_step', 'two', 13, 1, 7, 'Arial 10')
    LL.TKDI['la']['scale_step']['text'] = ' Scale step '
    LL.TKDI['en']['scale_step'].insert(0, 5)

    LL.Add__entry('scale_length', 'two', 14, 1, 7, 'Arial 10')
    LL.TKDI['la']['scale_length']['text'] = ' Scale length '
    LL.TKDI['en']['scale_length'].insert(0, 400)

    

    
################### Current Graph    ###########################################

    LL.TKDI['fr']['cur_graph'] = LL.TK.Frame(LL.TKDI['nb'][0])
    LL.Add__one__frame('cur_gr_lxx',  'cur_graph', 1, 1)
    LL.Add__one__frame('cur_gr_color', 'cur_graph', 2, 1)
    
    LL.TKDI['nb'][0].add(LL.TKDI['fr']['cur_graph'], text = 'Current Graph')
               

##    LL.TKDI['fr']['layout'] = LL.TK.Frame(LL.TKDI['nb'][0])    
##    LL.TKDI['nb'][0].add(LL.TKDI['fr']['layout'], text = 'Layout')
##    LL.Add__one__frame('lt_0', 'layout', 1, 0 )
##    LL.Add__one__frame('lt_1', 'layout', 1, 1 )
##

    
#############################################################
    LL.TKDI['fr']['report'] = LL.TK.Frame(LL.TKDI['nb'][0])    
    LL.TKDI['nb'][0].add(LL.TKDI['fr']['report'], text = 'Report')
               

    LL.TKDI['fr']['layout'] = LL.TK.Frame(LL.TKDI['nb'][0])    
    LL.TKDI['nb'][0].add(LL.TKDI['fr']['layout'], text = 'Layout')
    LL.Add__one__frame('lt_0', 'layout', 1, 0 )
    LL.Add__one__frame('lt_1', 'layout', 1, 1 )
#    LL.TKDI['fr']['two']['bd'] = 7

##    LL.TKDI['fr']['two']['relief'] = TK.SUNKEN

##    LL.TKDI['fr']['modeling'] = LL.TK.Frame(LL.TKDI['nb'][0])    
##    LL.TKDI['nb'][0].add(LL.TKDI['fr']['modeling'], text = 'Modeling')
#    LL.Add__one__frame('mod_0', 'modeling', 1, 1)

   
##    LL.TKDI['fr']['console'] = LL.TK.Frame(LL.TKDI['nb'][0])    
##    LL.TKDI['nb'][0].add(LL.TKDI['fr']['console'], text = 'Console')
##    LL.Add__one__frame('cons_1', 'console', 2, 1)
##    LL.Add__button('save_script', 'cons_1', 1, 1, 10, 'Save_script')
##    LL.TKDI['bu']['save_script']['command'] = Save_script
##    

##    LL.Add__button('load_script', 'cons_1', 1, 2, 10, 'Load_script')
##    LL.TKDI['bu']['load_script']['command'] = Load_script
##   
##    LL.Add__button('run_script', 'cons_1', 1, 3, 15, '__Execute script__')
##    LL.TKDI['bu']['run_script']['command'] = ExecuteScript
##
    
    


##    LL.TKDI['fr']['two'] = LL.TK.Frame(LL.TKDI['nb'][0])    
##    LL.TKDI['nb'][0].add(LL.TKDI['fr']['two'], text = 'Semblocks')


def SamplePrintout():

    print 'SamplePrintout'
    

def CreateForms():
##       LL.Add__one__frame('00', 'root', 1, 1)

    LL.Create__root('   Crystal:   Core Viewer  ')
#    LL.Add__one__frame(0, 'root', 1, 1)
    CreateFrames()

#    CreateInternalFrame()

    CreateCanvas()

    #######################

    Add__lxx()

    Add__txx()


def CreateMenu():

    LL.TKDI['me'][0] = LL.TK.Menu(LL.TKDI['fr']['root'])
       
    LL.TKDI['me'][1] = TK.Menu(LL.TKDI['me'][0])
    LL.TKDI['me'][1].add_command(label = 'Read GML', command = ReadGML)
    LL.TKDI['me'][1].add_command(label = 'Read Biogrid mitab file', command = ReadBiogrid)
    LL.TKDI['me'][1].add_separator()
    LL.TKDI['me'][1].add_command(label = 'Save current subgraph', command = SaveSubgraph)
 

    LL.TKDI['me'][2] = TK.Menu(LL.TKDI['me'][0])
    LL.TKDI['me'][2].add_command(label = 'Erdos-Renyi', command = Erdos_Renyi)
    LL.TKDI['me'][2].add_command(label = 'Watts_Strogatz', command = Watts_Strogatz)
    

    LL.TKDI['me'][3] = TK.Menu(LL.TKDI['me'][0])
    LL.TKDI['me'][3].add_command(label = 'Fruchterman-Reingold', command = LT_FR)
    LL.TKDI['me'][3].add_command(label = 'Graphopt ', command = LT_graphopt)
    LL.TKDI['me'][3].add_command(label = 'Grid F-R', command = LT_grid_FR)
    LL.TKDI['me'][3].add_command(label = 'Circle', command = LT_circle)
    
    LL.TKDI['me'][4] = TK.Menu(LL.TKDI['me'][0])
    LL.TKDI['me'][4].add_command(label = 'Summary', command = PrintSummary)
#    LL.TKDI['me'][4].add_command(label = 'PrintRefsiOl', command = PrintRefsiOl)
    LL.TKDI['me'][4].add_command(label = 'Degree of vertices', command = PrintVsDegrees)
##    LL.TKDI['me'][4].add_command(label = 'PrintEsOl', command = PrintEsOl)
##    LL.TKDI['me'][4].add_command(label = 'PrintVsOl', command = PrintVsOl)

    LL.TKDI['me'][4].add_separator()
    LL.TKDI['me'][4].add_command(label = 'Shell indices', command = GetShellIndex)
##    LL.TKDI['me'][4].add_command(label = 'FillRefKCores', command = FillRefKCores)
    LL.TKDI['me'][4].add_separator()
    LL.TKDI['me'][4].add_command(label = 'Articulation points', command = ArticulationPoints)
    LL.TKDI['me'][4].add_command(label = 'Betweenness', command = Betweenness)
    LL.TKDI['me'][4].add_command(label = 'Biliographic coupling', command = BC)
    LL.TKDI['me'][4].add_command(label = 'Cliques', command = Cliques)



    LL.TKDI['me'][5] = TK.Menu(LL.TKDI['me'][0])
    LL.TKDI['me'][5].add_command(label = 'Visualize', command = Visualize)
    LL.TKDI['me'][5].add_command(label = 'Resize canvas', command = ResizeCanvas)    
    LL.TKDI['me'][5].add_command(label = 'Resize scale', command = ResizeScale)


    
    LL.TKDI['me'][5].add_separator()
    LL.TKDI['me'][5].add_command(label = 'Zoom + ', command = ZoomPlus)
    LL.TKDI['me'][5].add_command(label = 'Zoom - ', command = ZoomMinus)
    LL.TKDI['me'][5].add_separator()
    LL.TKDI['me'][5].add_command(label = 'Move Up  /\\', command = move__up)
    LL.TKDI['me'][5].add_command(label = 'Move Down  \\/', command = move__down)
    LL.TKDI['me'][5].add_separator()
    LL.TKDI['me'][5].add_command(label = 'Move Right -->', command = move__right)
    LL.TKDI['me'][5].add_command(label = 'Move Left <--', command = move__left)

    
    LL.TKDI['me'][7] = TK.Menu(LL.TKDI['me'][0])
    LL.TKDI['me'][7].add_command(label = 'Show labels', command = ShowLabels)
    LL.TKDI['me'][7].add_command(label = 'Hide labels', command = HideLabels)
    LL.TKDI['me'][7].add_command(label = 'Show vertex attributes', command = ShowVertexAttrs)
#    LL.TKDI['me'][7].add_command(label = 'Get values of current graph attribute', command = GetGraphAttrValues)

    LL.TKDI['me'][8] = TK.Menu(LL.TKDI['me'][0])
    LL.TKDI['me'][8].add_command(label = 'About Crystal', command = AboutCrystalFrame)



#########################################################    
    LL.TKDI['me'][0].add_cascade(label = 'File', menu = LL.TKDI['me'][1])
##    LL.TKDI['me'][0].add_cascade(label = 'Build', menu = LL.TKDI['me'][2])
    LL.TKDI['me'][0].add_cascade(label = 'Layout', menu = LL.TKDI['me'][3])
    LL.TKDI['me'][0].add_cascade(label = 'Report', menu = LL.TKDI['me'][4])
    LL.TKDI['me'][0].add_cascade(label = 'Visualize', menu = LL.TKDI['me'][5])
    LL.TKDI['me'][0].add_cascade(label = 'Labels', menu = LL.TKDI['me'][7])
    LL.TKDI['me'][0].add_cascade(label = 'Help', menu = LL.TKDI['me'][8])

    LL.TKDI['fr']['root'].config(menu = LL.TKDI['me'][0])


def Start():

    CreateForms()

    CreateMenu()

#    fna = 'C:/Il/__0__Crystal/Biogrid_2_300.gml'        
#    LL.TKDI['en']['path_to_file'].insert(0, fna)
#    ReadGML()

    

    LL.TKDI['fr']['root'].mainloop()    

##########################

Start()    

    
