# -*- coding: cp1251 -*-

import Tkinter as TK
import ttk
import pickle as PI


TKDI = {'lx':{},
        'fr':{},
        'en':{},
        'la':{},
        'tx':{},
 	'me':{},
	'bu':{},
	'sc':{},
        'cb':{}
        }

        
############ Linter Light s

class Ent(TK.Entry):

     

    def clear(self):

        self.delete(0, TK.END)

    def put(self, line):

        self.clear()
        self.insert(0, line)
        
    def Grid(self, rinx, cinx):

        self.grid(row = rinx, column = cinx)
 

def Create__root(root_title):        

    TKDI['fr']['root'] = TK.Tk()
    TKDI['fr']['root'].title(root_title)



def Add__one__frame(frame_name, parent_frame, rinx, cinx):

    TKDI['fr'][frame_name] = TK.Frame(TKDI['fr'][parent_frame])
    TKDI['fr'][frame_name].grid(row = rinx, column = cinx)                                       
    
def Add__cb(entry_name, frame_name, rinx, cinx, winx, font_description):

    TKDI['la'][entry_name] = TK.Label(TKDI['fr'][frame_name])
    TKDI['la'][entry_name]['text']  = '  '+entry_name+'  '
    TKDI['la'][entry_name]['relief'] = TK.RAISED
    TKDI['la'][entry_name]['bd'] = 5
    TKDI['la'][entry_name].grid(row = rinx, column = cinx)

    TKDI['cb'][entry_name] = ttk.Combobox(TKDI['fr'][frame_name])
    TKDI['cb'][entry_name]['width'] = winx
    TKDI['cb'][entry_name].grid(row = (rinx), column = cinx+1)
    TKDI['cb'][entry_name]['font'] = font_description


##def Add__button('SelectFile', 0,1,3, 6, '...')
def Add__button(button_name, frame_name, rinx, cinx, winx, button_text):

    TKDI['bu'][button_name] = TK.Button(TKDI['fr'][frame_name])
    TKDI['bu'][button_name]['text']  = button_text
    TKDI['bu'][button_name]['relief'] = TK.RAISED
    TKDI['bu'][button_name]['bd'] = 5
    TKDI['bu'][button_name].grid(row = rinx, column = cinx)
    TKDI['bu'][button_name]['width'] = winx


def Add__entry(entry_name, frame_name, rinx, cinx, winx, font_description):

    TKDI['la'][entry_name] = TK.Label(TKDI['fr'][frame_name])
    TKDI['la'][entry_name]['text']  = '  '+entry_name+'  '
#    TKDI['la'][entry_name]['relief'] = TK.RAISED
    TKDI['la'][entry_name]['bd'] = 5
    TKDI['la'][entry_name].grid(row = rinx, column = cinx)

    #TKDI['en'][entry_name] = TK.Entry(TKDI['fr'][frame_name])
    TKDI['en'][entry_name] = Ent(TKDI['fr'][frame_name])
    TKDI['en'][entry_name]['width'] = winx
    TKDI['en'][entry_name].grid(row = (rinx), column = cinx+1)
    TKDI['en'][entry_name]['font'] = font_description

    
def Add__tx(txname, frame_name, rinx, cinx, winx, hinx, bg, fg, font_description):

    TKDI['tx'][txname] = TK.Text(TKDI['fr'][frame_name])
    TKDI['tx'][txname].grid(row = rinx, column = cinx)
    TKDI['tx'][txname]['bg'] = bg
    TKDI['tx'][txname]['fg'] = fg
    TKDI['tx'][txname]['width'] = winx
    TKDI['tx'][txname]['height'] = hinx
    TKDI['tx'][txname]['font'] = font_description    


def reflect__lx__in__entry(lxname):
    
#    lxname = 'Headers'
    cs = int(TKDI['lx'][lxname].curselection()[0])
    si = TKDI['lx'][lxname].get(cs)
    TKDI['en'][lxname].delete(0, TK.END)
    TKDI['en'][lxname].insert(0, si)
    
    return [cs, si]


def reflect__lx__in__other__entry(lxname, entry_name):
    
#    lxname = 'Headers'
    cs = int(TKDI['lx'][lxname].curselection()[0])
    si = TKDI['lx'][lxname].get(cs)
    TKDI['en'][lxname].delete(0, TK.END)
    TKDI['en'][entry_name].insert(0, si)
    
    return [cs, si]


def reflect__lx__in__tx(lxname, txname):
    
#    lxname = 'Headers'
    cs = int(TKDI['lx'][lxname].curselection()[0])
    si = TKDI['lx'][lxname].get(cs)
    TKDI['tx'][txname].delete('1.0', TK.END)
    TKDI['tx'][txname].insert('1.0', si)
    
    return [cs, si]


def Add__lx(lxname, frame_name, rinx, cinx, winx, hinx, font_description):

    TKDI['la'][lxname] = TK.Label(TKDI['fr'][frame_name])
    TKDI['la'][lxname]['text']  = '  '+lxname+'  '
#    TKDI['la'][lxname]['relief'] = TK.RAISED
    TKDI['la'][lxname]['bd'] = 5
    TKDI['la'][lxname].grid(row = rinx, column = cinx)

#    TKDI['en'][lxname] = TK.Entry(TKDI['fr'][frame_name])
    TKDI['en'][lxname] = Ent(TKDI['fr'][frame_name])

    TKDI['en'][lxname]['width'] = winx
    TKDI['en'][lxname].grid(row = (rinx+1), column = cinx)
    TKDI['en'][lxname]['font'] = font_description

    def reflect_lx(event):
        cs = int(TKDI['lx'][lxname].curselection()[0])
        si = TKDI['lx'][lxname].get(cs)
        TKDI['en'][lxname].delete(0, TK.END)
        TKDI['en'][lxname].insert(0, si)        
        
        
    TKDI['lx'][lxname] = TK.Listbox(TKDI['fr'][frame_name])
    TKDI['lx'][lxname].grid(row = (rinx+2), column = cinx)
    TKDI['lx'][lxname]['width'] = winx
    TKDI['lx'][lxname]['height'] = hinx
    TKDI['lx'][lxname]['relief'] = TK.SUNKEN
    TKDI['lx'][lxname]['bd'] = 7
    TKDI['lx'][lxname]['font'] = font_description
    TKDI['lx'][lxname].bind('<KeyRelease>', reflect_lx)
    TKDI['lx'][lxname].bind('<ButtonRelease>', reflect_lx)

   

def Fill__lx(array, lxname):

    TKDI['lx'][lxname].delete(0, TK.END)
    for si in array:
        TKDI['lx'][lxname].insert(TK.END, si)

        
######### particulars                                  
##    
##def Add__frames():
##
##    Add__one__frame(0, 'root', 1, 1)
##    Add__one__frame(1, 'root', 2, 1)
##    
##def Add__lxx():
##    
##    Add__lx('Descriptors', 0, 1, 1, 15, 7)
##    TKDI['lx']['Descriptors']['font'] = 'Arial 14'
##    arr = Semblocks
##    arr.sort()
##    Fill__lx(arr, 'Descriptors')
##
##
##    Add__lx('sent', 0, 1, 2, 70, 7)
##    TKDI['lx']['sent']['font'] = 'Arial 12'
##
##def Add__Txx():
##
##    TKDI['tx']['sent'] = TK.Text(TKDI['fr'][1])
##    TKDI['tx']['sent'].grid(row = 1, column = 1)
##    TKDI['tx']['sent']['width'] = 70
##    TKDI['tx']['sent']['font'] = 'Courier 15'
##    TKDI['tx']['sent']['height'] = 10
##    
##    





def Create__menu():

    TKDI['me'][0] = TK.Menu(TKDI['fr']['root'])
    TKDI['me'][1] = TK.Menu(TKDI['me'][0])
##TKDI['me'][1].add_command(label = 'Print_blocks', command = Print_blocks)
##TKDI['me'][1].add_command(label = 'Accept_block_content', command = Accept_block_content)


    TKDI['me'][0].add_cascade(label = 'General', menu = TKDI['me'][1])

    TKDI['fr']['root'].config(menu = TKDI['me'][0])
    
##def Start():
##    
##    Create__empty__structure()
##    Add__frames()
##    Add__lxx()
##    Add__Txx()
##    
##    Reflections()
##    
##
##Start()

    
